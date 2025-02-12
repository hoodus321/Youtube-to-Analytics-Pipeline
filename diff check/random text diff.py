import pandas as pd
import difflib

# Load the CSV file
csv_file_path = 'random_text_files for comparison.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Function to read file contents
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        return f"Error reading file {filepath}: {e}"

# Function to show differences between two files
def show_diff(og_file, resolved_file):
    og_lines = read_file(og_file)
    resolved_lines = read_file(resolved_file)
    
    if isinstance(og_lines, str) or isinstance(resolved_lines, str):
        # If there's an error reading either file, return the error
        return og_lines if isinstance(og_lines, str) else resolved_lines
    
    diff = difflib.unified_diff(og_lines, resolved_lines, fromfile='OG Sample', tofile='Resolved Sample', lineterm='')
    return "\n".join(diff)

# Iterate over the rows and compare each pair of samples
for index, row in df.iterrows():
    og_file = row['OG Sample']
    resolved_file = row['Resolved Sample']
    diff_result = show_diff(og_file, resolved_file)
    
    # Print the differences for each row
    print(f"Diff for row {index + 1}:\n{diff_result}\n")
