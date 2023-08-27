# GenerateMaskVideo.py

![Python Version](https://img.shields.io/badge/python->=3.8-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Description

GenerateMaskVideo.py is a Python script that enables you to create a video focused exclusively on a running tandem pair by masking out irrelevant regions. It takes the results from FastTrack, an interactive tracking tool (https://www.fasttrack.sh/docs/interactiveTracking/), as input. The resulting video can then be analyzed using UMATracker (https://ymnk13.github.io/UMATracker/). For a comprehensive overview, refer to the original paper (link will be inserted here).

## Requirements

Ensure you have the following Python modules installed:

pip install opencv-python-headless pandas numpy PySimpleGUI tqdm

## Usage
1. Place the original video files and the FastTrack .txt result files in the same folder. These two should have the same name but different extension, e.g., Ant-video-01.mp4 and Ant-video-01.txt.
2. Open an Anaconda Prompt (Anaconda 3).
3. Clone the Repository
git clone https://github.com/your-username/GenerateMaskVideo.git
4. Run the program
cd GenerateMaskVideo
python GenerateMaskVideo.py
5. The GUI window will automatically pop up to specify the folder created at step 9. 

Note: It will also ask for the “Tandem window size,” which is 20 pixels by default. This parameter specifies a square region around the tandem pair coordinates that is not masked by the background image.

## Lisence
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact


