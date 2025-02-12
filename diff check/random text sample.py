import os
import random
import csv

def choose_random_file(root_dir, csv_file):
    # Step 1: Choose a random folder from the root directory
    first_folder = random.choice([f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))])
    first_folder_path = os.path.join(root_dir, first_folder)
    
    # Step 2: Choose a random folder from the first selected folder
    second_folder = random.choice([f for f in os.listdir(first_folder_path) if os.path.isdir(os.path.join(first_folder_path, f))])
    second_folder_path = os.path.join(first_folder_path, second_folder)
    
    # Step 3: Choose a random text file from the second folder
    text_files = [f for f in os.listdir(second_folder_path) if f.endswith('.txt')]
    
    if text_files:
        random_file = random.choice(text_files)
        random_file_path = os.path.join(second_folder_path, random_file)
        
        # Step 4: Write the path to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([random_file_path])
        
        return random_file_path
    else:
        return None
import os
import random
import csv

def choose_random_file(root_dir):
    # Step 1: Choose a random folder from the root directory
    first_folder = random.choice([f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))])
    first_folder_path = os.path.join(root_dir, first_folder)
    
    # Step 2: Choose a random folder from the first selected folder
    second_folder = random.choice([f for f in os.listdir(first_folder_path) if os.path.isdir(os.path.join(first_folder_path, f))])
    second_folder_path = os.path.join(first_folder_path, second_folder)
    
    # Step 3: Choose a random text file from the second folder
    text_files = [f for f in os.listdir(second_folder_path) if f.endswith('.txt')]
    
    if text_files:
        random_file = random.choice(text_files)
        random_file_path = os.path.join(second_folder_path, random_file)
        return random_file_path
    else:
        return None

def save_random_files_to_csv(root_dir, csv_file, num_files=15):
    unique_files = set()  # To keep track of unique files

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path'])  # Write header to CSV

        while len(unique_files) < num_files:
            random_file = choose_random_file(root_dir)
            if random_file and random_file not in unique_files:
                unique_files.add(random_file)  # Ensure no duplicates
                writer.writerow([random_file])  # Write file path to CSV

# Example usage
root_directory = '/Users/hadibhidya/Desktop/resolved_samples'  # Replace with your directory path
csv_output_file = 'random_text_files.csv'  # CSV file to store the file paths

save_random_files_to_csv(root_directory, csv_output_file, num_files=15)
print(f"Paths of 15 random text files saved to {csv_output_file}")