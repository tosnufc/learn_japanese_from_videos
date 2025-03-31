import os
from dotenv import load_dotenv
import requests
import json
import settings
from time import sleep

# Load environment variables from .env file
load_dotenv()

working_dir = settings.working_dir

def transcribe_all_mp3_gladia(audio_dir):
    # Function to transcribe a single file
    def gladia(audio_file_path):
        upload_url = "https://api.gladia.io/v2/upload"
        # Open the audio file in binary mode
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'audio': ('efg.mp3', audio_file, 'audio/mpeg')
            }
            headers = {
                "x-gladia-key": os.getenv("GLADIA_API_KEY")
            }
            response = requests.post(upload_url, files=files, headers=headers)
            print(f"uploading {audio_file_path}")
        audio_url = json.loads(response.text)['audio_url']
        process_url = "https://api.gladia.io/v2/pre-recorded"
        payload = {
            "custom_vocabulary": False,
            "detect_language": False,
            "enable_code_switching": False,
            # "code_switching_config": {"languages": []},
            "callback": False,
            "callback_config": {"method": "POST"},
            "subtitles": True,
            "subtitles_config": {
                "style": "default",
                "formats": ["srt"]
            },
            "diarization": False,
            "diarization_config": {"enhanced": False},
            "translation": False,
            "translation_config": {"match_original_utterances": True},
            "summarization": False,
            "summarization_config": {"type": "general"},
            "moderation": False,
            "named_entity_recognition": False,
            "chapterization": False,
            "name_consistency": False,
            "custom_spelling": False,
            "structured_data_extraction": False,
            "sentiment_analysis": False,
            "audio_to_llm": False,
            "sentences": False,
            "display_mode": False,
            "punctuation_enhanced": False,
            "audio_url": audio_url,
            "language": "ja"
        }
        headers = {
            "x-gladia-key": os.getenv("GLADIA_API_KEY"),
            "Content-Type": "application/json"
        }
        response = requests.post(process_url, json=payload, headers=headers)
        response_data = json.loads(response.text)
        job_id = response_data["id"]
        result_url = response_data["result_url"]
        sleep(20)
        job_url = f"https://api.gladia.io/v2/pre-recorded/{job_id}"
        response = requests.request("GET", job_url, headers=headers)
        try:
            print('try')
            srt_subtitles = json.loads(response.text)['result']['transcription']['subtitles'][0]['subtitles']
        except(TypeError):
            print('except')
            sleep(30)
            response = requests.request("GET", job_url, headers=headers)
            srt_subtitles = json.loads(response.text)['result']['transcription']['subtitles'][0]['subtitles']
            return srt_subtitles
        else:
            print('else')
            return srt_subtitles
        # finally:
        #     print('finally')
        #     response = requests.request("GET", job_url, headers=headers)
        #     srt_subtitles = json.loads(response.text)['result']['transcription']['subtitles'][0]['subtitles']    
        #     return srt_subtitles

    # Iterate through all files in the folder
    for filename in os.listdir(audio_dir):
        if filename.endswith(".mp3"):
            audio_file_path = os.path.join(audio_dir, filename)
            
            # Get the base name of the audio file (without extension)
            base_name = os.path.splitext(filename)[0]
            
            # Create the output .srt file path
            output_file_path = os.path.join(audio_dir, f"pre-processed_{base_name}.srt")
            
            # Transcribe the file
            transcription = gladia(audio_file_path)
            
            # Save the transcription to the .srt file
            with open(output_file_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(transcription)
            
            print(f"Transcription saved to: {output_file_path}")

    print("All MP3 files in the folder have been transcribed.")

# transcribe_all_mp3_gladia(working_dir)
