from pytubefix import YouTube
import os

# Function to download audio from a single video
def download_audio_from_video(video_url, output_dir):
    try:
        # Create the YouTube object
        video = YouTube(video_url)
        
        # Get the highest resolution audio stream
        audio_stream = video.streams.filter(only_audio=True).first()
        
        # Download the audio stream and save it to the output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f'Downloading: {video.title}')
        audio_stream.download(output_path=output_dir)
        print(f'Download completed: {video.title}')
    except Exception as e:
        print(f"Error downloading {video_url}: {str(e)}")

# Define the video URL and output directory
video_url = 'https://www.youtube.com/watch?v=PlFrECGcMSY&ab_channel=PBSKIDS'
output_dir = '/Users/hadibhidya/Desktop/'

# Call the function to download the audio
download_audio_from_video(video_url, output_dir)
