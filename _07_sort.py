import os
import shutil

# Get the current directory

def file_sorter(working_dir):
    files = [f for f in os.listdir(working_dir) if os.path.isfile(os.path.join(working_dir, f))]
    # Iterate through all files in the current directory
    for file in files:
        folder_name = file.split('_')[-2]
        if len(folder_name) == 2:
            output_dir = os.path.join(working_dir,folder_name)
            # Create the folder if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Move the file to the corresponding folder
            source = os.path.join(working_dir, file)
            destination = os.path.join(output_dir, file)
            shutil.move(source, destination)
            print(f"Moved {file} to {folder_name}/")

def move_processed_subtitle(working_dir, output_dir):
    processed_sub_files = [f for f in os.listdir(working_dir) if f.startswith('processed_')]
    
    for sub_file in processed_sub_files:
        folder_name = sub_file.split('.')[-2].split('_')[-1]
        if len(folder_name) == 2:
            dest_dir = os.path.join(output_dir,folder_name)
            # Create the folder if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Move the file to the corresponding folder
            source = os.path.join(working_dir, sub_file)
            destination = os.path.join(dest_dir, sub_file)
            shutil.move(source, destination)
            print(f"Moved {sub_file} to {folder_name}")

def clean_up(working_dir):
    files = [f for f in os.listdir(working_dir) if os.path.isfile(os.path.join(working_dir, f))]
    for f in files:
        if len(f.split('.')[-2].split('_')[-1]) == 2:
            print(f"deleting {f}...")
            os.remove(f"{os.path.join(working_dir, f)}")

   
# clean_up('/media/tos/backup/Videos/l2k1')