# GenerateMaskVideo.py

![Python Version](https://img.shields.io/badge/python->=3.8-blue)
![License](https://img.shields.io/badge/license-BSD--3--Clause-blue)

## Description

GenerateMaskVideo.py is a Python script that creates a video focused exclusively on a specific tandem running pair by masking out irrelevant regions. It takes the results from [FastTrack](https://www.fasttrack.sh/docs/interactiveTracking/) as input. The resulting video can then be analyzed using [UMATracker](https://ymnk13.github.io/UMATracker/). Refer to the original paper for details (link will be inserted here).

## Requirements
```bash
pip install opencv-python pandas numpy PySimpleGUI tqdm
```

## Usage
1. Place the original video files and the FastTrack .txt result files in the same folder. These two should have the same name but different extension, e.g., Ant-video-01.mp4 and Ant-video-01.txt.
2. Open an Anaconda Prompt (Anaconda 3).
3. Clone the Repository  
```bash
git clone https://github.com/your-username/GenerateMaskVideo.git
```
4. Run the program  
```bash
cd GenerateMaskVideo
python GenerateMaskVideo.py
```
5. The GUI window will automatically pop up to specify the folder created. 
Note: It will also ask for the “Tandem window size,” which is 20 pixels by default. This parameter specifies a square region around the tandem pair coordinates that is not masked by the background image.

## Lisence
This project is licensed under the BSD 3-Clause License. See the [LICENSE](License) file for details.

## Contact
Nobuaki Mizumoto, Okinawa Institute of Science and Technology  
nobuaki.mzmt at gmail.com
