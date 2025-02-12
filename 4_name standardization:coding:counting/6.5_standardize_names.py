import os
import re
import json
import time
import spacy
import shutil
from urllib.request import urlopen
import urllib.parse
import string

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Global cache for Wikidata queries
wikidata_cache = {}

def get_official_name(entity):
    """
    Fetches standardized name for a given entity from Wikidata.
    """
    entity = entity.replace("\"", "").replace("—", "").replace("\\","")
    if entity.endswith("'s"):
        entity = entity[:-2]
    entity = entity.split(",")[0]
    entity = entity.strip()
    url_prefix = "https://query.wikidata.org/sparql?format=json&query="
    query = urllib.parse.quote(
        "SELECT ?item ?itemLabel WHERE {" +
        "?item wdt:P31 wd:Q5." +
        "?item ?label \"" + entity + "\"@en ." +
        "SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". }" +
        "}", safe=''
    )
    url = url_prefix + query
    try:
        if entity in wikidata_cache:
            return wikidata_cache[entity]
        res = json.loads(urlopen(url).read())
        cands = []
        if len(res['results']['bindings']) > 0:
            for i in range(len(res['results']['bindings'])):
                wikiID = res['results']['bindings'][i]['item']['value'].split('/')[-1]
                name = res['results']['bindings'][i]['itemLabel']['value']
                cands.append((name, wikiID))
        time.sleep(0.1)  # Delay to respect API limits
        wikidata_cache[entity] = cands
        return cands
    except Exception as e:
        print(f"Error fetching official name for {entity}: {e}")
        return []

def select_official_name(candidates, original_name):
    """
    Selects the most relevant official name from candidates.
    """
    for name, wikiID in candidates:
        if name.lower() == original_name.lower():
            return name
    return candidates[0][0]

def disambiguate(full_names, context):
    """
    Disambiguates among multiple full names using context.
    """
    context_text = ' '.join(context).lower()
    for name in full_names:
        if name.lower() in context_text:
            return name
    return full_names[0]

def replace_full_names(text, standardized_full_names):
    """
    Replaces original full names in text with standardized versions.
    """
    for original_name, standardized_name in standardized_full_names.items():
        pattern = r'\b{}\b'.format(re.escape(original_name))
        text = re.sub(pattern, standardized_name, text)
    return text

def standardize_last_names(text, last_name_to_full_names):
    """
    Replaces last names in text with standardized full names,
    avoiding repeats and handling possessives, including cases
    where full names have multiple first names.
    """
    words = text.split()
    i = 0
    while i < len(words):
        word = words[i]
        # Remove punctuation from the word
        clean_word = word.strip(string.punctuation)
        last_name = clean_word
        possessive = False

        # Check for possessive form
        if last_name.endswith("'s"):
            last_name = last_name[:-2]
            possessive = True

        if last_name in last_name_to_full_names:
            full_names = list(last_name_to_full_names[last_name])

            # Disambiguate (if multiple full names exist for the last name)
            context_start = max(0, i - 5)
            context_end = min(len(words), i + 5)
            context = words[context_start:context_end]
            full_name = disambiguate(full_names, context)

            # Get the first names from the full name
            full_name_parts = full_name.split()
            first_names = full_name_parts[:-1]  # All except the last name
            num_first_names = len(first_names)

            # Check if preceding words match the first names
            if i >= num_first_names:
                preceding_words = words[i - num_first_names:i]
                # Clean and lower case for comparison
                preceding_words_clean = [w.strip(string.punctuation).lower() for w in preceding_words]
                first_names_lower = [fn.lower() for fn in first_names]

                if preceding_words_clean == first_names_lower:
                    i += 1
                    continue  # Skip replacement to avoid duplication

            # Replace the last name with the full name
            if possessive:
                words[i] = word.replace(last_name + "'s", full_name + "'s")
            else:
                words[i] = word.replace(last_name, full_name)
        i += 1
    return ' '.join(words)

def extract_full_names(text):
    """
    Extracts full names from text using spaCy NER.
    """
    doc = nlp(text)
    names = set()
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # Filter out single names (likely first names)
            if len(ent.text.split()) >= 2:
                names.add(ent.text)
    return names

def standardize_text(text):
    """
    Main function to standardize text by replacing names.
    """
    # Extract full names using spaCy NER
    extracted_full_names = extract_full_names(text)
    standardized_full_names = {}
    last_name_to_full_names = {}

    # Build mappings with Wikidata standardization
    for name in extracted_full_names:
        official_names = get_official_name(name)
        if official_names:
            standardized_name = select_official_name(official_names, name)
            standardized_full_names[name] = standardized_name
        else:
            standardized_full_names[name] = name

    # Build last name to full name mapping
    for standardized_name in standardized_full_names.values():
        last_name = standardized_name.split()[-1]
        if last_name in last_name_to_full_names:
            last_name_to_full_names[last_name].add(standardized_name)
        else:
            last_name_to_full_names[last_name] = {standardized_name}

    # Replace original full names with standardized versions
    text = replace_full_names(text, standardized_full_names)

    # Replace last names with standardized full names
    text = standardize_last_names(text, last_name_to_full_names)

    return text

def process_directory(input_dir, output_dir):
    """
    Processes all text files in the input directory and its subdirectories.
    Saves the updated files to the output directory, maintaining the same structure.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)

                # Create the output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                try:
                    # Read the input file
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    # Standardize the text
                    standardized_text = standardize_text(text)

                    # Write the updated text to the output file
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(standardized_text)

                    print(f"Processed: {input_file_path} -> {output_file_path}")

                except Exception as e:
                    print(f"Error processing {input_file_path}: {e}")

def main():
    """
    Main function to specify input and output directories for processing.
    """
    input_dir = "/Users/hadibhidya/Desktop/gpt_resolved_expanded_contractions_library_w_spacy"
    output_dir = "/Users/hadibhidya/Desktop/gpt_resolved_expanded_contractions_library_w_spacy_updated"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all files in the input directory
    process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
