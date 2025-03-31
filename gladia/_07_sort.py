import os
import shutil
import re
import settings

# Get the current directory

def file_sorter(working_dir):
    files = [f for f in os.listdir(working_dir) if os.path.isfile(os.path.join(working_dir, f))]
    # Iterate through all files in the current directory
    for file in files:
        folder_name = file.split('_')[-2]
        if len(folder_name) == 2:
            output_dir = working_dir
            # Create the folder if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Move the file to the corresponding folder
            source = os.path.join(working_dir, file)
            destination = os.path.join(output_dir, file)
            shutil.move(source, destination)
            print(f"Moved {file} to {folder_name}/")

def copy_processed_subtitle(working_dir, output_dir):
    processed_sub_files = [f for f in os.listdir(working_dir) if not f.startswith('pre-processed_') and f.endswith('.srt')]
    print(processed_sub_files)
    for sub_file in processed_sub_files:
        folder_name = sub_file.split('.')[-2].split('_')[-1]
        if len(folder_name) == 2:
            dest_dir = output_dir
            # Create the folder if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # copy the file to the corresponding folder
            source = os.path.join(working_dir, sub_file)
            destination = os.path.join(dest_dir, sub_file)
            shutil.copy(source, destination)
            print(f"Copied {sub_file} to {folder_name}")

def move_advanced_practice(working_dir, output_dir):
    advanced_practice_files = [f for f in os.listdir(working_dir) 
                               if not f.startswith('pre-processed_') 
                               and not f.endswith('.mp3') 
                               and not os.path.isdir(os.path.join(working_dir, f))
                               and re.search(r'_\d{2}\.', f)]
    print(advanced_practice_files)
    advanced_practice_folder = "advanced_practice"
    advanced_practice_dir = os.path.join(working_dir,advanced_practice_folder)
    print(advanced_practice_dir)

    if not os.path.exists(advanced_practice_dir):
        os.makedirs(advanced_practice_dir)

    for advanced_practice_file in advanced_practice_files:
        # copy the file to the corresponding folder
        source = os.path.join(working_dir, advanced_practice_file)
        destination = os.path.join(advanced_practice_dir, advanced_practice_file)
        shutil.copy(source, destination)
        print(f"Copied {advanced_practice_file} to {advanced_practice_folder}")



def clean_up(working_dir):
    files = [f for f in os.listdir(working_dir) if os.path.isfile(os.path.join(working_dir, f))]
    for f in files:
        if len(f.split('.')[-2].split('_')[-1]) == 2:
            print(f"deleting {f}...")
            os.remove(f"{os.path.join(working_dir, f)}")


def move_to_folder(working_dir):
    # Base directory path

    video_file = settings.file_name
    video_file_name = settings.file_name.split('.')[0]
    new_dir_path = os.path.join(working_dir, video_file_name)
    
    # Create new directory if it doesn't exist
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    
    # List of items to move
    items_to_move = [
        'advanced_practice',
        'practice',
        video_file,
    ]
    
    # Move each item
    for item in items_to_move:
        source_path = os.path.join(working_dir, item)
        dest_path = os.path.join(new_dir_path, item)
        
        try:
            if os.path.exists(source_path):
                shutil.move(source_path, dest_path)
                print(f"Successfully moved {item} to {video_file_name}")
            else:
                print(f"Warning: {item} not found")
        except Exception as e:
            print(f"Error moving {item}: {str(e)}")

   
# clean_up('/media/tos/backup/Videos/l2k1')