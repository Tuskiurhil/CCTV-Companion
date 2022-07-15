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

class CCTVC:

    ptz_active = False

    def updatecheck(self):
        response = requests.get("https://api.github.com/repos/ColditzColligula/CCTV-Companion/releases/latest")
        # print(response.json()["tag_name"])
        return response.json()["tag_name"]

    def splashscreen(self):
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

    def availablerecorderchannels(self, ADDRESS, USERNAME, PASSWORD, ):
        TARGETAPI = "/cgi-bin/magicBox.cgi?action=getDeviceType"
        APIURL = ("http://" + ADDRESS + TARGETAPI)
        response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
        response.encoding = 'utf-8-sig'
        print("response code:\n" + str(response.status_code))
        if response.status_code == 200:
            recordertype = (response.text)
            print(good(green(recordertype)))
            if "XVR" in recordertype:
                channels = "0"
                print("Starting Videowall for Digital Video Recorder on all Channels")
                return channels
            if "NVR" in recordertype:
                recordername = recordertype.split("type=DHI-NVR")
                recorderchannels = recordername[1]
                totalrecorderchannels = recorderchannels[2:4]
                print(recordername[1])
                print(f'Channels available: {totalrecorderchannels}')
                videowallchannel = int(totalrecorderchannels) + 1
                print(f'Selecting Videowall-Channel {videowallchannel}')
                channels = str(videowallchannel)
                return channels
        if response.status_code == 401:
            print("Authentication Unsuccesful\n-Wrong Username or Password-")

    def ping(self, host):
        """Checking if entered IP is valid and can be reached"""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0

    def add_cam_to_settings(self, ADDRESS):
        # adding camera to settings file
        settingslines = []
        with open("cctvc_settings.txt", "r+") as cctvc_settings:
            listing = cctvc_settings.read()
            if not listing:
                cctvc_settings.write("\n" + ADDRESS)  # append missing data
                print(good(green(f'Saved {ADDRESS} to list')))
                cctvc_settings.close()
            else:
                if listing.find(ADDRESS) >= 0:
                    print(bad(red(f'{ADDRESS} already in list, not saved')))
                    cctvc_settings.close()
                else:
                    print(good(green(f'Saved {ADDRESS} to list')))
                    cctvc_settings.write("\n" + ADDRESS)  # append missing data
                    cctvc_settings.close()

    def detectedObjectResponse(self):
        """Handling of object detection as a seperate function"""
        # global detectedObjectResponse_isRunning
        # print(info(yellow("I'm sending a webhook to GroupLotse!")))
        # webhook_url = "https://webhook.grouplotse.com:4433/inc/18997579?key=QJu7OB5FjoGk"
        # data = "I have detected a Person in the Image!"
        # requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        # time.sleep(8)
        # detectedObjectResponse_isRunning = 0

    def ptz_movement(self, ADDRESS, USERNAME, PASSWORD, ):
        """Allows control of PTZ Cameras through Dahua API calls over HTTP Requests"""


        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == ('alt' and 'p'):
                if not CCTVC.ptz_active:
                    CCTVC.ptz_active = True
                    print("PTZ Controls Activated")
                elif CCTVC.ptz_active:
                    CCTVC.ptz_active = False
                    print("PTZ Controls Deactivated")

            if CCTVC.ptz_active:
                if event.event_type == keyboard.KEY_DOWN and event.name == 's':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=Down&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    print("DOWN")
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=Down&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=Up&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=Up&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'a':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=Left&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=Left&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'd':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=Right&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=Right&arg1=0&arg2=2&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=ZoomWide&arg1=0&arg2=0&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=ZoomWide&arg1=0&arg2=0&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'e':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=start&channel=1&code=ZoomTele&arg1=0&arg2=0&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    time.sleep(1)
                    APIURL = "http://" + ADDRESS + "/cgi-bin/ptz.cgi?action=stop&channel=1&code=ZoomTele&arg1=0&arg2=0&arg3=0"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'f':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/devVideoInput.cgi?action=autoFocus"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    print("Autofocusing...")

                if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/rainBrush.cgi?action=moveContinuously&interval=5"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    print(good(green("Wiper ON")))

                if event.event_type == keyboard.KEY_DOWN and event.name == 'm':
                    APIURL = "http://" + ADDRESS + "/cgi-bin/rainBrush.cgi?action=stopMove"
                    response = requests.get(APIURL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
                    print(bad(red("Wiper OFF")))

    def openimage(self, imagepath, SMD):
        """Opens an Image and displays it for viewing. If the SMD Checkbox has been ticket, object recognition
        will be employed"""
        # _________________________________________
        #   Object Recognition Parameters
        thresholdValue = 0.57

        windowName = "Output"
        classNames = []
        classFile = "coco.names"
        with open(classFile, 'rt') as f:
            classNames = [line.rstrip() for line in f]
        # print(classNames)

        configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "frozen_inference_graph.pb"

        #   Object Detection Accuracy Neuron Input
        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)  # Accuracy of detection
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        # _________________________________________

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

    def opencamerastream(self, ADDRESS, USERNAME, PASSWORD, CHANNELSELECT, STREAMSELECT, SMD, WEBCAM):
        global detectedObjectResponse_isRunning

        # _________________________________________
        #   Object Recognition Parameters
        thresholdValue = 0.57

        windowName = "Output"
        classNames = []
        classFile = "coco.names"
        with open(classFile, 'rt') as f:
            classNames = [line.rstrip() for line in f]
        # print(classNames)

        configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "frozen_inference_graph.pb"

        #   Object Detection Accuracy Neuron Input
        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)  # Accuracy of detection
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        # _________________________________________

        if WEBCAM == "1":
            capture = cv2.VideoCapture(0)
        elif WEBCAM == "0":
            capture = cv2.VideoCapture(str(
                "rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT
            ))
        #   PTZ Control
        ptz_control = threading.Thread(target=CCTVC.ptz_movement, args=(CCTVC, ADDRESS, USERNAME, PASSWORD,))
        ptz_control.daemon = True
        ptz_control.start()

        while (capture.isOpened()):

            if SMD == "1":
                success, img = capture.read()
                classIds, confs, bbox = net.detect(img, confThreshold=thresholdValue)
            ret, frame = capture.read()

            #   Allowing to resize the window
            text_color_top = (255, 255, 255)
            text_color_bot = (0, 0, 0)
            cv2.namedWindow(str(ADDRESS), cv2.WINDOW_NORMAL)
            #   Drawing Rectangles and Names for Object Recognition
            if SMD == "1":
                if len(classIds) != 0:
                    for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                        if classId == 1:
                            cv2.rectangle(frame, box, color=(0, 0, 255), thickness=2)
                            cv2.putText(frame, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                            cv2.putText(frame, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                        else:
                            cv2.rectangle(frame, box, color=(0, 255, 0), thickness=1)
                            cv2.putText(frame, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(frame, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        #if classId == int(1) and detectedObjectResponse_isRunning == 0:
                        #    detection = threading.Thread(target=detectedObjectResponse)
                        #    detection.start()
                        #    detectedObjectResponse_isRunning = 1
            if WEBCAM == "1":
                cv2.putText(frame, "CAM", (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_bot, thickness=3)
                cv2.putText(frame, "CAM", (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_top, thickness=2)
            elif WEBCAM == "0":
                cv2.putText(frame, ADDRESS, (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_bot, thickness=3)
                cv2.putText(frame, ADDRESS, (30, 40), cv2.FONT_HERSHEY_DUPLEX, 1.0, text_color_top, thickness=2)
            if CCTVC.ptz_active == True:
                cv2.putText(frame, "PTZ ON", (30, 80), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0,255,0), thickness=3)
            elif CCTVC.ptz_active == False:
                cv2.putText(frame, "PTZ OFF", (30, 80), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0,0,255), thickness=2)
            cv2.imshow(str(ADDRESS), frame)
            if cv2.waitKey(1) & 0xFF == ord('p'):
                break

            #   Taking a Snapshot of the live stream
            if cv2.waitKey(1) & 0xFF == ord('b'):
                stream_screenshot = capture.read()[1]
                cv2.imwrite("screenshot" + ".png", stream_screenshot)

            #   Checks if the Window is being closed by pressing the "X" button, if the window becomes invisible it'll break
            if cv2.getWindowProperty(str(ADDRESS), cv2.WND_PROP_VISIBLE) < 1:
                break
        capture.release()
        cv2.destroyAllWindows()
        WEBCAM = "0"

    def webhook_post(self, webhook_addr, webhook_key, webhook_msg):
        """Main function to send Text via Webhook.
        webhook_addr is the URL of your Webhook. webhook_key is the Key.
        Pass a String to webhook_msg and call the method."""
        webhook_lotse = webhook_addr + "?key=" + webhook_key

        try:
            requests.post(
                webhook_lotse,
                data=json.dumps(webhook_msg),
                headers={"Content-Type": "application/json"},
            )
            print('OK')
        except:
            raise Exception(
                "ERR!"
            )

    def webbrowserapiwindow(self, ADDRESS, USERNAME, PASSWORD, TARGETAPI):
        webbrowser.open("http://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + TARGETAPI)

    def openpageinbrowser(self, WEBURL):
        webbrowser.open(WEBURL)