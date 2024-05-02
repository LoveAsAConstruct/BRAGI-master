using UnityEngine;

// Ensure the Oculus namespace is included if using a specific Oculus integration package
using Oculus;

public class ToggleObject : MonoBehaviour
{
    public GameObject objectToToggle; // Drag the object to toggle in the inspector

    void Update()
    {
        // Check if the X button on the left hand controller is pressed
        if (OVRInput.GetDown(OVRInput.Button.Three, OVRInput.Controller.LTouch))
        {
            // Toggle the active state of the object
            if (objectToToggle != null)
            {
                objectToToggle.SetActive(!objectToToggle.activeSelf);
            }
        }
    }
}
