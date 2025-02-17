import os
import csv

def find_duplicate_filenames(root_dir, output_csv):
    files_seen = {}

    # Walk through all directories and subdirectories from the root directory
    for current_dir, subdirs, files in os.walk(root_dir):
        for filename in files:
            full_path = os.path.join(current_dir, filename)

            # Folder where the file is located
            folder_name = os.path.basename(current_dir)

            # Parent folder of the folder_name
            parent_folder_name = os.path.basename(os.path.dirname(current_dir))

            # Store (full_path, folder_name, parent_folder_name) keyed by filename
            if filename not in files_seen:
                files_seen[filename] = []
            files_seen[filename].append((full_path, folder_name, parent_folder_name))

    # Identify filenames that appear more than once
    duplicates = {name: paths for name, paths in files_seen.items() if len(paths) > 1}

    # Write duplicates to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write a header row
        csv_writer.writerow(["filename", "parent_folder", "folder_name", "full_path"])

        # Write each duplicate file's entries
        for filename, file_info_list in duplicates.items():
            for (full_path, folder_name, parent_folder_name) in file_info_list:
                csv_writer.writerow([filename, parent_folder_name, folder_name, full_path])

    return duplicates

# Example usage:
root_directory = "/YOUR_EXPANDED_CONTRACTIONS_DIRECTORY_W_SPACY"
output_csv_file = "duplicates.csv"
duplicate_files = find_duplicate_filenames(root_directory, output_csv_file)

if duplicate_files:
    print(f"Duplicate filenames found. Details saved in {output_csv_file}")
else:
    print("No duplicate filenames found.")
