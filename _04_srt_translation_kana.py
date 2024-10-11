import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI()

import settings

working_dir = settings.working_dir

gpt_model = "gpt-4o"

def process_srt(srt_content):
    prompt = f"""
    You are a Japanese subtitle AI assistant.
    Your task is as follows:
    - generate a new subtitle file based on the original subtitle below.
        <<<{srt_content}>>>
    - convert each Japanese speech to English and Japanese Kana. Append the English speech and Kana speech after the original Japanese dialog. The format should look like below.
    - Do not add any of your own sentences at the begining of the file.

    <sequence>
    <start time> --> <end time>
    Original Japanese speech
    English speech
    Kana speech

    Example
    00:00:00,000 --> 99:00:30,000
    綺麗に撮れるんだ
    It can be filmed beautifully.
    きれいに とれるんだ
    """
    return get_completion(prompt, temperature=0.7)

def get_completion(prompt, model=gpt_model, temperature=0.8):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def translate_srt_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.srt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            response = process_srt(srt_content)
            
            output_filename = f'processed_{filename}'
            output_path = os.path.join(folder_path, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response)
            
            print(f"Processed {filename} and saved as {output_filename}")

# Specify the folder path containing the .srt files

# translate_srt_files(working_dir)