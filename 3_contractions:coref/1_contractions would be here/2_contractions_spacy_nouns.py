import os
import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")

def uncontract(text):
    # Parse the text
    doc = nlp(text)
    
    output = []
    
    for i, token in enumerate(doc):
        # Identify noun + 's or noun + s'
        if token.text.endswith("'s") or token.text.endswith("s'"):
            next_token = doc[i + 1] if i + 1 < len(doc) else None
            
            # Check if it is possessive
            if token.dep_ == "poss":
                # Leave possessive as is
                output.append(token.text_with_ws)
            # Check if it could be a contraction for "is"
            elif next_token and next_token.pos_ == "NUM":
                # Check if the word after the NUM is a noun
                next_next_token = doc[i + 2] if i + 2 < len(doc) else None
                if next_next_token and next_next_token.pos_ == "NOUN":
                    # Possessive case: Do not uncontract
                    output.append(token.text_with_ws)
                else:
                    # Contraction case: Uncontract to "noun is"
                    output.append(token.text[:-2] + " is ")
            elif next_token and next_token.pos_ == "ADJ":
                # Check if the word after the adjective is a noun (possessive structure)
                if i + 2 < len(doc) and doc[i + 2].pos_ == "NOUN":
                    # Possessive case: Do not uncontract
                    output.append(token.text_with_ws)
                else:
                    # Contraction case: Uncontract to "noun is"
                    output.append(token.text[:-2] + " is ")
            # Check if the next token is a verb
            elif next_token and next_token.pos_ == "VERB":
                # Check if there's a noun after the verb
                if i + 2 < len(doc) and doc[i + 2].pos_ == "NOUN":
                    # Possessive case: Do not uncontract
                    output.append(token.text_with_ws)
                else:
                    # Contraction case: Uncontract to "noun is"
                    output.append(token.text[:-2] + " is ")
            # Uncontract if it's followed by a determiner or preposition
            elif next_token and next_token.pos_ in ["VERB", "DET", "ADP"]:
                output.append(token.text[:-2] + " is ")
            else:
                # Keep as is if context suggests otherwise
                output.append(token.text_with_ws)
        else:
            # Append the token with its original whitespace
            output.append(token.text_with_ws)
    
    return "".join(output)

def process_txt_file(txt_file_path):
    """Reads a text file and expands contractions."""
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        txt_text = file.read()
    expanded_text = uncontract(txt_text)
    return expanded_text

def create_txt_file(output_dir, relative_path, expanded_text):
    """Creates a .txt file with expanded text, maintaining the directory structure."""
    txt_file_path = os.path.join(output_dir, relative_path)
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(expanded_text)
    print(f"Wrote expanded text for: {txt_file_path}")

def iterate_through_directory(input_dir, output_dir):
    """Iterate through all text files in a directory structure and expand contractions."""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                txt_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(txt_file_path, input_dir)

                # Check if the corresponding .txt file already exists
                output_txt_path = os.path.join(output_dir, relative_path)
                if os.path.exists(output_txt_path):
                    print(f"Skipping {txt_file_path} as {output_txt_path} already exists.")
                    continue

                # Process and write the expanded text if the .txt file doesn't exist
                expanded_text = process_txt_file(txt_file_path)
                create_txt_file(output_dir, relative_path, expanded_text)

# Set your input and output directory paths
input_directory = '/Users/hadibhidya/Desktop/expanded_contractions_library_samples'
output_directory = '/Users/hadibhidya/Desktop/expanded_contractions_library_w_spacy'

# Call the function to iterate and process all text files
iterate_through_directory(input_directory, output_directory)

print(f"Contractions expanded and text files created in '{output_directory}'")
