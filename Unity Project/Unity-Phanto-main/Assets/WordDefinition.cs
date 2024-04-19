using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[CreateAssetMenu(fileName = "Data", menuName = "WordData/WordContainer", order = 1)]
public class WordContainer : ScriptableObject
{
    public string englishWord;
    public string spanishWord;
    public string englishPhonetics;
    public string spanishPhonetics;
    public AudioClip pronounciationClip;
    public string definition;
    public enum Gender { female, male}
    public Gender gender = Gender.male;
    public enum Tag { female, male}
    public Tag[] tags;
    public Sprite background;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
