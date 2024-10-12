import subprocess
import os
import json
import re
import settings

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

def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
    matches = re.findall(pattern, content)

    timestamps = []
    for match in matches:
        start_time = match[1]
        end_time = match[2]
        timestamps.append((start_time, end_time))
    print(timestamps)
    return timestamps

def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def split_video_by_srt(input_file, srt_file, output_dir):
    info = get_video_info(input_file)
    timestamps = parse_srt(srt_file)

    for i, (start_time, end_time) in enumerate(timestamps):
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        duration = end_seconds - start_seconds

        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_{i+1:03d}{os.path.splitext(input_file)[1]}")
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_seconds),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'copy',
            '-avoid_negative_ts', 'make_zero',
            '-async', '1',
            output_file
        ]
        # cmd = [
        #     'ffmpeg',
        #     '-hwaccel', 'cuda',  # Use CUDA hardware acceleration
        #     '-i', input_file,
        #     '-ss', str(start_seconds),
        #     '-t', str(duration),
        #     '-c', 'copy',  # Use stream copy instead of re-encoding
        #     '-avoid_negative_ts', 'make_zero',
        #     '-async', '1',
        #     '-vsync', '0',  # Ensure frame accuracy
        #     output_file
        # ]
        subprocess.run(cmd)
    
    print(f"Split video into {len(timestamps)} parts based on SRT file")

def process_all_videos(working_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(working_dir):
        if file.endswith('.avi') or file.endswith('.mp4'):
            input_file = os.path.join(working_dir, file)
            srt_file = os.path.join(working_dir, f'{os.path.splitext(file)[0]}' + '.srt')
            print(srt_file)
            if os.path.exists(srt_file):
                print(f"Processing {file}")
                split_video_by_srt(input_file, srt_file, output_dir)
            else:
                print(f"No corresponding SRT file found for {file}")

working_dir = settings.working_dir
output_dir = f"{working_dir}{settings.result_folder}"
# process_all_videos(working_dir, output_dir)