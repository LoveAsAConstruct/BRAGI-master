using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro; // Make sure to include this if using TextMeshPro
using System.Collections.Generic; // Import this for using List<>

public class YoloRequester : MonoBehaviour
{
    public GameObject textPrefab; // Assign your text prefab in the inspector
    public Camera active_camera;
    private string url = "http://127.0.0.1:5000/detect";
    private bool isRequestInProgress = false;
    private List<GameObject> instantiatedTextObjects = new List<GameObject>();

    void Update()
    {
        if (!isRequestInProgress)
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
            // Clear existing text objects
            foreach (var textObject in instantiatedTextObjects)
            {
                Destroy(textObject);
            }
            instantiatedTextObjects.Clear(); // Clear the list after destroying the objects

            // Parse and instantiate new text objects
            try
            {
                var detections = JsonUtility.FromJson<RootObject>("{\"Items\":" + request.downloadHandler.text + "}");
                float scalingFactor = active_camera.pixelWidth / 580; // Calculate scaling factor based on a 640 pixel width
                foreach (var item in detections.Items)
                {
                    // Apply the scaling factor to the coordinates
                    float scaledX1 = item.x1 * scalingFactor;
                    float scaledY1 = item.y1 * scalingFactor;

                    // Adjust the Z value as needed to ensure it's within the camera's clipping range
                    float depth = 100f; // Example depth; adjust this based on your scene's scale and camera setup

                    Vector3 worldPosition = active_camera.ScreenToWorldPoint(new Vector3(scaledX1, scaledY1, active_camera.nearClipPlane + depth));

                    var textInstance = Instantiate(textPrefab, worldPosition, Quaternion.identity);

                    // Make the text face the camera
                    textInstance.transform.forward = active_camera.transform.forward;

                    var textComponent = textInstance.GetComponent<TextMeshPro>(); // Or GetComponent<TextMeshProUGUI>() if it's a UI element
                    textComponent.text = $"{item.objectName} ({item.confidence})";
                    instantiatedTextObjects.Add(textInstance);
                }

                Vector3 pos = active_camera.ScreenToWorldPoint(new Vector3(active_camera.pixelWidth/2, active_camera.pixelHeight/2, active_camera.nearClipPlane + 100));

                var text = Instantiate(textPrefab, pos, Quaternion.identity);

                // Make the text face the camera
                text.transform.forward = active_camera.transform.forward;

                var textc = text.GetComponent<TextMeshPro>(); // Or GetComponent<TextMeshProUGUI>() if it's a UI element
                textc.text = $"Center";
                instantiatedTextObjects.Add(text);
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
