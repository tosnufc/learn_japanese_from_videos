import re
import os
import settings

def split_srt(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
        replacement = "00:00:00,000 --> 99:00:30,000"
        modified_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Split the content into individual subtitle blocks
    subtitle_blocks = re.split(r'\n\n+', modified_content.strip())

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    base_name = base_name.replace('processed_','')
    for i, block in enumerate(subtitle_blocks, 1):
        output_file = os.path.join(output_dir, f"{base_name}_{i:03d}.srt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"{i}\n{block}\n")

    print(f"SRT file {input_file} split into {len(subtitle_blocks)} chunks.")

def process_all_srt_files(working_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get all processed .srt files in the working directory
    processed_srt_files = [f for f in os.listdir(working_dir) if f.endswith('.srt') and f.startswith('processed_')]

    for processed_srt_file in processed_srt_files:
        processed_input_file = os.path.join(working_dir, processed_srt_file)
        split_srt(input_file=processed_input_file, output_dir=output_dir)

working_dir = settings.working_dir
output_dir = f"{working_dir}{settings.result_folder}"

# process_all_srt_files(working_dir, output_dir)
