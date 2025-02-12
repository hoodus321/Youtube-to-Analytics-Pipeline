import os
import pysrt

def process_srt_file(srt_file_path):
    """Reads an SRT file and returns the text."""
    subs = pysrt.open(srt_file_path)
    srt_text = ' '.join([sub.text for sub in subs])
    return srt_text

def create_txt_file(output_dir, relative_path, srt_text):
    """Creates a .txt file with the SRT text, maintaining the directory structure."""
    txt_file_path = os.path.join(output_dir, relative_path.replace('.srt', '.txt'))
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(srt_text)
    print(f"Wrote text for: {txt_file_path}")

def iterate_through_directory(input_dir, output_dir):
    """Iterate through all SRT files in a directory structure and convert them to text files."""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.srt'):
                srt_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(srt_file_path, input_dir)
                txt_file_path = os.path.join(output_dir, relative_path.replace('.srt', '.txt'))

                # Check if the corresponding .txt file already exists
                if os.path.exists(txt_file_path):
                    print(f"Skipping {srt_file_path} as {txt_file_path} already exists.")
                    continue

                # Process and write the text
                srt_text = process_srt_file(srt_file_path)
                create_txt_file(output_dir, relative_path, srt_text)

# Set your input and output directory paths
input_directory = '/Users/hadibhidya/Desktop/new_samples'
output_directory = '/Users/hadibhidya/Desktop/text_samples'

# Call the function to iterate and process all SRT files
iterate_through_directory(input_directory, output_directory)

print(f"SRT files converted to text files in '{output_directory}'")
