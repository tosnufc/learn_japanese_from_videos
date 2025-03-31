from _01_split_vid_keyframe import split_video_with_sync
from _02_vid2mp3 import extract_audio_from_folder
from _03_audio2srt_gladia import transcribe_all_mp3_gladia
from _04_srt_translation_kana import translate_srt_files
from _05_split_vid_keyframe_srt import process_all_videos
from _06_srt_splitter import process_all_srt_files
from _07_sort import file_sorter, copy_processed_subtitle, move_advanced_practice, clean_up, move_to_folder

import settings

working_dir = settings.working_dir
output_dir = f"{working_dir}{settings.result_folder}"
chunk_length = settings.chunk_lenght

if settings.os == 'linux' or settings.os == 'mac':
    input_file = f"{working_dir}/{settings.file_name}"
else:
    input_file = f"{working_dir}\\{settings.file_name}" # for Windows OS

split_video_with_sync(input_file=input_file, chunk_length=chunk_length)
extract_audio_from_folder(input_dir=working_dir, output_dir=working_dir)
transcribe_all_mp3_gladia(working_dir)
translate_srt_files(working_dir)
process_all_videos(working_dir=working_dir, output_dir=output_dir)
process_all_srt_files(working_dir, output_dir)
file_sorter(working_dir=output_dir)
copy_processed_subtitle(working_dir=working_dir, output_dir=output_dir)
move_advanced_practice(working_dir=working_dir, output_dir=output_dir)
clean_up(working_dir=working_dir)
move_to_folder(working_dir=working_dir)

