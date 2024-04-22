using UnityEngine;
using TMPro; // Include the TextMeshPro namespace

public class FlashcardScript : MonoBehaviour
{
    public TMP_Text englishText;
    public TMP_Text spanishText;
    public TMP_Text definitionText;
    public AudioSource audioSource;

    // Method to set flashcard data
    public void SetFlashcard(string inputEnglishWord)
    {
        WordContainer wordData = FindWordDataByEnglish(inputEnglishWord);
        if (wordData != null)
        {
            englishText.text = wordData.englishWord;
            spanishText.text = wordData.spanishWord;
            definitionText.text = wordData.definition;
            audioSource.clip = wordData.pronounciationClip;
            audioSource.Play(); // Play audio when the word is set
        }
        else
        {
            Debug.LogError("Word not found: " + inputEnglishWord);
        }
    }

    // Helper method to find the matching WordContainer
    private WordContainer FindWordDataByEnglish(string englishWord)
    {
        // Assuming you have an array or a list that contains all your WordContainers
        foreach (WordContainer word in Resources.LoadAll<WordContainer>("WordData"))
        {
            if (word.englishWord.ToLower() == englishWord.ToLower())
                return word;
        }
        return null;
    }
}
