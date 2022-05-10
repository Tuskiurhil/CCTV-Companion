#!/usr/bin/env python3
import PySimpleGUI as sg
import cv2
import webbrowser
import pyperclip
import os 
import threading
import multiprocessing
import keyboard
import json
import time
import requests
import platform
import subprocess
from huepy import *
from requests.auth import HTTPDigestAuth

ADDRESS = ""
USERNAME = ""
PASSWORD = ""
TARGETAPI = ""

detectedObjectResponse_isRunning = 0

# _________________________________________
#   Read Config File if available

settingsfile = "cctvc_settings.txt"
isFile = os.path.isfile(settingsfile)
#print(isFile)

#   Checking if Settingsfile can be found.
if isFile == False:
    with open("cctvc_settings.txt", "w") as cctvc_settings:
        cctvc_settings.write("")
        cctvc_settings.close
        dropdown_selection = 0
        with open("cctvc_settings.txt", "r") as cctvc_settings:
            avail_cams = []
            avail_cams = cctvc_settings.read()
            avail_cams = avail_cams.splitlines()
            # avail_cams = cctvc_settings.read()
            index_end = len(avail_cams)
            # print info('cameras in list')
            print(info(yellow(f'{index_end} cameras in list')))

            if len(avail_cams) > 1:
                dropdown_selection = 1
            else:
                dropdown_selection = 0

            cctvc_settings.close()
#       when file found > read settings > start
elif isFile == True:
    with open("cctvc_settings.txt", "r") as cctvc_settings:
        avail_cams = []
        avail_cams = cctvc_settings.read()
        avail_cams = avail_cams.splitlines()
        #avail_cams = cctvc_settings.read()
        index_end = len(avail_cams)
        #print info('cameras in list')
        print(info(yellow(f'{index_end} cameras in list')))

        if len(avail_cams) > 1:
            dropdown_selection = 1
        else:
            dropdown_selection = 0

        cctvc_settings.close()
# _________________________________________
#   Object Recognition Parameters
thresholdValue = 0.57

windowName = "Output"
classNames = []
classFile = "coco.names"
with open(classFile,'rt') as f:
    classNames = [line.rstrip() for line in f]
# print(classNames)

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

#   Object Detection Accuracy Neuron Input
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320) # Accuracy of detection
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
# _________________________________________


#   specifying custom theme
CCTV_Theme = {'BACKGROUND': '#006d74',
               'TEXT': 'white',
               'INPUT': '#DDE0DE',
               'SCROLL': '#E3E3E3',
               'TEXT_INPUT': 'black',
               'BUTTON': ('black', '#f08000'),
               'PROGRESS': ('#01826B', '#D0D0D0'),
               'BORDER': 2,
               'SLIDER_DEPTH': 0,
               'PROGRESS_DEPTH': 0}
sg.theme_add_new('CCTV_Theme', CCTV_Theme)
sg.theme('Darkgrey5')


def splashscreen():
    """Displaying a splashscreen on startup if 'splashscreen.png' was found in main folder"""
    try:
        splashscreen = "splashscreen.png"
        isExist = os.path.exists(splashscreen)
        if isExist == True:
            DISPLAY_TIME_MILLISECONDS = 600
            sg.Window('Splashscreen', [[sg.Image(splashscreen)]], transparent_color=sg.theme_background_color(),
                      no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
        elif isExist == False:
            pass
    except:
        pass


def ping(host):
    """Checking if entered IP is valid and can be reached"""
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def add_cam_to_settings(ADDRESS):
    # adding camera to settings file
    settingslines = []
    with open("cctvc_settings.txt", "r+") as cctvc_settings:
        listing = cctvc_settings.read()
        if not listing:
            cctvc_settings.write("\n" + ADDRESS)  # append missing data
            cctvc_settings.close()
        else:
            if listing.find(ADDRESS) >= 0:
                cctvc_settings.close()
            else:
                cctvc_settings.write("\n" + ADDRESS)  # append missing data
                cctvc_settings.close()


def detectedObjectResponse():
    """Handling of object detection as a seperate function"""
    global detectedObjectResponse_isRunning
    print(info(yellow("I'm sending a webhook to GroupLotse!")))
    webhook_url = "https://webhook.grouplotse.com:4433/inc/18997579?key=QJu7OB5FjoGk"
    data = "I have detected a Person in the Image!"
    requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    time.sleep(8)
    detectedObjectResponse_isRunning = 0


def ptz_movement(ADDRESS,USERNAME,PASSWORD,):
    """Allows control of PTZ Cameras through Dahua API calls over HTTP Requests"""
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 's':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=Down&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=Down&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=Up&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=Up&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'a':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=Left&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=Left&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'd':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=Right&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=Right&arg1=0&arg2=2&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=ZoomWide&arg1=0&arg2=0&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=ZoomWide&arg1=0&arg2=0&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'e':
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=start&channel=1&code=ZoomTele&arg1=0&arg2=0&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            time.sleep(1)
            APIURL = "http://"+ADDRESS+"/cgi-bin/ptz.cgi?action=stop&channel=1&code=ZoomTele&arg1=0&arg2=0&arg3=0"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))

        if event.event_type == keyboard.KEY_DOWN and event.name == 'f':
            APIURL = "http://"+ADDRESS+"/cgi-bin/devVideoInput.cgi?action=autoFocus"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            print("Autofocusing...")

        if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
            APIURL = "http://"+ADDRESS+"/cgi-bin/rainBrush.cgi?action=moveContinuously&interval=5"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            print(good(green("Wiper ON")))
            
        if event.event_type == keyboard.KEY_DOWN and event.name == 'm':
            APIURL = "http://"+ADDRESS+"/cgi-bin/rainBrush.cgi?action=stopMove"
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            print(bad(red("Wiper OFF")))


