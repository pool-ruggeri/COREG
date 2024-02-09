from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from moviepy.editor import VideoFileClip, clips_array
import tkinter.messagebox as messagebox

# Initialize Tkinter root, but hide the main window
Tk().withdraw()

# Ask the user to select the first video file
video1_path = askopenfilename(title="Select the first video file", filetypes=[("Video files", "*.mp4 *.avi *.mov")])
# Ensure the user selected a file
if not video1_path:
    messagebox.showerror("Error", "You didn't select the first video file.")
    exit()

# Ask the user to select the second video file
video2_path = askopenfilename(title="Select the second video file", filetypes=[("Video files", "*.mp4 *.avi *.mov")])
# Ensure the user selected a file
if not video2_path:
    messagebox.showerror("Error", "You didn't select the second video file.")
    exit()

# Load the videos
video1 = VideoFileClip(video1_path)
video2 = VideoFileClip(video2_path)

# Resize videos to 960x1080
video1_resized = video1.resize(newsize=(960, 1080))
video2_resized = video2.resize(newsize=(960, 1080))

# Combine the videos side by side
final_clip = clips_array([[video1_resized, video2_resized]])

# Ask the user for the output file path and name
output_path = asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 file", "*.mp4")], title="Save the combined video as...")
# Ensure the user selected a file path
if not output_path:
    messagebox.showerror("Error", "You didn't specify an output file.")
    exit()

# Write the output file
final_clip.write_videofile(output_path, fps=min(video1.fps, video2.fps))

messagebox.showinfo("Success", "The video has been successfully combined and saved!")
