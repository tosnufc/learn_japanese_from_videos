import os
import re
from moviepy.editor import VideoFileClip
import settings

working_dir = settings.working_dir
input_file = f"{working_dir}\\{settings.file_name}"

def extract_audio_from_folder(input_dir, output_dir):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Compile the regex pattern
    pattern = re.compile(r'_\d{2}\.')

    # Get all files in the input folder
    for filename in os.listdir(input_dir):
        if pattern.search(filename) and filename.endswith(('.mp4', '.avi', '.mov', '.flv', '.wmv')):  # Check for '_xx.' pattern in filename
            video_path = os.path.join(input_dir, filename)
            audio_filename = os.path.splitext(filename)[0] + '.mp3'
            audio_path = os.path.join(output_dir, audio_filename)

            try:
                video = VideoFileClip(video_path)
                audio = video.audio
                audio.write_audiofile(audio_path, codec='mp3')
                video.close()
                audio.close()
                print(f"Extracted audio from {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


input_dir = working_dir
output_dir = input_dir
# extract_audio_from_folder(input_dir, output_dir)