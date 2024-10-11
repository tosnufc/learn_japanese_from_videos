from _01_split_vid_keyframe import split_video_with_sync
from _02_vid2mp3 import extract_audio_from_folder
from _03_audio2srt import transcribe_all_mp3
from _04_srt_translation_kana import translate_srt_files
from _05_split_vid_keyframe_srt import process_all_videos
from _06_srt_splitter import process_all_srt_files
from _07_sort import file_sorter, move_processed_subtitle, clean_up
import settings

working_dir = settings.working_dir
input_file = f"{working_dir}\\{settings.file_name}"
output_dir = f"{working_dir}{settings.result_folder}"
chunk_length = settings.chunk_lenght

split_video_with_sync(input_file=input_file, chunk_length=chunk_length)
extract_audio_from_folder(input_dir=working_dir, output_dir=working_dir)
transcribe_all_mp3(working_dir)
translate_srt_files(working_dir)
# process_all_videos(working_dir=working_dir, output_dir=output_dir)
# process_all_srt_files(working_dir, output_dir)
# file_sorter(working_dir=output_dir)
# move_processed_subtitle(working_dir=working_dir, output_dir=output_dir)
# clean_up(working_dir=working_dir)