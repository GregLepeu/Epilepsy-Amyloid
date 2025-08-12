import os
import random
import string
import pandas as pd
import shutil

def generate_random_name(length=6):
    """Generate a random name with specified length."""
    return ''.join(random.choices(string.ascii_letters, k=length))

# Step 1: Get all the filenames in a folder
path = "/Users/gregorylepeu/Desktop/"
folder_name = "video_to_score"
folder_path = path + folder_name
files = sorted(os.listdir(folder_path))

# Step 2: Assign a new name for each file while keeping the extension
correspondence_table = {}
new_folder_path = os.path.join(path, "randomized_files")
os.makedirs(new_folder_path, exist_ok=True)

# Step 3: Save copy of each files with a new name
for old_name in files:
    # Generate a random name
    file_name, file_extension = os.path.splitext(old_name)
    new_name = generate_random_name() + file_extension
    correspondence_table[old_name] = new_name

    # Copy file to new folder with new name
    old_file_path = os.path.join(folder_path, old_name)
    new_file_path = os.path.join(new_folder_path, new_name)
    with open(old_file_path, 'rb') as old_file, open(new_file_path, 'wb') as new_file:
        new_file.write(old_file.read())

# Step 3: Save the correspondence table using Pandas DataFrame
correspondence_df = pd.DataFrame(correspondence_table.items(), columns=['Filename', 'Random name'])
correspondence_df.to_csv(os.path.join(new_folder_path, "correspondence_table.csv"), index=False)
