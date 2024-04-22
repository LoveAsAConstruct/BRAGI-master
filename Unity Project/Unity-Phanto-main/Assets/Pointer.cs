using UnityEngine;
using UnityEditor;
using System.Collections;
public class Pointer : MonoBehaviour
{
    public float defaultLength = 3.0f; // Default length of the pointer
    public GameObject dot; // A dot to visualize the end of the pointer

    private LineRenderer lineRenderer = null;

    private void Awake()
    {
        lineRenderer = GetComponent<LineRenderer>();
    }

    private void Update()
    {
        UpdateLine();
    }

    private void UpdateLine()
    {
        // Use physics raycast to see if we hit anything
        RaycastHit hit = CreateRaycast(defaultLength);

        // Default end of the line
        Vector3 endPosition = transform.position + (transform.forward * defaultLength);

        // If we hit something, shorten the line
        if (hit.collider != null)
            endPosition = hit.point;

        // Set position of the line renderer
        lineRenderer.SetPosition(0, transform.position);
        lineRenderer.SetPosition(1, endPosition);

        // Position the dot
        if (dot != null)
            dot.transform.position = endPosition;
    }

    private RaycastHit CreateRaycast(float length)
    {
        RaycastHit hit;
        Ray ray = new Ray(transform.position, transform.forward);
        Physics.Raycast(ray, out hit, defaultLength);
        return hit;
    }
}
