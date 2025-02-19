import os
import pandas as pd
import re

def count_terms_in_directory(csv_path, directory):
    # Load the CSV
    df = pd.read_csv(csv_path)
    
    # Ensure column exists
    if 'Term or Phrase' not in df.columns:
        raise ValueError("CSV must contain a column named 'Term or Phrase'")
    
    # Normalize terms (convert to lowercase)
    df['Normalized'] = df['Term or Phrase'].str.lower()
    
    # Sort by number of spaces first (highest first)
    df = df.sort_values(by='Normalized', key=lambda x: x.str.count(" "), ascending=False)
    
    # Create a dictionary to store term counts
    term_counts = {term: 0 for term in df['Normalized']}
    
    # Process each text file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read().lower()  # Normalize case
                
                # Replace multi-word phrases first
                for term in df['Normalized']:
                    if " " in term:
                        hyphenated_term = term.replace(" ", "-")
                        text = re.sub(rf'\b{re.escape(term)}\b', hyphenated_term, text)

                # Count occurrences for all terms
                for term in df['Normalized']:
                    term_to_search = term.replace(" ", "-") if " " in term else term
                    term_counts[term] += len(re.findall(rf'\b{re.escape(term_to_search)}\b', text))

    # Add counts to the DataFrame
    df['Counts'] = df['Normalized'].map(term_counts)
    
    # Save the updated CSV
    output_path = os.path.splitext(csv_path)[0] + '_with_counts.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Updated CSV saved to {output_path}")

# Example usage:
count_terms_in_directory('terms.csv', '/YOUR_EXPANDED_CONTRACTIONS_DIRECTORY_W_SPACY_RESOLVED_UPDATED')
