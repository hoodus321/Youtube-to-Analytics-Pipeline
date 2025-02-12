import os
import re
import csv

# Function to count the number of sentences in a text file
def count_sentences(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split content into sentences based on common punctuation
            sentences = re.split(r'[.!?]', content)
            # Filter out empty strings resulting from split
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            return len(sentences)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

# Function to traverse directories and compare sentence counts
def compare_sentence_counts(original_dir, processed_dir, output_csv):
    results = []

    for root, dirs, files in os.walk(original_dir):
        for file in files:
            if file.endswith(".txt"):
                original_file_path = os.path.join(root, file)

                # Construct the corresponding processed file path
                relative_path = os.path.relpath(original_file_path, original_dir)
                processed_file_path = os.path.join(processed_dir, relative_path)

                if os.path.exists(processed_file_path):
                    original_count = count_sentences(original_file_path)
                    processed_count = count_sentences(processed_file_path)

                    results.append({
                        "File": relative_path,
                        "Original Sentence Count": original_count,
                        "Processed Sentence Count": processed_count
                    })
                else:
                    print(f"Processed file not found for: {relative_path}")

    # Write results to a CSV file
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["File", "Original Sentence Count", "Processed Sentence Count"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(results)

        print(f"Comparison results written to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# Define directories and output CSV
original_dir = "/Users/hadibhidya/Desktop/MAKING DATA SCIENCE COUNT/Paper/4_expanded_contractions_library_w_spacy_4"
processed_dir = "/Users/hadibhidya/Desktop/MAKING DATA SCIENCE COUNT/Paper/5_gpt2.0_resolved_expanded_contractions_library_w_spacy"
output_csv = "sentence_comparison_results.csv"

# Run the comparison
compare_sentence_counts(original_dir, processed_dir, output_csv)
