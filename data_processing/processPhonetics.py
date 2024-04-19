import pandas as pd
import epitran
import traceback
def phonetic_transcription(word, lang_code):
    """Transcribes a word into its phonetic representation using epitran."""
    try:
        epi = epitran.Epitran(lang_code)
        return epi.transliterate(word)
    except Exception as e:
        # If there's an error, log it and return a placeholder or the original word
        print(f"Error transcribing word '{word}': {e}")
        traceback.print_exc()
        return "N/A"  # Or return word if you prefer to keep the original word in case of failure

def process_csv(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Check if necessary columns exist
    if not all(col in df.columns for col in ['Index','Original Word','Translated Word','Audio File Path','Definition']):
        raise ValueError("CSV file is missing one or more required columns.")
    
    # Append phonetic pronunciation columns
    df['English Phonetic'] = df['Original Word'].apply(lambda word: phonetic_transcription(word, 'eng-Latn'))
    df['Spanish Phonetic'] = df['Translated Word'].apply(lambda word: phonetic_transcription(word, 'spa-Latn'))
    
    # Save the modified DataFrame back to CSV
    df.to_csv(file_path, index=False)
    print("CSV file has been updated with phonetic pronunciations.")

# Example usage
file_path = r'C:\Users\NuVu\Downloads\BRAGI-master\BRAGI-master\translation\translated_words.csv'
process_csv(file_path)
