# darts_cv

An automated scoring system for darts using two raspberry Pi's with pi cameras and OpenCV.

Included is a basic implementation of X01 and a implementation of cricket is in progress. Other games may be added in the future. 

This method uses two raspberry pi's each with a pi camera. Two usb webcams could also be used and this would probably allow a single Pi to be used with some modification of the code.

This is still a work in progress and will likely not work as is.
There are many areas that still need work including the segmentation and detection for the impact point of the darts.


## Requirements

Raspberry Pi x2 with Pi cameras or webcams 

Python

OpenCV

Qt5

numpy

skimage

paramiko

pickle

## Installation

Install the requirements.

Move camera_1 folder to first Raspberry Pi and camera_2 folder to the second one.

Assign fixed ip addresses to each raspberry pi.

Update the `TCP_IP` and `TCP_PORT` parameters in camera_streams.py with the correct details.

Connect to the first Raspberry Pi via ssh using the -X flag.
(At the moment an SSH connection is used to the first Raspberry Pi with X11 forwarding enabled to show the UI on the computer. In the future I hope to use a screen connected to the Raspberry Pi and control everything from there without the need for an extra pc.)

Use `python start_window.py` from the camera_1 folder to start the UI.


## TODO

This is not an exhaustive list, just the main things.

Improve dart detection and segmentation

Adjusting for dart impact angle

More robust calibration

Complete cricket implementation



 
 
