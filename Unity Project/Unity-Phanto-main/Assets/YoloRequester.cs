using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.Collections.Generic;
using Oculus;

public class YoloRequester : MonoBehaviour
{
    public GameObject objectPrefab; // Assign your text prefab in the inspector
    public Camera active_camera;
    private string url = "http://127.0.0.1:5000/detect";
    private bool isRequestInProgress = false;
    private List<GameObject> instantiatedTextObjects = new List<GameObject>();
    public CardOffset offset;
    void Update()
    {
        // Check if the right trigger is pressed and no request is currently in progress
        if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch) && !isRequestInProgress)
        {
            StartCoroutine(SendRequestToServer());
        }
    }

    IEnumerator SendRequestToServer()
    {
        isRequestInProgress = true;
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Response: " + request.downloadHandler.text);
            foreach (var textObject in instantiatedTextObjects)
            {
                Destroy(textObject);
            }
            instantiatedTextObjects.Clear();

            try
            {
                var detections = JsonUtility.FromJson<RootObject>("{\"Items\":" + request.downloadHandler.text + "}");
                float inputWidth = 1080;
                float scalingFactor = active_camera.pixelWidth / inputWidth;
                foreach (var item in detections.Items)
                {
                    float scaledX1 = ((item.x1 + item.x2) / 2 + offset.offset.x) * scalingFactor;
                    float scaledY1 = (inputWidth - (item.y1 + item.y2) / 2 + offset.offset.y) * scalingFactor;
                    float depth = 70f;
                    Vector3 worldPosition = active_camera.ScreenToWorldPoint(new Vector3(scaledX1, scaledY1, active_camera.nearClipPlane + depth), Camera.MonoOrStereoscopicEye.Left);

                    var objectInstance = Instantiate(objectPrefab, worldPosition, Quaternion.identity);
                    objectInstance.transform.forward = active_camera.transform.forward;
                    var flashcardManager = objectInstance.GetComponent<FlashcardInitializer>();
                    flashcardManager.SetFlashcard($"{item.objectName}");
                    instantiatedTextObjects.Add(objectInstance);
                }
            }
            catch (System.Exception e)
            {
                Debug.Log("Error parsing JSON: " + e.Message);
            }
        }
        else
        {
            Debug.Log("Error: " + request.error);
        }

        isRequestInProgress = false;
    }

    [System.Serializable]
    public class DetectionItem
    {
        public string objectName;
        public float confidence;
        public float x1;
        public float y1;
        public float x2;
        public float y2;
    }

    [System.Serializable]
    public class RootObject
    {
        public DetectionItem[] Items;
    }
}
