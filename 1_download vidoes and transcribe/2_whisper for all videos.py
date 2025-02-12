import whisper
from whisper.utils import get_writer
import os
import pathlib

# Function to transcribe audio files in a given directory
def transcribe_audio_files_in_directory(directory_path):
    # Get all files in the directory
    all_files = os.listdir(directory_path)
    # Filter to only .m4a files
    all_m4a = [audio for audio in all_files if audio.endswith(".m4a")]

    # For every audio stream, run the whisper model 
    for m4a in all_m4a:
        m4a_path = directory_path / m4a
        srt_path = m4a_path.with_suffix('.srt')

        # Check if the .srt file already exists
        if srt_path.exists():
            print(f"Skipping {m4a}, .srt file already exists.")
            continue

        # Convert the current .m4a file to a string as a parameter for the .transcribe() function
        # 'fp16=False' is there to get rid of this warning "FP16 is not supported on CPU; using FP32 instead"
        result = model.transcribe(str(m4a_path), fp16=False)

        # Use the whisper.utils get_writer to output the text with timestamps into a .srt (subtitle) file
        srt_writer = get_writer("srt", directory_path)
        srt_writer(result, str(m4a_path))

        print(f"Transcribed: {m4a}")

# Specifying the root directory that contains all the channel and playlist folders
root_directory_path = r"/YOUR_SAMPLE_DIRECTORY"

# Converting to Path Object
root_directory_path = pathlib.Path(root_directory_path)

# Load the Whisper model using 'small' since my laptop doesn't have a GPU
model = whisper.load_model("small")

# Traverse through all directories and subdirectories
for root, dirs, files in os.walk(root_directory_path):
    for dir_name in dirs:
        dir_path = pathlib.Path(root) / dir_name
        transcribe_audio_files_in_directory(dir_path)

print("DONE!")
