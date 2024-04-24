using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.XR;

public class JoystickOffsetController : MonoBehaviour
{
    public CardOffset cardOffset;
    public float scalar = 10;
    void Update()
    {
        if (cardOffset == null)
            return;

        // Check if the left Touch controller is connected
        var leftHandDevices = new List<InputDevice>();
        InputDevices.GetDevicesAtXRNode(XRNode.LeftHand, leftHandDevices);
        if (leftHandDevices.Count == 0)
            return;

        InputDevice leftController = leftHandDevices[0];

        // Get the joystick input
        leftController.TryGetFeatureValue(CommonUsages.primary2DAxis, out Vector2 joystickInput);

        // Update the CardOffset's offset
        cardOffset.offset += joystickInput*scalar;

        // Check if the joystick is clicked
        if (leftController.TryGetFeatureValue(CommonUsages.primary2DAxisClick, out bool isClicked) && isClicked)
        {
            cardOffset.offset = Vector2.zero;
        }
    }
}
