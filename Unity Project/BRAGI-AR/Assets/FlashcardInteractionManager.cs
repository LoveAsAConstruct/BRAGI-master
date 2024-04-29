using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using UnityEngine.Events;

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
                    CheckResponse(responseText);
                }
            }
        }
    }

    void CheckResponse(string response)
    {
        string currentWordToCheck = (flashcardInitializer != null && !string.IsNullOrEmpty(flashcardInitializer.wordData.spanishWord))
            ? flashcardInitializer.wordData.spanishWord
            : wordToCheck;

        string normalizedResponse = RemoveAccents(response.ToLower());
        string normalizedWordToCheck = RemoveAccents(currentWordToCheck.ToLower());

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
        byte[] bytes = System.Text.Encoding.GetEncoding("Cyrillic").GetBytes(input);
        return System.Text.Encoding.ASCII.GetString(bytes);
    }
}
