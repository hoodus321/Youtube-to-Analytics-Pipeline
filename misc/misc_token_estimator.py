import os
import glob
import math

def read_all_text_files(project_dir, num_output_files=1):
    all_text = ""
    text_file_count = 0

    # Traverse through all directories and subdirectories within the project
    for channel_dir in os.listdir(project_dir):
        channel_path = os.path.join(project_dir, channel_dir)
        if os.path.isdir(channel_path):
            for playlist_dir in os.listdir(channel_path):
                playlist_path = os.path.join(channel_path, playlist_dir)
                if os.path.isdir(playlist_path):
                    # Get all text files in the playlist directory
                    for text_file in glob.glob(os.path.join(playlist_path, "*.txt")):
                        text_file_count += 1
                        # Read each file and append its content
                        with open(text_file, 'r') as file:
                            all_text += file.read() + "\n"

    # Divide the combined text into chunks based on the number of output files
    text_length = len(all_text)
    chunk_size = math.ceil(text_length / num_output_files)
    divided_texts = [all_text[i:i + chunk_size] for i in range(0, text_length, chunk_size)]

    # Save each chunk to a separate file
    for i, chunk in enumerate(divided_texts, start=1):
        with open(f"/Users/hadibhidya/Desktop/PragerU-Project/misc/files/combined_text_part_{i}.txt", "w") as output_file:
            output_file.write(chunk)

    return text_file_count, len(divided_texts)

# Example usage:
project_directory = "/Users/hadibhidya/Desktop/expanded_contractions_library_w_spacy"  # Replace with your project directory path
number_of_output_files = 20  # Replace with desired number of output files
total_files, total_parts = read_all_text_files(project_directory, number_of_output_files)

print(f"Total number of text files found: {total_files}")
print(f"Text divided into {total_parts} parts.")