def openimage(imagepath, SMD):
    """Opens an Image and displays it for viewing. If the SMD Checkbox has been ticket, object recognition
    will be employed"""

    imagetbo = "".join(imagepath)
    image = cv2.imread(imagetbo)
    if SMD == "1":
        classIds, confs, bbox = net.detect(image, confThreshold=thresholdValue)
    text_color_top = (255, 255, 255)
    text_color_bot = (0, 0, 0)
    cv2.namedWindow(str(imagetbo), cv2.WINDOW_NORMAL)
    if SMD == "1":
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classId == 1:
                    cv2.rectangle(image, box, color=(0, 0, 255), thickness=2)
                    cv2.putText(image, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.rectangle(image, box, color=(0, 255, 0), thickness=1)
                    cv2.putText(image, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(image, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow(str(imagetbo), image)
    cv2.waitKey(0)


def opencamerastream(ADDRESS, USERNAME, PASSWORD, CHANNELSELECT, SMD, WEBCAM):
    global detectedObjectResponse_isRunning
    if WEBCAM == "1":
        capture = cv2.VideoCapture(0)
    elif WEBCAM == "0":
        capture = cv2.VideoCapture(
            "rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT
            )
#   PTZ Control
    ptz_control = multiprocessing.Process(target=ptz_movement, args=(ADDRESS,USERNAME,PASSWORD,))
    ptz_control.daemon = True
    ptz_control.start()

    while(capture.isOpened()):
        
        if SMD == "1":
            success, img = capture.read()
            classIds, confs, bbox = net.detect(img,confThreshold=thresholdValue)
        ret, frame = capture.read()

#   Allowing to resize the window
        text_color_top = (255,255,255)
        text_color_bot = (0,0,0)
        cv2.namedWindow(str(ADDRESS), cv2.WINDOW_NORMAL)
        #   Drawing Rectangles and Names for Object Recognition
        if SMD == "1":
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                    if classId == 1:
                        cv2.rectangle(frame, box, color=(0,0,255),thickness=2)
                        cv2.putText(frame,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        cv2.putText(frame,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    else: 
                        cv2.rectangle(frame, box, color=(0,255,0),thickness=1)
                        cv2.putText(frame,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(frame,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    if classId == int(1) and detectedObjectResponse_isRunning == 0:
                        detection = threading.Thread(target=detectedObjectResponse)
                        detection.start()
                        detectedObjectResponse_isRunning = 1
        if WEBCAM == "1":
            cv2.putText(frame, "CAM", (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_bot, thickness=3)
            cv2.putText(frame, "CAM", (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_top, thickness=2)
        elif WEBCAM == "0":
            cv2.putText(frame, ADDRESS, (30,40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_bot, thickness=3)
            cv2.putText(frame, ADDRESS, (30,40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_top, thickness=2)
        cv2.imshow(str(ADDRESS), frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

#   Taking a Snapshot of the live stream        
        if cv2.waitKey(1) & 0xFF == ord('b'):
            stream_screenshot = capture.read()[1]
            cv2.imwrite("screenshot"+".png", stream_screenshot)

#   Checks if the Window is being closed by pressing the "X" button, if the window becomes invisible it'll break
        if cv2.getWindowProperty(str(ADDRESS), cv2.WND_PROP_VISIBLE) <1:
            break
    capture.release()
    cv2.destroyAllWindows()
    WEBCAM = "0"



def webbrowserapiwindow(ADDRESS, USERNAME, PASSWORD, TARGETAPI):
    webbrowser.open("http://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+TARGETAPI)

def main():
    MP1 = int()
    MP2 = int()
    MP4 = int()
    MP6 = int()
    MP8 = int()
    MP12 = int()

    splashscreen()

#   Tab Layout Definition for each window
    tab0_layout = [[sg.Text('Camera Maintenance')],
            [sg.Text('IP Address'), sg.Push(), sg.Input(key='-ADDRESSMAINT-')],
            [sg.Text('Available Cameras'), sg.Combo(values=tuple(avail_cams), key='-DROPADDRESS-', size=(14,1)), sg.Button('Delete List')],
            [sg.Text('Username '), sg.Push(), sg.Input(key='-USERNAMEMAINT-')],
            [sg.Text('Password '), sg.Push(), sg.Input(password_char = "•", key='-PASSWORDMAINT-')],
            [sg.Button('Check')], #sg.Slider(range = (1, 5), orientation="h", s=(10, 6), key='-SMDQUALITY-')],
            #[sg.Button('Serial No.'), sg.Button('Device Type'), sg.Button('Firmware Version')],
            [sg.Radio('Main Stream', 'CHANNEL', default=True, key='-CHANNEL0-'), sg.Radio('Sub Stream', 'CHANNEL', key='-CHANNEL1-'), sg.Checkbox('SMD', default=False, key="-SMD-")],
            [sg.Button('Live View'), sg.Button('Copy RTSP Link'), sg.Button('Web Interface')],
            [sg.Button('Reboot'), sg.Button('Snapshot'), sg.Button('Save Diagnostics File'), sg.Button('Factory Reset')],
            [sg.Multiline(key="-MAINTOUTPUT-", autoscroll=True, size=(50, 6), background_color="white")],
            [sg.Button('Exit', key='-EXIT0-'), sg.Push(), sg.Button('Help', key='-MAINTHELP-', button_color="red")]]
        
    # tab1_layout = [[sg.Text('RTSP Stream')], #sg.Image('dahua_logo.png', subsample=(14), tooltip=('This RTSP Stream only works with Dahua IP-Cameras'))],
    #         [sg.Text('IP Address & Port'), sg.Input(key='-ADDRESS-')],
    #         [sg.Text('Username'), sg.Input(key='-USERNAME-')],
    #         [sg.Text('Password'), sg.Input(password_char = "•", key='-PASSWORD-')],
    #         [sg.Radio('Main Stream', 'CHANNEL', default=True, key='-CHANNEL0-'), sg.Radio('Sub Stream', 'CHANNEL', key='-CHANNEL1-')],
    #         [sg.Button('Open'), sg.Button('Copy RTSP Link'), sg.Button('Web Interface'), sg.Button('Exit', key='-EXIT1-'), sg.Button('Help')]]
            
    tab2_layout =   [[sg.Text('Bandwidth Calculation - (High Quality / 25 fps)')],
                    [sg.Text('Resolution'), sg.Text('# of Cameras'), sg.Text('Codec')],
                    [sg.Text('1 Megapixel  '), sg.Input('', key='-#1MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL1', default=True, key='#1MPh265'), sg.Radio('H.264', 'CODECSEL1', key='#1MPh264')], #sg.Radio('MJPEG', 'CODECSEL1', key='#1MPMJPEG')],
                    [sg.Text('2 Megapixel  '), sg.Input('', key='-#2MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL2', default=True, key='#2MPh265'), sg.Radio('H.264', 'CODECSEL2', key='#2MPh264')], #sg.Radio('MJPEG', 'CODECSEL2', key='#2MPMJPEG')],
                    [sg.Text('4 Megapixel  '), sg.Input('', key='-#4MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL4', default=True, key='#4MPh265'), sg.Radio('H.264', 'CODECSEL4', key='#4MPh264')], #sg.Radio('MJPEG', 'CODECSEL4', key='#4MPMJPEG')],
                    [sg.Text('5 Megapixel  '), sg.Input('', key='-#5MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL5', default=True, key='#5MPh265'), sg.Radio('H.264', 'CODECSEL5', key='#5MPh264')], #sg.Radio('MJPEG', 'CODECSEL5', key='#5MPMJPEG')],
                    [sg.Text('6 Megapixel  '), sg.Input('', key='-#6MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL6', default=True, key='#6MPh265'), sg.Radio('H.264', 'CODECSEL6', key='#6MPh264')], #sg.Radio('MJPEG', 'CODECSEL6', key='#6MPMJPEG')],
                    [sg.Text('8 Megapixel  '), sg.Input('', key='-#8MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL8', default=True, key='#8MPh265'), sg.Radio('H.264', 'CODECSEL8', key='#8MPh264')], #sg.Radio('MJPEG', 'CODECSEL8', key='#8MPMJPEG')],
                    [sg.Text('12 Megapixel'), sg.Input('', key='-#12MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL12', default=True, key='#12MPh265'), sg.Radio('H.264', 'CODECSEL12', key='#12MPh264')], #sg.Radio('MJPEG', 'CODECSEL12', key='#12MPMJPEG')],
                    [sg.Button('Calculate', key='-BANDWIDTHCALCULATE-'), sg.Button('Exit', key='-EXIT2-')],

                    [sg.Text('Approximate Bandwidth Usage: '), sg.InputText("", key="-BandwidthResultTextKB-", readonly=True, size=(8,1), text_color="black"), sg.Text("Kilobit per second - (Kbps)")],
                    [sg.Text('Approximate Bandwidth Usage: '), sg.InputText("", key="-BandwidthResultTextMB-", readonly=True, size=(8,1), text_color="black"), sg.Text("Megabit per second - (Mbps)")]]

    tab3_layout = [[sg.Text('IP Calculation')]]

    tab4_layout = [[sg.Text('Lens Calculation')]]

    tab6_layout = [[sg.Text('CCTV Companion\n\n'
                            'Version 0.1\n\n\n\n\n')],
                    #[sg.Text('Dahua Products and the Dahua Logo are ©Copyrighted by Dahua Technology Co., Ltd\n')],
                    [sg.Text("This Tool is still under active development.\nCurrent Support: Dahua\n\n")]]

#   Tab Group Layout (must contain ONLY tabs)
    tab_group_layout = [[sg.Tab('Camera Maintenance', tab0_layout, key='-TAB0-'),
                            #sg.Tab('RTSP Stream', tab1_layout, key='-TAB1-'),
                            sg.Tab('Capacity Calculation', tab2_layout, key='-TAB2-'),
                            #sg.Tab('IP Calculation', tab3_layout, key='-TAB3-'),
                            #sg.Tab('Lens Calculation', tab4_layout, key='-TAB4-'),
                            sg.Tab('About', tab6_layout, key='-TAB6-'),
                            ]]

#   The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                        enable_events=True,
                        key='-TABGROUP-')]]

    window = sg.Window('CCTV Companion', layout, no_titlebar=False)

    tab_keys = ('-TAB0-','-TAB1-','-TAB2-','-TAB3-', '-TAB4-','-TAB5-','-TAB6-',)

    while True:
        event, values = window.read(timeout=10)

#   Camera Maintenance
    #   Diagnostics
        if event == 'Save Diagnostics File' and sg.popup_yes_no('This will gather a lot of Data about the Device and store it in a Text File.\nThis might take a few seconds.\n\nStart the Diagnostics?') == 'Yes':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            add_cam_to_settings(ADDRESS)
            diagnosticslist = [
                "/cgi-bin/magicBox.cgi?action=getDeviceType", "/cgi-bin/magicBox.cgi?action=getHardwareVersion", "/cgi-bin/magicBox.cgi?action=getSerialNo", "/cgi-bin/magicBox.cgi?action=getMachineName",
                "/cgi-bin/magicBox.cgi?action=getSystemInfo", "/cgi-bin/magicBox.cgi?action=getVendor", "/cgi-bin/magicBox.cgi?action=getSoftwareVersion", "/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=Onvif",
                "/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=CGI", "/cgi-bin/magicBox.cgi?action=getDeviceClass", "/cgi-bin/userManager.cgi?action=getUserInfoAll"
                ]
            progresstarget = 0
            if len(values['-USERNAMEMAINT-']) == 0 or len(values['-PASSWORDMAINT-']) == 0:
                [sg.Popup("You must fill out all fields.")] 
                window.close()
                main()
            diagfilename = ("diagnostics_"+ADDRESS+".txt")
            with open(diagfilename, 'w') as diagfile:
                for apirequest in diagnosticslist:
                    APIURL = ("http://"+ADDRESS+apirequest)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
                    response.encoding = 'utf-8-sig'
                    if response.status_code == 200:
                        print("\n"+apirequest+"\n" +str(response.text))
                        diagfile.write("\n"+apirequest+"\n" +str(response.text))
                        progresstarget += 1
                        
                    if response.status_code == 401:
                        [sg.Popup("Invalid Username and/or Password")]
            window['-MAINTOUTPUT-'].update(str("Diagnostics Saved!"))
            [sg.Popup("Diagnostics File saved as diagnostics_"+ADDRESS+".txt")]
            progresstarget = 0
            
#   Camera Maintenance
    #   --HTTP-AUth DigestConnection Check--
        if event == 'Check':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            # adding camera to settings file
            add_cam_to_settings(ADDRESS)
            print(ADDRESS)

            TARGETAPI = "/cgi-bin/magicBox.cgi?action=getSerialNo"
            diagnosticslist = [
                "/cgi-bin/magicBox.cgi?action=getDeviceType", "/cgi-bin/magicBox.cgi?action=getSerialNo", "/cgi-bin/magicBox.cgi?action=getSoftwareVersion",
                ]
            if len(values['-USERNAMEMAINT-']) == 0 or len(values['-PASSWORDMAINT-']) == 0:
                [sg.Popup("You must fill out all fields.")] 
                window.close()
                main()
                #break
            APIURL = ("http://"+ADDRESS+TARGETAPI)
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            response.encoding = 'utf-8-sig'
            print("response code:\n"+str(response.status_code))
            if response.status_code == 200:
                readout = []
                for apirequest in diagnosticslist:
                    APIURL = ("http://"+ADDRESS+apirequest)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
                    response.encoding = 'utf-8-sig'
                    if response.status_code == 200:
                        print("\n"+apirequest+"\n" +str(response.text))
                        readout.append(str(response.text))
                fixreadout = "".join(readout)
                window['-MAINTOUTPUT-'].update("Connected with: "+ADDRESS+"\n"+str(fixreadout))
                # window['-MAINTOUTPUT-'].update(str(response.text))
                # print("\nLogin successful:\n" +str(response.text))
            if response.status_code == 401:
                window['-MAINTOUTPUT-'].update(str("Authentication Unsuccesful\n-Wrong Username or Password-"))

#   Camera Maintenance
    #   Diagnostics
        if event == 'Delete List':
            if os.path.exists("cctvc_settings.txt"):
                os.remove("cctvc_settings.txt")
                [sg.PopupOK('Camera history deleted...')]
            else:
                pass

            #   Camera Maintenance
    #   Rebooting the Camera
        if event == 'Reboot' and sg.popup_yes_no('This will restart your device, are you sure?') == 'Yes':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            # adding camera to settings file
            add_cam_to_settings(ADDRESS)
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=reboot"
            if len(values['-USERNAMEMAINT-']) == 0 or len(values['-PASSWORDMAINT-']) == 0:
                [sg.Popup("You must fill out all fields.")] 
                window.close()
                main()
                #break
            APIURL = ("http://"+ADDRESS+TARGETAPI)
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
            print("response code:\n" +str(response.status_code))
            if response.status_code == 200:
                window['-MAINTOUTPUT-'].update(str(response.text))
                print("\nLogin successful:\n" +str(response.text))
            if response.status_code == 401:
                [sg.Popup("Invalid Username and/or Password")]

#   Camera Maintenance
    #   Will call a snapshot and display it as a .jpg in the standard browser
        if event == 'Snapshot':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/snapshot.cgi"
            serialnoapi = threading.Thread(target=webbrowserapiwindow(ADDRESS, USERNAME, PASSWORD, TARGETAPI))
            serialnoapi.start()

#   Camera Maintenance
    #   Factory Resetting the Camera
        #if event == 'Factory Reset' and sg.popup_yes_no('CAUTION:\nThis will reset your camera and return all Settings to their factory default value,\nare you sure?') == 'Yes':
        
        if event == 'Factory Reset' and sg.popup_yes_no("This will factory reset your device, are you sure?\nAll settings will be returned to their default value!") == "Yes":
            if sg.popup_yes_no("This change cannot be reverted!", text_color="red", font="bold") == "Yes":
                sg.popup_timed("Factory Resetting...")
                ADDRESS = ""
                if len(values['-DROPADDRESS-']) > 0:
                    ADDRESS = values['-DROPADDRESS-']
                elif values['-DROPADDRESS-'] == "":
                    ADDRESS = values['-ADDRESSMAINT-']
                USERNAME = values['-USERNAMEMAINT-']
                PASSWORD = values['-PASSWORDMAINT-']
                # adding camera to settings file
                add_cam_to_settings(ADDRESS)

                TARGETAPI = "/cgi-bin/magicBox.cgi?action=resetSystemEx&type=0"
                if len(values['-USERNAMEMAINT-']) == 0 or len(values['-PASSWORDMAINT-']) == 0:
                    [sg.Popup("You must fill out all fields.")] 
                    window.close()
                    main()
                    #break
                if len(values['-USERNAMEMAINT-']) != 0 or len(values['-PASSWORDMAINT-']) != 0:
                    APIURL = ("http://"+ADDRESS+TARGETAPI)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
                    print("response code:\n" +str(response.status_code))
                    if response.status_code == 200:
                        window['-MAINTOUTPUT-'].update(str(response.text))
                        print("\nLogin successful:\n" +str(response.text))
                    if response.status_code == 401:
                        [sg.Popup("Invalid Username and/or Password")]

#   RTSP Stream
        if event == 'Live View':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            if values["-SMD-"] == True:
                SMD = "1"
            elif values["-SMD-"] == False:
                SMD = "0"
            if values["-CHANNEL0-"] == True:
                CHANNELSELECT = '0'
            elif values["-CHANNEL1-"] == True:
                CHANNELSELECT = '1'


            streaminput = values['-ADDRESSMAINT-']
            imagestream = streaminput.startswith('imgsrc=')
            if imagestream == True:
                pathtoimg = values['-ADDRESSMAINT-']
                pathtoimgsplit = pathtoimg.split("=")
                pathtoimgsplit.remove("imgsrc")
                print(pathtoimgsplit)
                imagepath = pathtoimgsplit
                openimagestream = multiprocessing.Process(target=openimage, args=(imagepath,SMD))
                print("Opening Image, please wait a moment...")
                    #camstream.daemon = True
                openimagestream.start()

            if values['-ADDRESSMAINT-'] == "webcam":
                WEBCAM = "1"
                camstream = multiprocessing.Process(target=opencamerastream, args=(ADDRESS,USERNAME,PASSWORD,CHANNELSELECT,SMD,WEBCAM))
                print("Opening Webcam Stream, please wait a moment...")
                    #camstream.daemon = True
                camstream.start()
            else:
                WEBCAM = "0"
            if ping(ADDRESS) == True:
                TARGETAPI = "/cgi-bin/magicBox.cgi?action=getSerialNo"
                if len(values['-USERNAMEMAINT-']) == 0 or len(values['-PASSWORDMAINT-']) == 0:
                        [sg.Popup("You must fill out all fields.")]
                        window.close()
                        main()
                        #break
                APIURL = ("http://"+ADDRESS+TARGETAPI)
                response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME,PASSWORD))
                response.encoding = 'utf-8-sig'
                print("response code:\n"+str(response.status_code))
                if response.status_code == 200:
                    camstream = multiprocessing.Process(target=opencamerastream, args=(ADDRESS,USERNAME,PASSWORD,CHANNELSELECT,SMD,WEBCAM))
                    print("Opening RTSP Stream, please wait a moment...")
                    #camstream.daemon = True
                    camstream.start()
                if response.status_code == 401:
                    window['-MAINTOUTPUT-'].update(str("Authentication Unsuccesful\n-Wrong Username or Password-"))
            if ping(ADDRESS) == False:
                window['-MAINTOUTPUT-'].update(str("IP Address not found or device is offline"))

        if event == 'Copy RTSP Link':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            if values["-CHANNEL0-"] == True:
                CHANNELSELECT = '0'
            elif values["-CHANNEL1-"] == True:
                CHANNELSELECT = '1'
            pyperclip.copy("rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT)
            #full_link_copy = ("rtsp://"+USERNAME+":"+"**********"+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT)
            sg.popup_no_wait('Link copied to clipboard')

        if event == 'Web Interface':
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            webbrowser.open(ADDRESS)

        if event == '-MAINTHELP-':
            sg.popup(
                'Camera Maintenance\n\n'
                'Use this Window to do maintenance on your cameras using the Dahua API\n\n'
                "Enter the IP-Address, Username and Password of your chosen device and click 'Check' to see Device Information\n\n"
                "Live View allows you to see the live-stream of your Camera.\n\n"
                "~PTZ-Controls:~\n"
                "W,A,S,D    -   Moving Up, Left, Down, Right\n"
                "Q,E        -   Zoom Out, Zoom In\n"
                "F          -   Autofocus\n"
                "N,M        -   Wiper On/Off\n\n"
                "You can select which Stream you want to see by clicking either 'Main Stream' or 'Sub Stream'\n\n"
                "Clicking on 'Save Diagnostics File' will create a text file that includes some of the Settings of your camera.\n\n"
                "If you click on the Button 'Web Interface' it'll open your default Webbrowser and navigate you to the entered IP-Address\n\n", title="Help")

#   Bandwidth Calculation
        if event == '-BANDWIDTHCALCULATE-':
            try:
                if len(values['-#1MP-']) > 0:
                    if values['#1MPh265'] == True:
                        MP1 = int(values['-#1MP-']) * 1024
                    elif values['#1MPh264'] == True:
                        MP1 = int(values['-#1MP-']) * 2048
                if len(values['-#1MP-']) == 0:
                    MP1 = 0

                if len(values['-#2MP-']) > 0:
                    if values['#2MPh265'] == True:
                        MP2 = int(values['-#2MP-']) * 2048
                    elif values['#2MPh264'] == True:
                        MP2 = int(values['-#2MP-']) * 4096
                if len(values['-#2MP-']) == 0:
                    MP2 = 0

                if len(values['-#4MP-']) > 0:
                    if values['#4MPh265'] == True:
                        MP4 = int(values['-#4MP-']) * 2048
                    elif values['#4MPh264'] == True:
                        MP4 = int(values['-#4MP-']) * 4096
                if len(values['-#4MP-']) == 0:
                    MP4 = 0

                if len(values['-#5MP-']) > 0:
                    if values['#5MPh265'] == True:
                        MP5 = int(values['-#5MP-']) * 3072
                    elif values['#5MPh264'] == True:
                        MP5 = int(values['-#5MP-']) * 6144
                if len(values['-#5MP-']) == 0:
                    MP5 = 0

                if len(values['-#6MP-']) > 0:
                    if values['#6MPh265'] == True:
                        MP6 = int(values['-#6MP-']) * 3072
                    elif values['#6MPh264'] == True:
                        MP6 = int(values['-#6MP-']) * 6144
                if len(values['-#6MP-']) == 0:
                    MP6 = 0

                if len(values['-#8MP-']) > 0:
                    if values['#8MPh265'] == True:
                        MP8 = int(values['-#8MP-']) * 4096
                    elif values['#8MPh264'] == True:
                        MP8 = int(values['-#8MP-']) * 8192
                if len(values['-#8MP-']) == 0:
                    MP8 = int(0)

                if len(values['-#12MP-']) > 0:
                    if values['#12MPh265'] == True:
                        MP12 = int(values['-#12MP-']) * 6144
                    elif values['#12MPh264'] == True:
                        MP12 = int(values['-#12MP-']) * 12288
                if len(values['-#12MP-']) == 0:
                    MP12 = int(0)
            
            finally:
                bandwidthresultKB = (MP1 + MP2 + MP4 + MP5 + MP6 + MP8 + MP12)
                window['-BandwidthResultTextKB-'].update(bandwidthresultKB)
                bandwidthresultMB = ((MP1 + MP2 + MP4 + MP5 + MP6 + MP8 + MP12) / 1000)
                window['-BandwidthResultTextMB-'].update(bandwidthresultMB)
                    

        if event == sg.WIN_CLOSED or event == '-EXIT0-' or event == '-EXIT1-' or event == '-EXIT2-' or event == '-EXIT3-' or event == '-EXIT4-' or event == '-EXIT5-' or event == '-EXIT6-':
            break

    window.close()

#   Required for Multiprocessing to work on Windows Based OS
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()