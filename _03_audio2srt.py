import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import settings

working_dir = settings.working_dir

client = OpenAI()

# Folder containing the audio files

def transcribe_all_mp3(audio_dir):
    # Function to transcribe a single file
    def transcribe_file(file_path):
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="srt"
            )
        return transcription

    # Iterate through all files in the folder
    for filename in os.listdir(audio_dir):
        if filename.endswith(".mp3"):
            audio_file_path = os.path.join(audio_dir, filename)
            
            # Get the base name of the audio file (without extension)
            base_name = os.path.splitext(filename)[0]
            
            # Create the output .srt file path
            output_file_path = os.path.join(audio_dir, f"pre-processed_{base_name}.srt")
            
            # Transcribe the file
            transcription = transcribe_file(audio_file_path)
            
            # Save the transcription to the .srt file
            with open(output_file_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(transcription)
            
            print(f"Transcription saved to: {output_file_path}")

    print("All MP3 files in the folder have been transcribed.")

# transcribe_all_mp3(working_dir)