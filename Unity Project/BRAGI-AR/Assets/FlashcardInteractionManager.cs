using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using UnityEngine.Events;
using System;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;

public class FlashcardInteractionManager : MonoBehaviour
{
    public string url = "http://localhost:5000/listen";
    public Button listenButton;
    public Text resultText;  // UI Text to display the response

    public string wordToCheck = "example";  // Default word to check in the response, used if no initializer is provided
    public FlashcardInitializer flashcardInitializer;  // Optional initializer to dynamic word data

    public UnityEvent onCorrectResponse;  // Event triggered when the response is correct
    public UnityEvent onIncorrectResponse;  // Event triggered when the response is incorrect
    public int userId; // User ID to send with the log

    void Start()
    {
        listenButton.onClick.AddListener(OnListenButtonPressed);
    }

    void OnListenButtonPressed()
    {
        StartCoroutine(SendRequest());
    }

    IEnumerator SendRequest()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
                resultText.text = "Failed to get response: " + www.error;
                onIncorrectResponse.Invoke();
            }
            else
            {
                string responseText = www.downloadHandler.text;
                Debug.Log(responseText);
                //resultText.text = "Response: " + responseText;

                // Check if response is null or empty before processing
                if (string.IsNullOrEmpty(responseText))
                {
                    Debug.LogError("Received empty or null response.");
                    onIncorrectResponse.Invoke();
                }
                else
                {
                    //resultText.text = "Response: " + RemoveAccents(responseText.ToLower());
                    Debug.Log("Raw response: " + responseText);
                    CheckResponse(responseText);
                }
            }
        }
    }

    void CheckResponse(string response)
    {
        string decodedResponse = DecodeUnicodeEscapes(response);

        string currentWordToCheck = (flashcardInitializer != null && !string.IsNullOrEmpty(flashcardInitializer.wordData.spanishWord))
            ? flashcardInitializer.wordData.spanishWord
            : wordToCheck;

        string normalizedResponse = RemoveAccents(decodedResponse.ToLower());
        string normalizedWordToCheck = RemoveAccents(currentWordToCheck.ToLower());
        print("checking  normalized " + normalizedWordToCheck.ToLower() + " in response " + normalizedResponse.ToLower());
        int threshold = 2;

        if (normalizedResponse.Contains(normalizedWordToCheck))
        {
            Debug.Log("Word found: " + normalizedWordToCheck + ", in " + normalizedResponse);
            onCorrectResponse.Invoke();
            StartCoroutine(SendLogToServer(userId, normalizedWordToCheck, true));
        }
        else
        {
            Debug.Log("Word not found: " + normalizedWordToCheck + ", in " + normalizedResponse);
            onIncorrectResponse.Invoke();
            StartCoroutine(SendLogToServer(userId, normalizedWordToCheck, false));
        }
    }

    public static string DecodeUnicodeEscapes(string input)
    {
        return Regex.Replace(input, @"\\u(?<Value>[a-fA-F0-9]{4})", m =>
        {
            return ((char)int.Parse(m.Groups["Value"].Value, System.Globalization.NumberStyles.HexNumber)).ToString();
        });
    }
    int ComputeLevenshteinDistance(string s1, string s2)
    {
        int len1 = s1.Length;
        int len2 = s2.Length;
        int[,] d = new int[len1 + 1, len2 + 1];

        if (len1 == 0) return len2;
        if (len2 == 0) return len1;

        for (int i = 0; i <= len1; i++) d[i, 0] = i;
        for (int j = 0; j <= len2; j++) d[0, j] = j;

        for (int i = 1; i <= len1; i++)
        {
            for (int j = 1; j <= len2; j++)
            {
                int cost = (s2[j - 1] == s1[i - 1]) ? 0 : 1;
                d[i, j] = Math.Min(
                    Math.Min(d[i - 1, j] + 1, d[i, j - 1] + 1),
                    d[i - 1, j - 1] + cost);
            }
        }
        return d[len1, len2];
    }

    bool IsCloseMatch(string response, string phraseToCheck, int threshold)
    {
        int n = phraseToCheck.Length;
        response = response.ToLower().Trim(); // Normalize the response
        phraseToCheck = phraseToCheck.ToLower().Trim(); // Normalize the word/phrase to check

        for (int i = 0; i <= response.Length - n; i++)
        {
            string segment = response.Substring(i, n);
            if (ComputeLevenshteinDistance(segment, phraseToCheck) <= threshold)
                return true;
        }
        return false;
    }
    IEnumerator SendLogToServer(int userId, string word, bool isCorrect)
    {
        LogData requestData = new LogData(userId, word, isCorrect);
        string jsonData = JsonUtility.ToJson(requestData);
        Debug.Log("Request data: " + jsonData);  // This should now correctly display the JSON structure.

        using (UnityWebRequest www = new UnityWebRequest("http://localhost:5000/log", "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError("Log failed: " + www.error);
            }
            else
            {
                Debug.Log("Log success: " + www.downloadHandler.text);
            }
        }
    }



    [System.Serializable]
    public class LogData
    {
        public int userid;
        public string word;
        public bool correct;

        public LogData(int userId, string word, bool isCorrect)
        {
            this.userid = userId;
            this.word = word;
            this.correct = isCorrect;
        }
    }


    string RemoveAccents(string input)
    {
        string normalizedString = input.Normalize(NormalizationForm.FormD);
        StringBuilder stringBuilder = new StringBuilder();

        foreach (char c in normalizedString)
        {
            if (CharUnicodeInfo.GetUnicodeCategory(c) != UnicodeCategory.NonSpacingMark)
            {
                stringBuilder.Append(c);
            }
        }

        return stringBuilder.ToString().Normalize(NormalizationForm.FormC);
    }

}
