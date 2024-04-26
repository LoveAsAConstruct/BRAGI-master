using System.Collections.Generic;
using System;
using TMPro;
using UnityEngine;

public class FlashcardInitializer : MonoBehaviour
{
    public TMP_Text englishText;
    public TMP_Text spanishText;
    public TMP_Text definitionText;
    public AudioSource audioSource;
    public WordContainer wordData;
    private List<string> words = new List<string> {
        "person", "bicycle", "car", "motorcycle", "airplane",
        "bus", "train", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "bird",
        "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee",
        "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
        "wine glass", "cup", "fork", "knife", "spoon",
        "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut",
        "cake", "chair", "couch", "potted plant", "bed",
        "dining table", "toilet", "TV", "laptop", "mouse",
        "remote", "keyboard", "cell phone", "microwave", "oven",
        "toaster", "sink", "refrigerator", "book", "clock",
        "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
    };

    public void SetFlashcard(string inputEnglishWord)
    {
        wordData = FindWordDataByEnglish(inputEnglishWord);
        if (wordData != null)
        {
            englishText.text = wordData.englishWord;
            spanishText.text = wordData.spanishWord;
            definitionText.text = wordData.definition;
            audioSource.clip = wordData.pronounciationClip;
            //audioSource.Play(); // Play audio when the word is set
        }
        else
        {
            Debug.LogError("Word not found: " + inputEnglishWord);
        }
    }

    private WordContainer FindWordDataByEnglish(string englishWord)
    {
        int index = words.FindIndex(w => w.Equals(englishWord, StringComparison.OrdinalIgnoreCase));
        if (index != -1)
        {
            string path = $"WordData/word_{index}";
            Debug.LogError("Path " + path);
            return Resources.Load<WordContainer>(path);
        }
        return null;
    }
}
