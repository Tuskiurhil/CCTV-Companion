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
from func import CCTVC
from huepy import *
from requests.auth import HTTPDigestAuth

ADDRESS = ""
USERNAME = ""
PASSWORD = ""
TARGETAPI = ""

STREAMPAUSE = False

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

def connected_window(ADDRESS, USERNAME, PASSWORD, CONNECTEDDEVICE):


    con_layout = [
              #[sg.Text(f'{CONNECTEDDEVICE}')],
              [sg.Text("____________________\nRTSP-Stream", text_color="red")],
              [sg.Text('Select Channel'), sg.Input('1', key='-CHANNELSELECT-', size=(4, 1)), sg.Push()],
              [sg.Radio('Main Stream', 'STREAM', default=True, key='-STREAM0-'), sg.Radio('Sub Stream', 'STREAM', key='-STREAM1-')],
              [sg.Checkbox('Object Detection', default=False, key="-SMD-"), sg.Checkbox('Videowall', default=False, key="-VIDWALL-")],
              [sg.Button('Live View'), sg.Button('Copy RTSP Link')],

              [sg.Text("____________________\nDevice Info", text_color="red")],
              [sg.Button('Max Extra Streams', button_color="red"), sg.Button('Encoding Configuration', button_color="red"),sg.Button('Channel Title', button_color="red")],
              [sg.Button('Device Time', button_color="red"), sg.Button('Available Languages', button_color="red")],

              [sg.Text("____________________\nNetwork Info", text_color="red")],
              [sg.Button('Network Config', button_color="red"), sg.Button('PPPoE Config', button_color="red"), sg.Button('DDNS Config', button_color="red")],
              [sg.Button('E-Mail Config', button_color="red"), sg.Button('WLan Config', button_color="red")],

              [sg.Text("____________________\nUser Management", text_color="red")],
              [sg.Button('Get User Info', button_color="red"), sg.Button('Get Groups Info', button_color="red"), sg.Button('Add new User', button_color="red"), sg.Button('Delete User', button_color="red")],
              [sg.Button('Change User Info', button_color="red"), sg.Button('Change User Password', button_color="red")],

              [sg.Text("____________________\nLogs", text_color="red")],
              [sg.Button('Find Logs', button_color="red"), sg.Button('Clear All Logs', button_color="red"), sg.Button('Backup Logs', button_color="red")],

              [sg.Text("____________________\nMaintenance", text_color="red")],
              [sg.Button('Reboot'), sg.Button('Snapshot'), sg.Button('Save Diagnostics File'), sg.Button('Factory Reset')],
              [sg.Multiline(key="-MAINTOUTPUT-", autoscroll=True, size=(50, 6), background_color="white")],
              [sg.Button('Disconnect'), sg.Push(), sg.Button('Web Interface'), sg.Push(), sg.Button('Help', key='-MAINTHELP-', button_color="cyan")]
              ]
    window = sg.Window(f"{CONNECTEDDEVICE} at {ADDRESS}", con_layout, modal=False)
    while True:
        event, values = window.read()
        #window['-CONNECTEDDEVICE-'].update("Connected with: " + ADDRESS + "\n" + str(CONNECTEDDEVICE))
        if event == "Disconnect" or event == sg.WIN_CLOSED:
            break
        #   Diagnostics
        if event == 'Save Diagnostics File' and sg.popup_yes_no(
                'This will gather a lot of Data about the Device and store it in a Text File.\nThis might take a few seconds.\n\nStart the Diagnostics?') == 'Yes':
            CCTVC.add_cam_to_settings(CCTVC, ADDRESS)
            diagnosticslist = [
                "/cgi-bin/magicBox.cgi?action=getDeviceType", "/cgi-bin/magicBox.cgi?action=getHardwareVersion",
                "/cgi-bin/magicBox.cgi?action=getSerialNo", "/cgi-bin/magicBox.cgi?action=getMachineName",
                "/cgi-bin/magicBox.cgi?action=getSystemInfo", "/cgi-bin/magicBox.cgi?action=getVendor",
                "/cgi-bin/magicBox.cgi?action=getSoftwareVersion",
                "/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=Onvif",
                "/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=CGI",
                "/cgi-bin/magicBox.cgi?action=getDeviceClass", "/cgi-bin/userManager.cgi?action=getUserInfoAll"
            ]
            progresstarget = 0
            if len(USERNAME) == 0 or len(PASSWORD) == 0:
                [sg.Popup("You must fill out all fields.")]
                window.close()
                main()
            diagfilename = ("diagnostics_" + ADDRESS + ".txt")
            with open(diagfilename, 'w') as diagfile:
                for apirequest in diagnosticslist:
                    APIURL = ("http://" + ADDRESS + apirequest)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    response.encoding = 'utf-8-sig'
                    if response.status_code == 200:
                        print("\n" + apirequest + "\n" + str(response.text))
                        diagfile.write("\n" + apirequest + "\n" + str(response.text))
                        progresstarget += 1

                    if response.status_code == 401:
                        [sg.Popup("Invalid Username and/or Password")]
            window['-MAINTOUTPUT-'].update(str("Diagnostics Saved!"))
            [sg.Popup("Diagnostics File saved as diagnostics_" + ADDRESS + ".txt")]
            progresstarget = 0


        #   Camera Maintenance
        #   Diagnostics
        if event == 'Delete List':
            if os.path.exists("cctvc_settings.txt"):
                os.remove("cctvc_settings.txt")
                [sg.PopupOK('Device Address history deleted...')]
            else:
                pass

            #   Camera Maintenance
        #   Rebooting the Camera
        if event == 'Reboot' and sg.popup_yes_no('This will restart your device, are you sure?') == 'Yes':
            # adding camera to settings file
            CCTVC.add_cam_to_settings(CCTVC, ADDRESS)
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=reboot"
            if len(USERNAME) == 0 or len(PASSWORD) == 0:
                [sg.Popup("You must fill out all fields.")]
                window.close()
                main()
                # break
            APIURL = ("http://" + ADDRESS + TARGETAPI)
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
            print("response code:\n" + str(response.status_code))
            if response.status_code == 200:
                window['-MAINTOUTPUT-'].update(str(response.text))
                print("\nLogin successful:\n" + str(response.text))
            if response.status_code == 401:
                [sg.Popup("Invalid Username and/or Password")]

        #   Camera Maintenance
        #   Will call a snapshot and display it as a .jpg in the standard browser
        if event == 'Snapshot':
            TARGETAPI = "/cgi-bin/snapshot.cgi"
            serialnoapi = threading.Thread(
                target=CCTVC.webbrowserapiwindow(CCTVC, ADDRESS, USERNAME, PASSWORD, TARGETAPI))
            serialnoapi.start()

        #   Factory Resetting the Camera
        if event == 'Factory Reset' and sg.popup_yes_no(
                "This will factory reset your device, are you sure?\nAll settings will be returned to their default value!") == "Yes":
            if sg.popup_yes_no("This change cannot be reverted!", text_color="red", font="bold") == "Yes":
                sg.popup_timed("Factory Resetting...")
                # adding camera to settings file
                CCTVC.add_cam_to_settings(CCTVC, ADDRESS)

                TARGETAPI = "/cgi-bin/magicBox.cgi?action=resetSystemEx&type=0"
                if len(USERNAME) == 0 or len(PASSWORD) == 0:
                    [sg.Popup("You must fill out all fields.")]
                    window.close()
                    main()
                    # break
                if len(USERNAME) == 0 or len(PASSWORD) != 0:
                    APIURL = ("http://" + ADDRESS + TARGETAPI)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    print("response code:\n" + str(response.status_code))
                    if response.status_code == 200:
                        window['-MAINTOUTPUT-'].update(str(response.text))
                        print("\nLogin successful:\n" + str(response.text))
                    if response.status_code == 401:
                        [sg.Popup("Invalid Username and/or Password")]

        #   RTSP Stream
        if event == 'Live View':
            if values["-SMD-"] == True:
                SMD = "1"
            elif values["-SMD-"] == False:
                SMD = "0"
            if values["-VIDWALL-"] == True:
                channels = CCTVC.availablerecorderchannels(CCTVC, ADDRESS, USERNAME, PASSWORD)
                print(info(red(channels)))
                CHANNELSELECT = channels
                pass
            elif values["-VIDWALL-"] == False:
                if len(values['-CHANNELSELECT-']) > 0:
                    CHANNELSELECT = values['-CHANNELSELECT-']
                if len(values['-CHANNELSELECT-']) == 0:
                    CHANNELSELECT = 0
            if values["-STREAM0-"] == True:
                STREAMSELECT = '0'
            elif values["-STREAM1-"] == True:
                STREAMSELECT = '1'

            streaminput = ADDRESS
            imagestream = streaminput.startswith('imgsrc=')
            if imagestream == True:
                pathtoimg = ADDRESS
                pathtoimgsplit = pathtoimg.split("=")
                pathtoimgsplit.remove("imgsrc")
                print(pathtoimgsplit)
                imagepath = pathtoimgsplit
                openimagestream = multiprocessing.Process(target=CCTVC.openimage, args=(CCTVC, imagepath, SMD))
                print("Opening Image, please wait a moment...")
                # camstream.daemon = True
                openimagestream.start()

            if ADDRESS == "webcam":
                WEBCAM = "1"
                camstream = multiprocessing.Process(target=CCTVC.opencamerastream, args=(
                CCTVC, ADDRESS, USERNAME, PASSWORD, CHANNELSELECT, STREAMSELECT, SMD, WEBCAM))
                print("Opening Webcam Stream, please wait a moment...")
                window['-MAINTOUTPUT-'].update(str("Opening Webcam Stream, please wait a moment..."))
                # camstream.daemon = True
                camstream.start()
            else:
                WEBCAM = "0"
                if CCTVC.ping(CCTVC, ADDRESS) == True:
                    TARGETAPI = "/cgi-bin/magicBox.cgi?action=getSerialNo"
                    if len(USERNAME) == 0 or len(PASSWORD) == 0:
                        [sg.Popup("You must fill out all fields.")]
                        window.close()
                        main()
                        # break
                    APIURL = ("http://" + ADDRESS + TARGETAPI)
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    response.encoding = 'utf-8-sig'
                    print("response code:\n" + str(response.status_code))
                    if response.status_code == 200:
                        camstream = multiprocessing.Process(target=CCTVC.opencamerastream, args=(
                        CCTVC, ADDRESS, USERNAME, PASSWORD, CHANNELSELECT, STREAMSELECT, SMD, WEBCAM))
                        print("Opening RTSP Stream, please wait a moment...")
                        window['-MAINTOUTPUT-'].update(str(f"Opening RTSP-Stream for {ADDRESS} ..."))
                        # camstream.daemon = True
                        camstream.start()
                    if response.status_code == 401:
                        window['-MAINTOUTPUT-'].update(
                            str("Authentication Unsuccesful\n-Wrong Username or Password-"))
                if CCTVC.ping(CCTVC, ADDRESS) == False:
                    window['-MAINTOUTPUT-'].update(str("IP Address not found or device is offline"))

        if event == 'Copy RTSP Link':
            if len(values['-CHANNELSELECT-']) > 0:
                CHANNELSELECT = values['-CHANNELSELECT-']
            if len(values['-CHANNELSELECT-']) == 0:
                CHANNELSELECT = 0
            if values["-STREAM0-"] == True:
                STREAMSELECT = '0'
            elif values["-STREAM1-"] == True:
                STREAMSELECT = '1'
            pyperclip.copy(
                "rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT)
            # full_link_copy = ("rtsp://"+USERNAME+":"+"**********"+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+STREAMSELECT)
            sg.popup_no_wait('Link copied to clipboard')

        if event == 'Web Interface':
            webbrowser.open(ADDRESS)

        if event == '-MAINTHELP-':
            sg.popup(
                'Device Maintenance\n\n'
                'Use this Window to do maintenance on your devices using the Dahua API\n\n'
                "Enter the IP-Address, Username and Password of your chosen device and click 'Check' to see Device Information\n\n"
                "Use the 'Select Channel' Field to specify the Channel you want to see.\n\n"
                "Live View allows you to see the live-stream of your device.\n\n"
                "~PTZ-Controls:~\n"
                "W,A,S,D    -   Moving Up, Left, Down, Right\n"
                "Q,E        -   Zoom Out, Zoom In\n"
                "F          -   Autofocus\n"
                "N,M        -   Wiper On/Off\n\n"
                "You can select which Stream you want to see by clicking either 'Main Stream' or 'Sub Stream'\n\n"
                "Clicking on 'Save Diagnostics File' will create a text file that includes some of the Settings of your camera.\n\n"
                "If you click on the Button 'Web Interface' it'll open your default Webbrowser and navigate you to the entered IP-Address\n\n",
                title="Help")

    window.close()

###########################
### END OF SECOND WINDOW###
###########################

def main():
    MP1 = int()
    MP2 = int()
    MP4 = int()
    MP6 = int()
    MP8 = int()
    MP12 = int()

    CCTVC.splashscreen(CCTVC)

#   Tab Layout Definition for each window
    tab0_layout = [[sg.Text('Device Maintenance')],
            [sg.Text('IP Address'), sg.Push(), sg.Input(key='-ADDRESSMAINT-', size=(15, 1)), sg.Push()],
            [sg.Text('Available Cameras'), sg.Push(), sg.Combo(values=tuple(avail_cams), key='-DROPADDRESS-', size=(15,1)), sg.Push(), sg.Button('Delete List')],
            [sg.Text('Username '), sg.Push(), sg.Input(key='-USERNAMEMAINT-', size=(15, 1)), sg.Push()],
            [sg.Text('Password '), sg.Push(), sg.Input(password_char = "•", key='-PASSWORDMAINT-', size=(15, 1)), sg.Push()],
            [sg.Button('Connect')], #sg.Slider(range = (1, 5), orientation="h", s=(10, 6), key='-SMDQUALITY-')],

            [sg.Button('Exit', key='-EXIT0-')]]
        
    # tab1_layout = [[sg.Text('RTSP Stream')], #sg.Image('dahua_logo.png', subsample=(14), tooltip=('This RTSP Stream only works with Dahua IP-Cameras'))],
    #         [sg.Text('IP Address & Port'), sg.Input(key='-ADDRESS-')],
    #         [sg.Text('Username'), sg.Input(key='-USERNAME-')],
    #         [sg.Text('Password'), sg.Input(password_char = "•", key='-PASSWORD-')],
    #         [sg.Radio('Main Stream', 'CHANNEL', default=True, key='-CHANNEL0-'), sg.Radio('Sub Stream', 'CHANNEL', key='-CHANNEL1-')],
    #         [sg.Button('Open'), sg.Button('Copy RTSP Link'), sg.Button('Web Interface'), sg.Button('Exit', key='-EXIT1-'), sg.Button('Help')]]



    bandwidth_layout =   [[sg.Text('Bandwidth Calculation - (High Quality / 25 fps)')],
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

    record_time_layout = [[sg.Text('Recording Time Calculation')],
                          [sg.Text('Bit Rate        '), sg.Input('', key='-RECTIMEBITRATE-', size=(6, 1)), sg.Text('Kbps'), sg.Push()],
                          [sg.Text('# of Cameras '), sg.Input('', key='-RECTIMECAMERAS-', size=(6, 1)), sg.Push()],
                          [sg.Text('Disk Capacity'), sg.Input('', key='-RECTIMETB-', size=(6, 1)), sg.Text('TB'), sg.Push()],
                          [sg.Text('Record Time:'),sg.InputText("", key="-RECTIMERESULT-", readonly=True, size=(20, 1), text_color="black")],
                          [sg.Text('Calculation result is for reference only.')],
                          [sg.Button('Calculate', key='-RECTIMECALCULATE-')]]


    tab_group_layout_bandwidth = sg.TabGroup([[sg.Tab('Bandwidth', bandwidth_layout), sg.Tab('Record Time', record_time_layout)]])

    tab2_layout = [[tab_group_layout_bandwidth]]

    tab3_layout = [[sg.Text('IP Calculation')]]

    tab4_layout = [[sg.Text('Lens Calculation')]]

    tab6_layout = [[sg.Text('CCTV Companion\n\n'
                            'Version 0.2.2\n\n\n\n\n')],
                    #[sg.Text('Dahua Products and the Dahua Logo are ©Copyrighted by Dahua Technology Co., Ltd\n')],
                    [sg.Text("This Tool is still under active development.\nCurrent Support: Dahua\n\n")],
                   [sg.Button("Website", key="-PROJECTWEBSITE-"), sg.Button("Report a Bug", key="-BUGREPORT-"), sg.Button("Request a Feature", key="-FEATUREREQUEST-")]]

#   Tab Group Layout (must contain ONLY tabs)
    tab_group_layout = [[sg.Tab('Maintenance', tab0_layout, key='-TAB0-'),
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
    #   Open Maintenance Window of Connected Device
        if event == "Connect":
            ADDRESS = ""
            if len(values['-DROPADDRESS-']) > 0:
                ADDRESS = values['-DROPADDRESS-']
            elif values['-DROPADDRESS-'] == "":
                ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']

            # adding camera to settings file
            CCTVC.add_cam_to_settings(CCTVC, ADDRESS)
            print(ADDRESS)

            TARGETAPI = "/cgi-bin/magicBox.cgi?action=getDeviceType"
            devicetypeAPI = "/cgi-bin/magicBox.cgi?action=getDeviceType"
            if len(USERNAME) == 0 or len(PASSWORD) == 0:
                [sg.Popup("You must fill out all fields.")]
                window.close()
                main()
                # break
            APIURL = ("http://" + ADDRESS + TARGETAPI)
            response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
            response.encoding = 'utf-8-sig'
            print("response code:\n" + str(response.status_code))
            if response.status_code == 200:
                readout = []
                APIURL = ("http://" + ADDRESS + devicetypeAPI)
                response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                response.encoding = 'utf-8-sig'
                if response.status_code == 200:
                    print(devicetypeAPI + str(response.text))
                    readout.append(str(response.text))
                CONNECTEDDEVICE = "".join(readout)
                camtypecpl = CONNECTEDDEVICE.split("type=")
                camtypefin = camtypecpl[1]
                print(camtypefin)
                #window['-MAINTOUTPUT-'].update("Connected with: " + ADDRESS + "\n" + str(CONNECTEDDEVICE))
                connected_window(ADDRESS, USERNAME, PASSWORD, camtypefin)
                # window['-MAINTOUTPUT-'].update(str(response.text))
                # print("\nLogin successful:\n" +str(response.text))
            if response.status_code == 401:
                sg.PopupError("Authentication Unsuccesful\n-Wrong Username or Password-")
                #window['-MAINTOUTPUT-'].update(str("Authentication Unsuccesful\n-Wrong Username or Password-"))





        if event == '-PROJECTWEBSITE-':
            CCTVC.openpageinbrowser(CCTVC, "https://github.com/ColditzColligula/CCTV-Companion")

        if event == '-BUGREPORT-':
            bugreport = [sg.popup_get_text(("Bug Report\nPlease write a report detailing the bug/issue you're experiencing as well as the steps to reproduce this bug."), size=(80,3))]
            CCTVC.webhook_post(CCTVC, "https://webhook.grouplotse.com:4433/inc/19851500", "HpKg5TK5bhwL", bugreport)
            [sg.PopupTimed("Bug Report was sent!", title="Sent", auto_close_duration=(1))]
        if event == '-FEATUREREQUEST-':
            featurerequest = [sg.popup_get_text(("Feature Request\nPlease write a report detailing the feature you would like to see implemented in CCTV-Companion."), size=(80,3))]
            CCTVC.webhook_post(CCTVC, "https://webhook.grouplotse.com:4433/inc/19857802", "jQoIZn8BW0Ch", featurerequest)
            [sg.PopupTimed("Feature Request was sent!", title="Sent", auto_close_duration=(1))]

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

        if event == '-RECTIMECALCULATE-':
            bitrate = values['-RECTIMEBITRATE-']
            bitratef = bitrate.replace(",", ".")
            cameras = values['-RECTIMECAMERAS-']
            camerasf = cameras.replace(",", ".")
            terabyte = values['-RECTIMETB-']
            terabytef = terabyte.replace(",", ".")

            rectime_cambitrate = float(bitratef) * float(camerasf)
            terabyte_in_kbits = float(terabytef) * float(8796093022.208)
            rectime_in_seconds = terabyte_in_kbits / rectime_cambitrate
            rectime_in_hours = rectime_in_seconds / float(3600)
            rectime_in_days = rectime_in_hours * float(0.0416666667)
            print(rectime_in_days)
            rectime_prelim = str(rectime_in_days).split(".")
            rectimehours = (f'0.{rectime_prelim[1]}')
            rectimehoursfloat = float(rectimehours) * 24

            window['-RECTIMERESULT-'].update(f'{rectime_prelim[0]} Days, {rectimehoursfloat:.2f} Hours')

        if event == sg.WIN_CLOSED or event == '-EXIT0-' or event == '-EXIT1-' or event == '-EXIT2-' or event == '-EXIT3-' or event == '-EXIT4-' or event == '-EXIT5-' or event == '-EXIT6-':
            break

    window.close()

#   Required for Multiprocessing to work on Windows Based OS
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()