import os
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

# Setup your Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(
    'path_to_your_service_account_file.json'
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

def main(words):
    os.makedirs('audio_files', exist_ok=True)
    translated_words = []
    
    for word in words:
        translated_word = translate_text(word)
        translated_words.append(translated_word)
        audio_content = text_to_speech(translated_word)
        with open(f'audio_files/{translated_word}.mp3', 'wb') as audio_file:
            audio_file.write(audio_content)
            print(f'Generated audio file for: {translated_word}')

    return translated_words

# Example list of words
words = ["cat", "dog", "bicycle"]
translated_words = main(words)
print("Translated words:", translated_words)
