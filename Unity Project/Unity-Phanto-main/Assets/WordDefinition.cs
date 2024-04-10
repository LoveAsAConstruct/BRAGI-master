using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WordDefinition : ScriptableObject
{
    public string Word;
    public string spanishWord;
    public string pronounciation;
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
