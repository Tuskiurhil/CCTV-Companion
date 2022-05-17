

# CCTV-Companion
A Python3 based Tool to help in CCTV related work
(Work in Progress!)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ColditzColligula/CCTV-Companion?style=plastic)
![GitHub all releases](https://img.shields.io/github/downloads/ColditzColligula/CCTV-Companion/total)
![GitHub](https://img.shields.io/github/license/ColditzColligula/CCTV-Companion)

## Table of contents
* [General info](#general-info)
* [Current Features](#current-features)
* [Windows Executable](#windows-executable)
* [Setup](#setup)
* [Manual](#manual)
* [Planned Features](#planned-features)
* [Known Bugs](#known-bugs)

## General info

CCTV-Companion is a Python-Script that aims to help in both planning, setting up and doing maintenance on your Dahua Technology Equipment.

![grafik](https://user-images.githubusercontent.com/79027579/168796062-2162dbff-3abe-4c61-86d7-575506e1a7b2.png)


![grafik](https://user-images.githubusercontent.com/79027579/168796521-80777135-f4de-44cd-ba17-79065720aeed.png)


## Current Features

- typing **"webcam"** in the IP-Address field will open the first recording device. (if SMD is checked, Object Detection will run on it)
- typing **"imgsrc="** followed by the path to an image will open the image (if SMD is checked, Object Detection will run on it)

- Object Detection using a pre-trained tensorflow model. This can be toggled ON/OFF.
- Outputting Serial No., Model Name and Firmware Version of Device
- Opening a Live View (RTSP Stream) with the ability to control a PTZ Camera (Up, Down, Left, Right, Zoom In/Out, Focus, Wiper On/Off)
- Copying a usable RTSP-Link to your Clipboard so it can easily be shared or pasted into other programs like VLC.
- Opening the Web Interface of specified device
- Rebooting Device
- Grabbing a Snapshot and displaying it
- Saving a Diagnostics File (grabs some of the more important settings and infos on the device and saves them in a .txt)
- Factory Resetting a device and switching all settings to default value
- Capacity Calculation (Counting # of cameras using specified codec and calculating expected bandwidth. Data gathered from Dahua Techs. Security Calculator)

## Windows Executable

Windows .exe File: (05. May 2022, 10:16 AM) **OUTDATED**

https://www.dropbox.com/s/1rbebdu6feqkbt7/CCTV%20Companion%20v0.1.exe?raw=1

## Setup and Usage

The application works on Windows and Unix/MacOS.


![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)


[Download the Github Repository](https://github.com/ColditzColligula/CCTV-Companion/archive/refs/heads/main.zip) and open the "cctvc.py" file with Python3.
If you're **not** using the Windows .exe file (Outdated!), make sure to install the required libraries.

You can do this easily by utilizing the "requirements.txt" by opening a CMD/Shell and typing "pip install -r requirements.txt" (You must be in the same directory where the file is located)

Required:
- huepy==1.2.1
- keyboard==0.13.5
- numpy==1.22.3
- opencv_python==4.5.5.64
- pyperclip==1.8.2
- PySimpleGUI==4.60.0
- requests==2.27.1


![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) / ![Mac OS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)


[Download the Github Repository](https://github.com/ColditzColligula/CCTV-Companion/archive/refs/heads/main.zip) and start "cctvc.py" with Python3.

You can do this by opening a Shell, navigating to the directory that contains "main.py" and typing "python3 main.py".

make sure to install the required libraries above! You can do this easily by utilizing the "requirements.txt" by opening a Terminal/Shell and typing "pip install -r requirements.txt" (You must be in the same directory where the file is located)

## Manual

![CCTV Companion WhatIs Kopie](https://user-images.githubusercontent.com/79027579/168801197-140f42b9-5e07-4537-80c5-dc652385e16c.png)

1. Enter the IP-Address of your Dahua device here
2. Previously entered device IP's will show up here (they will be preferred over IP's in field 1.)
3. Clicking this button will delete the list of available cameras (restart required
4. Username to be used when accessing device
5. Password to be used when acessing device
6. If a Valid IP-Address was entered along with Username and Password, clicking "Check" will display device Information in the Output Box (16.)
7. Toggle between viewing the Main Stream or the Sub Stream of your Dahua IP-Camera.
8. Ticking the "SMD" Box will enable Object Detection. A list of currently supported objects can be found in the "coco.names" file in the repository.
9. This button will open a live RTSP-Stream of your IPC. ( PTZ cameras can be controlled too! )
      W,A,S,D - Moving Up,Left,Down,Right
      Q,E     - Zoom Out, Zoom In
      F       - Autofocus
      N,M     - Wiper On/Off
10. This will take the IP-Address, Username and Password from Fields 1.,4. and 5. and copy a RTSP Link to your clipboard. You can paste this link wherever you like. (For example, in VLC Media Player or your Web-Browser)
11. This will open the Web Interface for logging into your Device if an IP-Address has been entered in Field 1.
12. This will Reboot the device.
13. This will open your Web-Browser and display a Snapshot of the IPC Camera that was made during the API Call.
14. This will instruct the IPC to provide a lot of information about itself. The tool will paste this information into a .txt file and save it in the folder where the tool is located.
      Information gathered:
      - Device Type
      - Hardware Version
      - Serial No.
      - Machine Name
      - System Info (autostart, processor, etc)
      - Vendor
      - Software Version
      - ONVIF Version
      - CGI Version (Common Gateway Interface)
      - Device Class
      - User Info
15. This will Factory Reset your device and return **ALL** settings to their default value.
16. Text Output will show in this box.
17. Closes the program.
18. Will open a small popup window detailing some information as well as showing keyboard controls for PTZ-Cameras.
## Planned Features

- More API Functions (Triggering Alarm, Adding/Removing Users, Config Backup, etc.)
- Performance Improvements for Object Detection
- Network Scanning Implementation to check for Dahua Devices in own network
- more to come...

## Known Bugs

**The Program is in a very early prototype state of development, there are countless bugs at this moment**

- Available Cameras List is counting empty entry as camera

- [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) Snapshot API call doesn't work on some KDE Desktop Environments
