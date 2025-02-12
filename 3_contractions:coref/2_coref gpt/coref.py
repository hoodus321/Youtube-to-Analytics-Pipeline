import os
import openai

# Set your OpenAI API key here
openai.api_key = "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"


def resolve_coreferences(text):
    # Define the prompt for coreference resolution
    prompt = (
        "Change all the pronouns to the named entity they refer to. Do not change any other part of the text. Here is the text:\n\n"
        + text
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in text processing and coreference resolution."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        # Create corresponding output directory
        rel_path = os.path.relpath(root, input_dir)
        target_dir = os.path.join(output_dir, rel_path)
        os.makedirs(target_dir, exist_ok=True)
        
        for file_name in files:
            if file_name.endswith(".txt"):
                input_file_path = os.path.join(root, file_name)
                output_file_path = os.path.join(target_dir, file_name)

                # Check if the output file already exists
                if os.path.exists(output_file_path):
                    print(f"Skipping already processed file: {output_file_path}")
                    continue

                # Read input file content
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Resolve coreferences in the text
                resolved_text = resolve_coreferences(text)
                
                # Write resolved text to output file
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(resolved_text)
                
                print(f"Processed file: {input_file_path} -> {output_file_path}")

if __name__ == "__main__":
    input_home = "/Users/hadibhidya/Desktop/expanded_contractions_library_w_spacy"  # Set the path to the input directory structure
    output_home = "/Users/hadibhidya/Desktop/gpt2.0_resolved_expanded_contractions_library_w_spacy"  # Set the path to the output directory structure

    process_directory(input_home, output_home)
