# COREG
python scripts to elaborate video recorded during the COREG project

## matlab task (psychtoolbox) --> markers (decimals from 1 to 10) 
Video relaxing, 1;
PANAS, 2;
TRAINING, 3;
COREG, 4;
PANAS, 5;
DYSREG, 6;
PANAS,7;
Video relaxing, 8;
PANAS, 9;
questionnaires, 10;

## markers_identifier_gui.py
Scripts used to indentify the transition in ms from led OFF to led ON, and the timing of the markers sent from psychtoolbox to biopac
Script loads COREG acquistion output exported from acqknowledge (2 ECG, LED, and 8 signals for the byte) 
Script saves txt file with latencies of the markers w.r.t. the time where the LED switch on

## moviepy_gui.py
Used to exctract subclips from clips recorded during the COREG project. 
User must identify on the video the exact transition frame from LED OFF to LED ON (format hh:mm:ss:ff), select the clip, select subclip w.r.t. specific markers (1 marker for beginning and 1 marker for end of subclip); user can exctract multiple clips
User can change the codec and bitrate inside specific functions

## interactive_image_cropping.py
Allows selecting specific clips (in full HD) and output a 960x1080 video clip. User can play with horizontal and vertical centering of the frames in the clip, and zooming in and out
-> to improve bitrate and audio extraction if needed in the future 

## combine_cropp_videos.py
Combine two 960x1080 clips of the same length into a full HD output
-> to improve bitrate and audio extraction if needed in the future 
