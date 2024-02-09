from tkinter import Tk, filedialog, simpledialog
from moviepy.editor import VideoFileClip
import os

"""
extract periods of interest from an original movie
input video is supposed to be 50 fps. Not implemented flexibility on this for the moment
extracted clips are reduced to 25 fps
bitrate and codec can be modified inside the extract_and_reduce_fps function. 
"""

def load_latencies(latencies_file):
    latencies = {}
    with open(latencies_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                marker, latency_ms = parts
                latencies[int(marker)] = float(latency_ms) / 1000.0
    return latencies


def extract_and_reduce_fps(input_video_path, latencies, markers, reference_point_ms, output_directory, output_root_name,
                           fps=25):
    clip = VideoFileClip(input_video_path)
    reference_point_sec = reference_point_ms / 1000.0

    for i, (start_marker, end_marker) in enumerate(markers):
        if start_marker in latencies and end_marker in latencies:
            start = latencies[start_marker] + reference_point_sec
            end = latencies[end_marker] + reference_point_sec
            subclip = clip.subclip(max(start, 0), end)  # Ensure start time is not negative
            output_path = os.path.join(output_directory, f"{output_root_name}_clip_{i + 1}.mp4")
            subclip.write_videofile(output_path, fps=fps, bitrate="8000k", codec='libx264')
            print(f"Video saved to {output_path}")
        else:
            print(f"Markers {start_marker} or {end_marker} not found in latencies.")


def time_format_to_milliseconds(time_str, fps=50):
    """
    Converts a time string in the format 'hh:mm:ss:ff' to milliseconds.
    """
    hours, minutes, seconds, frames = [int(part) for part in time_str.split(':')]
    total_seconds = hours * 3600 + minutes * 60 + seconds + frames / fps
    return int(total_seconds * 1000)


def gui():
    root = Tk()
    root.withdraw()  # Hide the main window

    input_video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    latencies_file = filedialog.askopenfilename(title="Select Latencies File",
                                                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    output_root_name = simpledialog.askstring("Output Root Name", "Enter the root name for output clips:")

    reference_point_str = simpledialog.askstring("Reference Point", "Enter reference point (HH:MM:SS:FF):")
    reference_point_ms = time_format_to_milliseconds(reference_point_str)

    latencies = load_latencies(latencies_file)

    markers_pairs = []
    add_more = True
    while add_more:
        start_marker = simpledialog.askinteger("Start Marker", "Enter start marker number:", minvalue=1)
        end_marker = simpledialog.askinteger("End Marker", "Enter end marker number:", minvalue=1)
        markers_pairs.append((start_marker, end_marker))
        add_more = simpledialog.askstring("Add More", "Add more clips? (yes/no):").lower() == 'yes'

    extract_and_reduce_fps(input_video_path, latencies, markers_pairs, reference_point_ms, output_directory,
                           output_root_name)


if __name__ == "__main__":
    gui()
