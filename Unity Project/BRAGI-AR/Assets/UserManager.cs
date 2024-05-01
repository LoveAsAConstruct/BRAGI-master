using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking; // For UnityWebRequest
using System;
using TMPro;
public class UserManager : MonoBehaviour
{
    public int UserID = 0;
    public InputField usernameInput;
    public TextMeshProUGUI incorrectUsernameText;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return))
        {
            FieldSubmitted();
        }
    }

    public void FieldSubmitted()
    {
        if (usernameInput != null && !string.IsNullOrWhiteSpace(usernameInput.text))
        {
            StartCoroutine(GetUserId(usernameInput.text));
        }
    }

    IEnumerator GetUserId(string username)
    {
        string url = "http://localhost:5000/user/" + username; // Change the URL as needed
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + webRequest.error);
                incorrectUsernameText.text = "User not found!";
            }
            else
            {
                try
                {
                    UserIDResponse response = JsonUtility.FromJson<UserIDResponse>(webRequest.downloadHandler.text);
                    UserID = response.user_id;
                    ChangeUser(UserID);
                }
                catch (Exception ex)
                {
                    Debug.LogError("JSON Error: " + ex.Message);
                    incorrectUsernameText.text = "Error retrieving user ID.";
                }
            }
        }
    }

    void ChangeUser(int userID)
    {
        UserID = userID;
        FlashcardInteractionManager[] slides = GameObject.FindObjectsOfType<FlashcardInteractionManager>();
        foreach (FlashcardInteractionManager slide in slides)
        {
            slide.userId = userID;
        }
    }

    [Serializable]
    public class UserIDResponse
    {
        public int user_id;
    }
}
