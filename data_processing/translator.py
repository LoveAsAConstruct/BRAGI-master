import os
import pandas as pd
import requests
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

# Setup your Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(
    r"C:\Users\NuVu\Downloads\BRAGI-master\BRAGI-master\data_processing\authentication\eco-signal-420813-b52a3632523a.json"
)

# Initialize Google Translate and Text-to-Speech clients
translate_client = translate.Client(credentials=credentials)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

def translate_text(text, target='es'):
    """Translate text to the target language."""
    result = translate_client.translate(text, target_language=target)
    return result['translatedText']

def text_to_speech(text, language_code='es-ES'):
    """Convert text to speech."""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    return response.audio_content

def get_definition(word):
    """Get the definition of a word using the Free Dictionary API."""
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data = response.json()
        return data[0]['meanings'][0]['definitions'][0]['definition']
    return "No definition found"

def main(words):
    # Create directories inside the 'translation' folder
    base_path = 'translation'
    audio_files_path = os.path.join(base_path, 'audio_files')
    os.makedirs(audio_files_path, exist_ok=True)
    
    data = []

    for index, word in enumerate(words):
        translated_word = translate_text(word)
        audio_content = text_to_speech(translated_word)
        audio_file_path = os.path.join(audio_files_path, f'{translated_word}.mp3')
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_content)
        
        definition = get_definition(word)
        data.append([index, word, translated_word, os.path.abspath(audio_file_path), definition])
        print(f'Processed {word}')

    # Save data to CSV in the 'translation' folder
    csv_file_path = os.path.join(base_path, 'translated_words.csv')
    df = pd.DataFrame(data, columns=['Index', 'Original Word', 'Translated Word', 'Audio File Path', 'Definition'])
    df.to_csv(csv_file_path, index=False)
    print("Data saved to CSV.")

if __name__ == "__main__":
    # Example list of words
    words = [
        "person", "bicycle", "car", "motorcycle", "airplane",
        "bus", "train", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "bird",
        "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee",
        "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
        "wine glass", "cup", "fork", "knife", "spoon",
        "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut",
        "cake", "chair", "couch", "potted plant", "bed",
        "dining table", "toilet", "TV", "laptop", "mouse",
        "remote", "keyboard", "cell phone", "microwave", "oven",
        "toaster", "sink", "refrigerator", "book", "clock",
        "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
    ]
    main(words)
