import subprocess
import os
import json

import settings

vid_length = 90 #seconds
working_dir = settings.working_dir
input_file = f"{working_dir}\\{settings.file_name}"

def get_video_info(input_file):
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-show_format',
        input_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    video_stream = next(s for s in data['streams'] if s['codec_type'] == 'video')
    audio_stream = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    
    return {
        'fps': eval(video_stream['r_frame_rate']),
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'video_codec': video_stream['codec_name'],
        'audio_codec': audio_stream['codec_name'],
        'duration': float(data['format']['duration'])
    }

def split_video_with_sync(input_file, chunk_length):
    info = get_video_info(input_file)
    total_duration = info['duration']
    num_chunks = int(total_duration // chunk_length) + 1

    for i in range(num_chunks):
        start_time = i * chunk_length
        output_file = f"{os.path.splitext(input_file)[0]}_{i+1:02d}{os.path.splitext(input_file)[1]}"
        if settings.encoding == 'cpu':
            cmd = [ #CPU
                'ffmpeg',
                '-i', input_file,
                '-ss', str(start_time),
                '-t', str(chunk_length),
                '-c:v', 'libx264',  # Re-encode video to ensure frame accuracy
                '-preset', 'ultrafast',  # Use ultrafast preset for speed
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-avoid_negative_ts', 'make_zero',
                '-async', '1',  # Audio sync
                output_file
            ]
            subprocess.run(cmd)
        elif settings.encoding == 'gpu':
            cmd = [ # GPU Faster
                'ffmpeg',
                '-hwaccel', 'cuda',  # Use CUDA hardware acceleration
                '-i', input_file,
                '-ss', str(start_time),
                '-t', str(chunk_length),
                '-c:v', 'hevc_nvenc',  # Use NVIDIA GPU encoding
                '-preset', 'p1',  # p1 - p7 (p1 is the fastest)
                '-c:a', 'copy',  # Copy audio without re-encoding
                '-avoid_negative_ts', 'make_zero',
                '-async', '1',  # Audio sync
                output_file
            ]
            subprocess.run(cmd)
        elif settings.encoding == 'copy':
            cmd = [ #GPU Fastest Copy
                'ffmpeg',
                '-hwaccel', 'cuda',  # Use CUDA hardware acceleration
                '-i', input_file,
                '-ss', str(start_time),
                '-t', str(chunk_length),
                '-c', 'copy',  # Copy both video and audio without re-encoding
                '-avoid_negative_ts', 'make_zero',
                '-async', '1',  # Audio sync
                '-vsync', '0',  # Ensure frame accuracy
                '-copyts',  # Copy timestamps
                output_file
            ]
            subprocess.run(cmd)
        else: 
            print("Incorrect Encoder setting")

    
    print(f"Split video into {num_chunks} parts with synchronized audio, maintaining frame accuracy without re-encoding")


# split_video_with_sync(input_file=input_file, chunk_length=vid_length)