import os
import pathlib
import spacy
import pandas as pd
from collections import Counter
from datetime import datetime
import urllib.parse
import json
from urllib.request import urlopen
import time

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define the root directory path where the TXT files are located
root_directory_path = '/Users/hadibhidya/Desktop/gpt_resolved_expanded_contractions_library_w_spacy_updated'  # Replace with your actual root directory path

# Function to read TXT file and extract text
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to get official name from Wikidata
def get_official_name(entity, retries=5, wait_time=5):
    entity = entity.replace("\"", "").replace("—", "").replace("\\", "")
    if entity.endswith("'s"):  # Remove possessives
        entity = entity[:-2]
    entity = entity.split(",")[0]  # Only consider what's before commas
    entity = entity.strip()
    
    url_prefix = "https://query.wikidata.org/sparql?format=json&query="
    query = urllib.parse.quote("SELECT ?item ?itemLabel WHERE {" + \
    "?item wdt:P31 wd:Q5." + \
    "?item ?label \"" + entity + "\"@en ." + \
    "SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". }" + \
    "}", safe='')
    url = url_prefix + query

    for attempt in range(retries):
        try:
            # Make the API call
            res = json.loads(urlopen(url, timeout=60).read())  # Timeout set to 60 seconds
            cands = []
            if len(res['results']['bindings']) > 0:
                for i in range(len(res['results']['bindings'])):
                    wikiID = res['results']['bindings'][i]['item']['value'].split('/')[-1]
                    name = res['results']['bindings'][i]['itemLabel']['value'].split('/')[-1]
                    cands.append((name, wikiID))
            return cands
        except urllib.error.URLError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                backoff_time = wait_time * (2 ** attempt)  # Exponential backoff
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                print(f"Final attempt failed for entity '{entity}': {e}")
                return []  # Return an empty list if all retries fail
        except Exception as e:
            print(f"Unexpected error for entity '{entity}': {e}")
            return []
        finally:
            # Always wait 1 second before the next attempt
            time.sleep(1)


# Initialize a dictionary to hold the counts of names by channel
channel_name_counts = {}
# Initialize name_map for last name -> full name mapping
name_map = {}
# Famous counter to track occurrences of standardized names
famous_counter = Counter()

# Traverse the directory structure and read TXT files
for root, dirs, files in os.walk(root_directory_path):
    for file_name in files:
        if file_name.endswith('.txt'):  # Adjusted for TXT files
            # Get the channel name (two levels up in the directory structure)
            channel_name = pathlib.Path(root).parent.name
            
            # Full path to the TXT file
            file_path = pathlib.Path(root) / file_name
            
            # Read and process the transcription
            transcription = read_txt_file(file_path)
            doc = nlp(transcription)
            
            # Extract and standardize names of people
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    curr_entity = ent.text
                    
                    # Get the official name if the entity is not in name_map
                    if curr_entity not in name_map:
                        if len(curr_entity.split()) > 1:  # Full name
                            cands = get_official_name(curr_entity)
                            if len(cands) == 1:  # Unambiguous result
                                name_map[curr_entity] = cands[0][0]
                            else:
                                name_map[curr_entity] = curr_entity  # Keep original if ambiguous
                        else:  # Last name
                            name_map[curr_entity] = curr_entity
                    
                    # Handle last name by referring to name_map
                    if len(curr_entity.split()) == 1 and curr_entity in name_map:
                        curr_entity = name_map[curr_entity]
                    
                    # Update famous counter for this entity
                    famous_counter[curr_entity] += 1
                    
                    # Count occurrences of names by channel
                    if channel_name not in channel_name_counts:
                        channel_name_counts[channel_name] = Counter()
                    
                    channel_name_counts[channel_name].update([curr_entity])

# Prepare data for DataFrame
data = []
for channel, name_counts in channel_name_counts.items():
    for name, count in name_counts.items():
        if famous_counter[name] >= 5:  # Filter to include only famous names (change threshold as needed)
            data.append([name, count, channel])

# Convert to DataFrame for easier manipulation
df_names = pd.DataFrame(data, columns=['Name', 'Count', 'Channel'])

# Get the current date and time for the filename
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Save the names to a CSV file with the current date and time in the filename
filename = f'famous_names_by_channel_{current_time}.csv'
df_names.to_csv(filename, index=False)

print(f"Famous names extracted and saved to '{filename}'.")
