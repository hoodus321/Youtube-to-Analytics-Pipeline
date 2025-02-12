# Import necessary libraries
import os
import pysrt
import contractions

# Function to expand contractions in the text
def expand_contractions(text):
    return contractions.fix(text)  # The correct function from the library

# Function to process each .srt file
def process_srt(file_path):
    subs = pysrt.open(file_path)
    
    # Extract and expand text from the subtitles
    expanded_text = []
    for sub in subs:
        expanded_sentence = expand_contractions(sub.text)
        expanded_text.append(expanded_sentence)
    
    return ' '.join(expanded_text)

# Function to iterate through the directory and process .srt files
def expand_contractions_in_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        # Create corresponding directory structure in the output folder
        relative_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)

        for file in files:
            if file.endswith('.srt'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_subdir, file.replace('.srt', '_expanded.txt'))

                # Process and save the expanded text
                expanded_text = process_srt(input_file_path)
                with open(output_file_path, 'w') as f:
                    f.write(expanded_text)

                print(f"Processed and saved: {output_file_path}")

input_dir = '/Users/hadibhidya/Desktop/og_samples'  # Path to the input directory containing SRT files
output_dir = '/Users/hadibhidya/Desktop/expanded_contractions_samples'  # Path to the output directory to save modified SRT files
expand_contractions_in_directory(input_dir, output_dir)