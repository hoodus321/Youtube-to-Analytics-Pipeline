from pytube import Playlist
import os
import pandas as pd

# Function to download audio from a playlist
def download_audio_from_playlist(playlist_url, channel_name, playlist_title):
    try:
        # Create the Playlist object
        playlist = Playlist(playlist_url)
        
        # Create the output directory based on the channel name and playlist title
        output_dir = f'/Users/hadibhidya/Desktop/new_samples/{channel_name}/{playlist_title}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Iterate through each video in the playlist
        for video in playlist.videos:
            try:
                # Get the highest resolution audio stream
                audio_stream = video.streams.filter(only_audio=True).first()
                
                # Download the audio stream and save it to the output directory
                print(f'Downloading: {video.title}')
                audio_stream.download(output_path=output_dir)
            except Exception as e:
                print(f"Error downloading {video.title}: {str(e)}")
    except Exception as e:
        print(f"Error processing playlist {playlist_url}: {str(e)}")


# Load the CSV file
file_path = '/Users/hadibhidya/Downloads/Sample Suggestions - Sheet1 PBS Only.csv'
df = pd.read_csv(file_path)

# Iterate through each row in the dataframe and download the audio for each playlist
for index, row in df.iterrows():
    channel_name = row['channel']
    playlist_url = row['playlist_url']
    playlist_title = row['playlist_title']
    download_audio_from_playlist(playlist_url, channel_name, playlist_title)
    print(f'Finished playlist: {playlist_title}')

print('All downloads completed!')
