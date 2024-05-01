using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
public class KeyboardManager : MonoBehaviour
{
    private TouchScreenKeyboard overlayKeyboard;
    public static string inputText = "";
    public TMP_InputField inputField = null;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (overlayKeyboard != null)
            inputText = overlayKeyboard.text;
    }
    public void Selected()
    {
        overlayKeyboard = TouchScreenKeyboard.Open("", TouchScreenKeyboardType.Default);
    }
}
