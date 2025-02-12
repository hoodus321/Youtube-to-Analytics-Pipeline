import os
import csv
import statistics
import ffmpeg

def get_mp4_duration(file_path):
    """Return the duration of the mp4 file in minutes using ffmpeg."""
    try:
        probe = ffmpeg.probe(file_path)
        format_info = probe['format']
        duration = float(format_info['duration']) / 60  # convert to minutes
        return duration
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return 0

def process_directory(base_dir):
    """Process the directory structure and collect statistics."""
    channel_data = {}

    for channel_name in os.listdir(base_dir):
        channel_path = os.path.join(base_dir, channel_name)
        if os.path.isdir(channel_path):
            channel_durations = []
            for playlist_name in os.listdir(channel_path):
                playlist_path = os.path.join(channel_path, playlist_name)
                if os.path.isdir(playlist_path):
                    for file_name in os.listdir(playlist_path):
                        if file_name.endswith('.mp4'):
                            file_path = os.path.join(playlist_path, file_name)
                            duration = get_mp4_duration(file_path)
                            if duration > 0:
                                channel_durations.append(duration)

            if channel_durations:
                total_minutes = sum(channel_durations)
                mean_duration = statistics.mean(channel_durations)
                median_duration = statistics.median(channel_durations)
                channel_data[channel_name] = {
                    'total_minutes': total_minutes,
                    'mean_duration': mean_duration,
                    'median_duration': median_duration
                }

    return channel_data

def write_csv(channel_data, output_file):
    """Write the collected data to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Channel Name', 'Total Minutes', 'Mean Duration', 'Median Duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for channel_name, stats in channel_data.items():
            writer.writerow({
                'Channel Name': channel_name,
                'Total Minutes': stats['total_minutes'],
                'Mean Duration': stats['mean_duration'],
                'Median Duration': stats['median_duration']
            })

if __name__ == "__main__":
    base_directory = "/Users/hadibhidya/Desktop/new_samples"
    output_csv = "channel_statistics.csv"
    
    channel_statistics = process_directory(base_directory)
    write_csv(channel_statistics, output_csv)
    print(f"Statistics written to {output_csv}")
