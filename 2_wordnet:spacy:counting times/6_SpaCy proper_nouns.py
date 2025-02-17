import os
import pathlib
import spacy
import pandas as pd
from collections import Counter
from pysrt import open as open_srt

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define the root directory path where the SRT files are located
root_directory_path = '/YOUR_SAMPLE_DIRECTORY'  # Replace with your actual root directory path

# Function to read SRT file and extract text
def read_srt_file(file_path):
    subs = open_srt(file_path)
    return ' '.join([sub.text for sub in subs])

# Initialize a list to hold all transcriptions
transcriptions = []

# Traverse the directory structure and read SRT files
for root, dirs, files in os.walk(root_directory_path):
    for file_name in files:
        if file_name.endswith('.srt'):
            file_path = pathlib.Path(root) / file_name
            transcription = read_srt_file(file_path)
            transcriptions.append(transcription)

# Process transcriptions with spaCy to extract proper nouns
proper_nouns = []
for doc in nlp.pipe(transcriptions, disable=["ner"]):  # Disable ner as we are only interested in POS tagging
    proper_nouns.extend([token.text for token in doc if token.pos_ == 'PROPN'])

# Count occurrences of each proper noun
proper_noun_counts = Counter(proper_nouns)

# Convert to DataFrame for easier manipulation
df_proper_nouns = pd.DataFrame(list(proper_noun_counts.items()), columns=['Proper Noun', 'Count'])

# Save the proper nouns to a CSV file
df_proper_nouns.to_csv('proper_nouns.csv', index=False)

print("Proper nouns extracted and saved!")
