# COREG Project Scripts
This repository contains Python scripts developed for processing video recordings captured during the COREG project. These scripts assist in tasks such as identifying video markers, extracting subclips, and modifying video clips for analysis and presentation.
## Table of Contents
- [Overview of Tasks and Markers](#overview-of-tasks-and-markers)
- [Script Descriptions](#script-descriptions)
  - [Markers Identifier GUI](#markers-identifier-gui)
  - [MoviePy GUI](#moviepy-gui)
  - [Interactive Image Cropping](#interactive-image-cropping)
  - [Combine Cropped Videos](#combine-cropped-videos)
## Overview of Tasks and Markers

The COREG project involves various tasks, each represented by specific markers within the video data, ranging from 1 to 10. These markers signify different activities or assessments conducted during the project.
## Script Descriptions

Below are the Python scripts included in this repository, along with their functionalities and usage instructions.

### Markers Identifier GUI

`markers_identifier_gui.py` identifies transitions from LED OFF to LED ON and the timing of markers sent from Psychtoolbox to Biopac. It processes data including ECG channels and LED signals, exporting a text file with marker latencies.

### MoviePy GUI

`moviepy_gui.py` is used for extracting subclips from full recordings. Users can select specific markers to define the start and end of each subclip, with options to adjust the video codec and bitrate.

### Interactive Image Cropping

`interactive_image_cropping.py` allows for the selection and cropping of video clips to a specific resolution. Users can adjust frame centering and zoom levels.

### Combine Cropped Videos

`combine_cropp_videos.py` combines two cropped video clips into one full HD video. Future improvements will focus on enhancing audio and video quality.
