using UnityEngine;

public class RandomizeChessboardRotation : MonoBehaviour
{
    public float angle = 15;
    void Update()
    {
        // Check for right trigger input (assuming the use of an axis named "Fire1" for simplicity)
        if (Input.GetButtonDown("Fire1")) // This might be replaced with your specific input for the right trigger
        {
            // Generate random angles for each axis
            float randomXRotation = 90+Random.Range(-angle, angle); // Pitch
            //float randomYRotation = 180+Random.Range(-60, 60); // Yaw
            float randomZRotation = Random.Range(-angle, angle); // Roll

            // Apply the random rotation to the chessboard
            transform.rotation = Quaternion.Euler(randomXRotation, 180, randomZRotation);
        }
    }
}
