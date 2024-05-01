using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.Collections.Generic;
using Oculus;
using UnityEditor.Experimental.GraphView;

public class YoloRequester : MonoBehaviour
{
    public GameObject objectPrefab; // Assign your text prefab in the inspector
    public GameObject quizPrefab;
    public Camera active_camera;
    private string url = "http://127.0.0.1:5000/detect";
    private bool isRequestInProgress = false;
    private List<GameObject> instantiatedTextObjects = new List<GameObject>();
    public CardOffset offset;
    void Update()
    {
        // Check if the right trigger is pressed and no request is currently in progress
        if (OVRInput.GetDown(OVRInput.Button.One, OVRInput.Controller.RTouch) && !isRequestInProgress)
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
                    // Calculate screen positions for raycasting
                    float scaledX1 = ((item.x1 + item.x2) / 2 + offset.offset.x) * scalingFactor;
                    float scaledY1 = (inputWidth - (item.y1 + item.y2) / 2 + offset.offset.y) * scalingFactor;
                    Vector3 screenPosition = new Vector3(scaledX1, scaledY1, 0);

                    // Cast a ray from the camera through the calculated screen position
                    Ray ray = active_camera.ScreenPointToRay(screenPosition);
                    RaycastHit hit;
                    float depth = 4f; // Default depth if no object is hit
                    Vector3 worldPosition;
                    // Check if the ray hits any collider in the scene
                    if (Physics.Raycast(ray, out hit))
                    {
                        // Use the hit point as the world position
                        worldPosition = hit.point;
                    }
                    else
                    {
                        // If nothing is hit, use the default depth
                        worldPosition = active_camera.ScreenToWorldPoint(new Vector3(scaledX1, scaledY1, active_camera.nearClipPlane + depth));
                    }
                    GameObject finalobj = objectPrefab;
                    if (Random.value > 0.5f)
                        finalobj = quizPrefab;
                    var objectInstance = Instantiate(finalobj, worldPosition, Quaternion.identity);
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
