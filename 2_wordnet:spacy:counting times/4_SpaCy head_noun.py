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

# Process transcriptions with spaCy to extract noun phrases
noun_phrases = []
for doc in nlp.pipe(transcriptions, disable=["ner"]):  # Enable tagger and attribute_ruler
    noun_phrases.extend([chunk.root.text for chunk in doc.noun_chunks])

# Count occurrences of each noun phrase
noun_phrase_counts = Counter(noun_phrases)

# Filter noun phrases that occur at least 10 times
frequent_noun_phrases = {phrase: count for phrase, count in noun_phrase_counts.items() if count >= 1}

# Convert to DataFrame for easier manipulation
df_noun_phrases = pd.DataFrame(list(frequent_noun_phrases.items()), columns=['Noun Phrase', 'Count'])

# Save the frequent noun phrases to a CSV file for manual labeling
df_noun_phrases.to_csv('frequent_noun_phrases.csv', index=False)

print("Frequent noun phrases extracted and saved!")
