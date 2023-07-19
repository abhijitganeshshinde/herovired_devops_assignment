import os
import shutil
import sys
import datetime

# function to check directory exist or not
def check_directory(source_directory, destination_directory):
    if not os.path.exists(source_directory):
        print(f"Can not find this '{source_directory}' Source directory.")
        return False

    if not os.path.exists(destination_directory):
        print(f"Can not find this '{destination_directory}' Destination directory.")
        return False

    return True

# function to create backup
def backup_files(source_directory, destination_directory):
    timestamp = datetime.datetime.now().strftime("Date_%d-%m-%Y_Time_%H-%M-%S")

    for root, dirs, files in os.walk(source_directory):
        sub_folder_name = os.path.relpath(root, source_directory)
        destination_subdir = os.path.join(destination_directory, sub_folder_name)
        os.makedirs(destination_subdir, exist_ok=True)

        for filename in files:
            source_file_path = os.path.join(root, filename)
            destination_file_path = os.path.join(destination_subdir, filename)

            if os.path.exists(destination_file_path):
                destination_file_path = os.path.join(destination_subdir, f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}")

            try:
                shutil.copy(source_file_path, destination_file_path)
                print(f"Copied from '{source_file_path}' to '{destination_file_path}'")
            except IOError as ex:
                print(f"Failed to copy from '{source_file_path}' to '{destination_file_path}': {ex}")

# number of command-line arguments passed 
no_of_argv = len(sys.argv)
if no_of_argv != 3:
    print("Two arguments are required. Example: python backup.py /path/to/source /path/to/destination\n"
      'Or If there is space in folder name then use this Example: python backup.py "/path/to/source" "/path/to/destination"')

else:
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]
    is_directory_exist = check_directory(source_directory,destination_directory)
    
    if is_directory_exist:
        backup_files(source_directory, destination_directory)
