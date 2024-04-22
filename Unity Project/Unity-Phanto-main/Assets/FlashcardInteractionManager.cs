using UnityEngine;
using UnityEngine.EventSystems;

public class FlashcardInteractionManager : MonoBehaviour, IPointerClickHandler
{
    public AudioSource audioSource;

    void Start()
    {
        if (audioSource == null)
        {
            audioSource = GetComponent<AudioSource>();
        }
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        // Check if the eventData is from the Oculus Touch controller
        if (eventData.button == PointerEventData.InputButton.Left)
        {
            PlayAudio();
        }
    }

    private void PlayAudio()
    {
        if (audioSource != null && !audioSource.isPlaying)
        {
            audioSource.Play();
        }
    }
}
