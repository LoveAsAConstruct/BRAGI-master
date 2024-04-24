using UnityEngine;
using UnityEngine.EventSystems;
using System.Collections.Generic;

public class OVRPointer : MonoBehaviour
{
    public float pointerLength = 5.0f; // Max length of the pointer
    public GameObject dot; // Pointer dot to show at the hit location
    public OVRInput.Controller controller = OVRInput.Controller.RTouch; // Default to the right controller

    public LineRenderer lineRenderer = null;

    private void Awake()
    {
        lineRenderer = GetComponent<LineRenderer>();
        if (lineRenderer == null)
        {
            lineRenderer = gameObject.AddComponent<LineRenderer>();
            lineRenderer.startWidth = 0.01f;
            lineRenderer.endWidth = 0.01f;
            lineRenderer.positionCount = 2;
            Debug.Log("LineRenderer configured with new instance.");
        }
        else
        {
            Debug.Log("LineRenderer component found.");
        }

        if (dot != null)
        {
            dot.SetActive(false);
            Debug.Log("Dot GameObject found and set to inactive.");
        }
        else
        {
            Debug.Log("No Dot GameObject assigned.");
        }
    }

    private void Update()
    {
        UpdatePointer();
    }

    private void UpdatePointer()
    {
        // Raycast forward from the controller
        RaycastHit hit;
        Vector3 forward = transform.forward;
        Vector3 startPosition = transform.position;
        bool hasHit = Physics.Raycast(startPosition, forward, out hit, pointerLength);
        Debug.Log($"Raycasting from {startPosition} forward {forward} with length {pointerLength}.");

        // Set the pointer length
        float currentPointerLength = hasHit ? hit.distance : pointerLength;
        lineRenderer.SetPosition(0, startPosition);
        lineRenderer.SetPosition(1, startPosition + forward * currentPointerLength);
        Debug.Log($"Pointer length set to {currentPointerLength}.");

        // Show the dot if hit something
        if (dot != null)
        {
            dot.SetActive(hasHit);
            if (hasHit)
            {
                dot.transform.position = hit.point;
                Debug.Log($"Dot positioned at hit point: {hit.point}.");
            }
            else
            {
                Debug.Log("No hit detected; dot deactivated.");
            }
        }

        // Check for interaction
        if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, controller))
        {
            Debug.Log("Primary Index Trigger pressed.");
            if (hasHit && hit.collider != null)
            {
                hit.collider.gameObject.SendMessage("OnPointerClick", SendMessageOptions.DontRequireReceiver);
                Debug.Log($"OnPointerClick message sent to {hit.collider.gameObject.name}.");
            }
            else
            {
                Debug.Log("Trigger pressed but no collider hit.");
            }
        }
    }
}
