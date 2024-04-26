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
        // Determine which word to check
        string currentWordToCheck = (flashcardInitializer != null && !string.IsNullOrEmpty(flashcardInitializer.wordData.spanishWord))
            ? flashcardInitializer.wordData.spanishWord
            : wordToCheck;

        // Convert response and word to check to lowercase and remove accents
        string normalizedResponse = RemoveAccents(response.ToLower());
        string normalizedWordToCheck = RemoveAccents(currentWordToCheck.ToLower());

        if (normalizedResponse.Contains(normalizedWordToCheck))
        {
            Debug.Log("Word found: " + normalizedWordToCheck +", in " +normalizedResponse);
            onCorrectResponse.Invoke();
        }
        else
        {
            Debug.Log("Word not found: " + normalizedWordToCheck + ", in " + normalizedResponse);
            onIncorrectResponse.Invoke();
        }
    }

    string RemoveAccents(string input)
    {
        byte[] bytes = System.Text.Encoding.GetEncoding("Cyrillic").GetBytes(input);
        return System.Text.Encoding.ASCII.GetString(bytes);
    }
}
