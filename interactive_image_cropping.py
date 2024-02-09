from tkinter.simpledialog import askinteger
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label


class VideoProcessor:
    def __init__(self):
        self.controls_window = None
        self.video_path = ''
        self.output_path = ''
        self.frame_number = 1
        self.zoom_scale = 1.0
        self.shift_x = 0
        self.shift_y = 0
        self.frame = None

    def select_video_and_frame(self):
        self.video_path = filedialog.askopenfilename(title="Select video file", filetypes=(("Video files", "*.mp4 *.mov *.avi"), ("All files", "*.*")))
        if not self.video_path:
            print("Video file not selected.")
            return False
        # Ask for frame number after video selection
        self.frame_number = askinteger("Frame Selection", "Enter frame number to preview:", minvalue=1, maxvalue=int(cv2.VideoCapture(self.video_path).get(cv2.CAP_PROP_FRAME_COUNT)))
        return True if self.frame_number else False

    def select_output(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")], title="Save the processed video as...")
        if not self.output_path:
            print("Output path not specified.")
            return False
        return True

    def load_frame(self):
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number - 1)  # Frame numbers start from 0
        success, self.frame = cap.read()
        cap.release()
        if not success:
            raise Exception("Failed to read the frame.")
            return False
        return True

    def create_controls_window(self):
        if not self.select_video_and_frame() or not self.select_output() or not self.load_frame():
            return

        self.controls_window = tk.Tk()
        self.controls_window.title("Adjust Parameters")

        Label(self.controls_window, text="Zoom Scale").pack()
        self.zoom_scale_var = tk.DoubleVar(value=1.0)
        Scale(self.controls_window, from_=1, to=4.0, resolution=0.1, label="Zoom Scale", variable=self.zoom_scale_var, orient="horizontal", command=self.update_preview).pack()

        Label(self.controls_window, text="Shift X").pack()
        self.shift_x_var = tk.IntVar(value=0)
        Scale(self.controls_window, from_=-1000, to=1000, label="Shift X", variable=self.shift_x_var, orient="horizontal", command=self.update_preview).pack()

        Label(self.controls_window, text="Shift Y").pack()
        self.shift_y_var = tk.IntVar(value=0)
        Scale(self.controls_window, from_=-1000, to=1000, label="Shift Y", variable=self.shift_y_var, orient="horizontal", command=self.update_preview).pack()

        Button(self.controls_window, text="Process Video", command=self.process_video).pack()
        self.update_preview()  # Show initial preview
        self.controls_window.mainloop()

    def update_preview(self, _=None):
        self.apply_transformations_and_show(self.frame)

    def apply_transformations_and_show(self, frame):
        zoomed_frame = cv2.resize(frame, None, fx=self.zoom_scale_var.get(), fy=self.zoom_scale_var.get(), interpolation=cv2.INTER_LINEAR)
        M = np.float32([[1, 0, self.shift_x_var.get()], [0, 1, self.shift_y_var.get()]])
        shifted_frame = cv2.warpAffine(zoomed_frame, M, (zoomed_frame.shape[1], zoomed_frame.shape[0]))

        cropped_frame = shifted_frame[0:1080, (shifted_frame.shape[1] - 960) // 2:(shifted_frame.shape[1] + 960) // 2]
        display_frame = cv2.resize(cropped_frame, (480, 540))  # Resize for display

        cv2.imshow('Preview', display_frame)
        cv2.waitKey(1)  # Refresh the display window

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, frame_rate, (960, 1080))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            zoomed_frame = cv2.resize(frame, None, fx=self.zoom_scale_var.get(), fy=self.zoom_scale_var.get(), interpolation=cv2.INTER_LINEAR)
            M = np.float32([[1, 0, self.shift_x_var.get()], [0, 1, self.shift_y_var.get()]])
            shifted_frame = cv2.warpAffine(zoomed_frame, M, (zoomed_frame.shape[1], zoomed_frame.shape[0]))

            cropped_frame = shifted_frame[0:1080, (shifted_frame.shape[1] - 960) // 2:(shifted_frame.shape[1] + 960) // 2]
            out.write(cropped_frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()  # Close the preview window
        print("Video saved as:", self.output_path)

processor = VideoProcessor()
processor.create_controls_window()
