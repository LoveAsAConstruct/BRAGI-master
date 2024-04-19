import pandas as pd
import os

def generate_csharp(csv_path, output_path):
    df = pd.read_csv(csv_path)
    with open(output_path, 'w') as file:
        file.write("using UnityEngine;\n")
        file.write("using UnityEditor;\n\n")
        file.write("public class CreateWordDataAssets {\n")
        file.write("    [MenuItem(\"WordData/Create Assets\")]\n")
        file.write("    public static void CreateAssets() {\n")
        
        for index, row in df.iterrows():
            asset_name = f"word_{index}"
            file.write(f"        WordContainer asset_{index} = ScriptableObject.CreateInstance<WordContainer>();\n")
            file.write(f"        asset_{index}.englishWord = \"{row['Original Word']}\";\n")
            file.write(f"        asset_{index}.spanishWord = \"{row['Translated Word']}\";\n")
            file.write(f"        asset_{index}.pronounciationClip = AssetDatabase.LoadAssetAtPath<AudioClip>(\"Assets/Data/Audio/{os.path.basename(row['Audio File Path'])}\");\n")
            file.write(f"        asset_{index}.definition = \"{row['Definition'].replace('\"', '\\"').replace('\n', '\\n')}\";\n")
            file.write(f"        AssetDatabase.CreateAsset(asset_{index}, \"Assets/Data/WordData/{asset_name}.asset\");\n")
            file.write(f"        AssetDatabase.SaveAssets();\n")
        
        file.write("        EditorUtility.DisplayDialog(\"Asset Creation\", \"Word Data Assets Created\", \"OK\");\n")
        file.write("    }\n")
        file.write("}\n")

csv_path = "C:\\Users\\NuVu\\Downloads\\BRAGI-master\\BRAGI-master\\translation\\translated_words.csv"
output_path = "C:\\Users\\NuVu\\Downloads\\BRAGI-master\\BRAGI-master\\Unity Project\\Unity-Phanto-main\\Assets\\Scripts\\CreateWordDataAssets.cs"
generate_csharp(csv_path, output_path)
