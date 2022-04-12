#!/usr/bin/env python
from tarfile import NUL
import PySimpleGUI as sg
import cv2
import webbrowser
import pyperclip
import os 
import threading
import multiprocessing
import sys
import time

animated_gif = b'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'

ADDRESS = ""
USERNAME = ""
PASSWORD = ""
TARGETAPI = ""
loading_gif = r'loadingcircle.gif'

def webbrowserapiwindow():
    global ADDRESS, USERNAME, PASSWORD, TARGETAPI
    webbrowser.open("http://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+TARGETAPI)

def opencamerastream(ADDRESS, USERNAME, PASSWORD, CHANNELSELECT):
    #global ADDRESS, USERNAME, PASSWORD, CHANNELSELECT
    capture = cv2.VideoCapture("rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT)
    while(capture.isOpened()):
        ret, frame = capture.read()
        #   Allowing to resize the window
        cv2.namedWindow(str(ADDRESS), cv2.WINDOW_NORMAL)
        cv2.imshow(str(ADDRESS), frame)
        if cv2.waitKey(20) & 0xFF == ord('Q'):
            break
            #rtspcounter -= 1
        #   Checks if the Window is being closed by pressing the "X" button, if the window becomes invisible it'll break
        if cv2.getWindowProperty(str(ADDRESS), cv2.WND_PROP_VISIBLE) <1:
            break
            #rtspcounter -= 1
        #if cv2.getWindowProperty(str(ADDRESS), 0) >= 0:
            #keyCode = cv2.waitKey(50)
            #break
    #rtspcounter -= 1
    capture.release()
    cv2.destroyAllWindows()
    #print(rtspcounter)


def main():
    sg.theme('DarkGrey5')     # Please always add color to your window
    #rtspcounter = 0
    MP1 = int()
    MP2 = int()
    MP4 = int()
    MP5 = int()
    MP6 = int()
    MP8 = int()
    MP12 = int()

    global ADDRESS, USERNAME, PASSWORD, TARGETAPI, loading_gif
    try:
        splashscreen = "splashscreen.png"
        isExist = os.path.exists(splashscreen)
        if isExist == True:
            DISPLAY_TIME_MILLISECONDS = 600
            sg.Window('Window Title', [[sg.Image(splashscreen)]], transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
        elif isExist == False:
            pass
    except:
        pass

    # The tab 1, 2, 3 layouts - what goes inside the tab

    tab0_layout = [[sg.Text('Camera Maintenance')],      
            [sg.Text('IP Address'), sg.Input(key='-ADDRESSMAINT-')],
            [sg.Text('Username'), sg.Input(key='-USERNAMEMAINT-')],
            [sg.Text('Password'), sg.Input(password_char = "•", key='-PASSWORDMAINT-')],
            [sg.Button('Serial No.'), sg.Button('Device Type'), sg.Button('Firmware Version')],
            [sg.Button('Reboot'), sg.Button('Snapshot')],
            [sg.Button('Exit', key='-EXIT0-')]]
        
            #[sg.Button('Open'), sg.Button('Copy RTSP Link'), sg.Button('Web Interface'), sg.Button('Exit', key='-EXIT-'), sg.Button('Help')]]

    tab1_layout = [[sg.Text('RTSP Stream'), sg.Image('dahua_logo.png', subsample=(14), tooltip=('This RTSP Stream only works with Dahua IP-Cameras'))],
            [sg.Text('IP Address & Port'), sg.Input(key='-ADDRESS-')],
            [sg.Text('Username'), sg.Input(key='-USERNAME-')],
            [sg.Text('Password'), sg.Input(password_char = "•", key='-PASSWORD-')],
            [sg.Radio('Main Stream', 'CHANNEL', default=True, key='-CHANNEL0-'), sg.Radio('Sub Stream', 'CHANNEL', key='-CHANNEL1-')],
            [sg.Button('Open'), sg.Button('Copy RTSP Link'), sg.Button('Web Interface'), sg.Button('Exit', key='-EXIT1-'), sg.Button('Help')]]
            

    #tab2_videosize = [sg.Text('Under Construction')]
    #tab2_recordtime = [sg.Text('Under Construction')]
    #tab2_diskarray = [sg.Text('Under Construction')]
    #tab2grouplayout = [sg.Tab('Video Size', tab2_videosize, key='-VIDEOSIZE-'), 
                    #sg.Tab('Record Time', tab2_recordtime, key='-RECORDTIME-'),
                    #sg.Tab('Disk Array', tab2_diskarray, key='-DISKARRAY-')]
    tab2_layout =   [[sg.Text('Bandwidth Calculation - (High Quality / 25 fps)')],
                    [sg.Text('Resolution'), sg.Text('# of Cameras'), sg.Text('Codec')],
                    [sg.Text('1 Megapixel  '), sg.Input('', key='-#1MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL1', default=True, key='#1MPh265'), sg.Radio('H.264', 'CODECSEL1', key='#1MPh264'), sg.Radio('MJPEG', 'CODECSEL1', key='#1MPMJPEG')],
                    [sg.Text('2 Megapixel  '), sg.Input('', key='-#2MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL2', default=True, key='#2MPh265'), sg.Radio('H.264', 'CODECSEL2', key='#2MPh264'), sg.Radio('MJPEG', 'CODECSEL2', key='#2MPMJPEG')],
                    [sg.Text('4 Megapixel  '), sg.Input('', key='-#4MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL4', default=True, key='#4MPh265'), sg.Radio('H.264', 'CODECSEL4', key='#4MPh264'), sg.Radio('MJPEG', 'CODECSEL4', key='#4MPMJPEG')],
                    [sg.Text('5 Megapixel  '), sg.Input('', key='-#5MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL5', default=True, key='#5MPh265'), sg.Radio('H.264', 'CODECSEL5', key='#5MPh264'), sg.Radio('MJPEG', 'CODECSEL5', key='#5MPMJPEG')],
                    [sg.Text('6 Megapixel  '), sg.Input('', key='-#6MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL6', default=True, key='#6MPh265'), sg.Radio('H.264', 'CODECSEL6', key='#6MPh264'), sg.Radio('MJPEG', 'CODECSEL6', key='#6MPMJPEG')],
                    [sg.Text('8 Megapixel  '), sg.Input('', key='-#8MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL8', default=True, key='#8MPh265'), sg.Radio('H.264', 'CODECSEL8', key='#8MPh264'), sg.Radio('MJPEG', 'CODECSEL8', key='#8MPMJPEG')],
                    [sg.Text('12 Megapixel'), sg.Input('', key='-#12MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL12', default=True, key='#12MPh265'), sg.Radio('H.264', 'CODECSEL12', key='#12MPh264'), sg.Radio('MJPEG', 'CODECSEL12', key='#12MPMJPEG')],
                    [sg.Button('Calculate', key='-BANDWIDTHCALCULATE-'), sg.Button('Exit', key='-EXIT2-')],

                    [sg.Text('Approximate Bandwidth Usage: '), sg.InputText("", key="-BandwidthResultTextKB-", readonly=True, size=(8,1), text_color="black"), sg.Text("Kilobit per second")],
                    [sg.Text('Approximate Bandwidth Usage: '), sg.InputText("", key="-BandwidthResultTextMB-", readonly=True, size=(8,1), text_color="black"), sg.Text("Megabit per second")]]

    #tabby_layout = [sg.Text('Bandwidth Calculation'), tab_capacitycalculation]

    #= [[sg.Tab('Capacity Calculation', layout_capacitycalculation)]]


    tab3_layout = [[sg.Text('IP Calculation')]]

    tab4_layout = [[sg.Text('Lens Calculation')]]

    tab5_layout = [[sg.Text('Controlex')],
                    [sg.Button('Website', key='-CONTROLEXWEBSITE-'), sg.Button('Online Shop', key='-CONTROLEXWEBSHOP-'), sg.Button('Support Portal', key='-CONTROLEXSUPPORTPORTAL-'), sg.Button('Exit', key='-EXIT5-'), sg.Button('Help', key='-CONTROLEXHELP-')]]



    tab6_layout = [[sg.Text('Controlex CCTV Companion\n\n'
                            'Version 0.1\n\n\n\n\n')],
                    [sg.Text('Dahua Products and the Dahua Logo are ©Copyrighted by Dahua Technology Co., Ltd\n')],
                    [sg.Text('The Controlex Logo is ©Copyrighted by Controlex GmbH')]]


    #   Bandwidth Calculation
    oneMPh265 = 1024



    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [[sg.Tab('Camera Maintenance', tab0_layout, key='-TAB0-'),
                        sg.Tab('RTSP Stream', tab1_layout, key='-TAB1-'),
                        sg.Tab('Capacity Calculation', tab2_layout, key='-TAB2-'),
                        sg.Tab('IP Calculation', tab3_layout, key='-TAB3-'),
                        sg.Tab('Lens Calculation', tab4_layout, key='-TAB4-'),
                        sg.Tab('Controlex', tab5_layout, key='-TAB5-'),
                        sg.Tab('About', tab6_layout, key='-TAB6-'),
                        ]]



    # The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                        enable_events=True,
                        key='-TABGROUP-')]]
    #          [sg.Text('Make tab number'), sg.Input(key='-IN-', size=(30,30)), sg.Button('Invisible'), sg.Button('Visible'), sg.Button('Select')]]

    window = sg.Window('CCTV Companion', layout, no_titlebar=False)

    tab_keys = ('-TAB0-','-TAB1-','-TAB2-','-TAB3-', '-TAB4-','-TAB5-','-TAB6-',)         # map from an input value to a key

    while True:
        event, values = window.read()
        #print(event, values)

        #   Camera Maintenance
        if event == 'Serial No.':
            ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=getSerialNo"
            serialnoapi = threading.Thread(target=webbrowserapiwindow())
            serialnoapi.start()

        if event == 'Device Type':
            ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=getDeviceType"
            serialnoapi = threading.Thread(target=webbrowserapiwindow())
            serialnoapi.start()

        if event == 'Firmware Version':
            ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=getSoftwareVersion"
            serialnoapi = threading.Thread(target=webbrowserapiwindow())
            serialnoapi.start()

        if event == 'Reboot' and sg.popup_yes_no('This will restart your device, are you sure?') == 'Yes':
            ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/magicBox.cgi?action=reboot"
            serialnoapi = threading.Thread(target=webbrowserapiwindow())
            serialnoapi.start()

        if event == 'Snapshot':
            ADDRESS = values['-ADDRESSMAINT-']
            USERNAME = values['-USERNAMEMAINT-']
            PASSWORD = values['-PASSWORDMAINT-']
            TARGETAPI = "/cgi-bin/snapshot.cgi"
            serialnoapi = threading.Thread(target=webbrowserapiwindow())
            serialnoapi.start()

        if event == 'Open':
            #print(rtspcounter)
            ADDRESS = values['-ADDRESS-']
            USERNAME = values['-USERNAME-']
            PASSWORD = values['-PASSWORD-']
            if values["-CHANNEL0-"] == True:
                CHANNELSELECT = '0'
            elif values["-CHANNEL1-"] == True:
                CHANNELSELECT = '1'
            ###ADDRESS = values['-ADDRESS-']
            #if rtspcounter != 0:
                #sg.PopupError("Only one RTSP Stream can be open at any time!")
            #if rtspcounter != 1:
                #rtspcounter += 1
                #print(rtspcounter)
            camstream = multiprocessing.Process(target=opencamerastream, args=(ADDRESS,USERNAME,PASSWORD,CHANNELSELECT,))
            print("Opening RTSP Stream, please wait a moment...")
                #camstream = threading.Thread(target=opencamerastream)
            camstream.daemon = True
            camstream.start()
            for i in range(350):
                sg.popup_animated(loading_gif, time_between_frames=40)
            sg.popup_animated(None)
            #opencamerastream()
        if event == 'Copy RTSP Link':
            ADDRESS = values['-ADDRESS-']
            USERNAME = values['-USERNAME-']
            PASSWORD = values['-PASSWORD-']
            if values["-CHANNEL0-"] == True:
                CHANNELSELECT = '0'
            elif values["-CHANNEL1-"] == True:
                CHANNELSELECT = '1'
            pyperclip.copy("rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT)
            sg.popup_no_wait('Link copied')
        if event == 'Web Interface':
            ADDRESS = values['-ADDRESS-']
            webbrowser.open(ADDRESS)
        if event == 'Help':
            sg.popup(
                'RTSP Stream\n\n'
                'This Window can be used to open the RTSP Stream of an IP-Camera.\n\n'
                "Enter the IP-Address of your desired Camera (If you're using the Default RTSP-Port 554 then you don't need to enter the Port)\n\n"
                "Clicking 'Copy RTSP Link' will take the Input of the above fields, merge them together and copy a usable RTSP Link to your clipboard\n\n"
                "If you click on the Button 'Web Interface' it'll open your default Webbrowser and navigate you to the entered IP-Address\n\n"
                "You can select which Stream you want to see by clicking either 'Main Stream' or 'Sub Stream'\n")

        if event == '-BANDWIDTHCALCULATE-':
            #BandwidthCalculationResult = 
            try:
                if len(values['-#1MP-']) > 0:
                    if values['#1MPh265'] == True:
                        MP1 = int(values['-#1MP-']) * 1024
                    elif values['#1MPh264'] == True:
                        MP1 = int(values['-#1MP-']) * 2048
                if len(values['-#1MP-']) == 0:
                    MP1 = 0
                    #pass

                if len(values['-#2MP-']) > 0:
                    if values['#2MPh265'] == True:
                        MP2 = int(values['-#2MP-']) * 2048
                    elif values['#2MPh264'] == True:
                        MP2 = int(values['-#2MP-']) * 4096
                if len(values['-#2MP-']) == 0:
                    MP2 = 0
                    #pass

                if len(values['-#4MP-']) > 0:
                    if values['#4MPh265'] == True:
                        MP4 = int(values['-#4MP-']) * 2048
                    elif values['#4MPh264'] == True:
                        MP4 = int(values['-#4MP-']) * 4096
                if len(values['-#4MP-']) == 0:
                    MP4 = 0
                    #pass

                if len(values['-#5MP-']) > 0:
                    if values['#5MPh265'] == True:
                        MP5 = int(values['-#5MP-']) * 3072
                    elif values['#5MPh264'] == True:
                        MP5 = int(values['-#5MP-']) * 6144
                if len(values['-#5MP-']) == 0:
                    MP5 = 0
                    #pass

                if len(values['-#6MP-']) > 0:
                    if values['#6MPh265'] == True:
                        MP6 = int(values['-#6MP-']) * 3072
                    elif values['#6MPh264'] == True:
                        MP6 = int(values['-#6MP-']) * 6144
                if len(values['-#6MP-']) == 0:
                    MP6 = 0
                    #pass

                if len(values['-#8MP-']) > 0:
                    if values['#8MPh265'] == True:
                        MP8 = int(values['-#8MP-']) * 4096
                    elif values['#8MPh264'] == True:
                        MP8 = int(values['-#8MP-']) * 8192
                if len(values['-#8MP-']) == 0:
                    MP8 = int(0)
                    #pass

                if len(values['-#12MP-']) > 0:
                    if values['#12MPh265'] == True:
                        MP12 = int(values['-#12MP-']) * 6144
                    elif values['#12MPh264'] == True:
                        MP12 = int(values['-#12MP-']) * 12288
                if len(values['-#12MP-']) == 0:
                    MP12 = int(0)
                    #pass

            
                #if int(values['-#1MP-']) > 0:
                    #bandwidthresult = int(values['-#1MP-']) * 1024
                    
            
                    #[sg.PopupOK(result+"kbps")]
            #except:
                #if len(values['-#1MP-']) == 0:
                    #[sg.PopupError('You must input a number of cameras')]
            
            finally:
                bandwidthresultKB = (MP1 + MP2 + MP4 + MP5 + MP6 + MP8 + MP12)
                window['-BandwidthResultTextKB-'].update(bandwidthresultKB)
                bandwidthresultMB = ((MP1 + MP2 + MP4 + MP5 + MP6 + MP8 + MP12) / 1000)
                window['-BandwidthResultTextMB-'].update(bandwidthresultMB)




            # 
            # int(values['-#1MP-']) * int(metadata['#1MPh265'])
                    

        if event == '-CONTROLEXWEBSITE-':
            webbrowser.open('https://controlex.eu')

        if event == '-CONTROLEXWEBSHOP-':
            webbrowser.open('https://controlex-shop.com')

        if event == '-CONTROLEXSUPPORTPORTAL-':
            webbrowser.open('https://controlex-shop.freshdesk.com/support/login')

        if event == '-CONTROLEXHELP-':
            [sg.Popup('Controlex\n\n'
                        'Use the links on this Site to quickly navigate to our Website, Online-Shop or Helpdesk\n')]

        if event == sg.WIN_CLOSED or event == '-EXIT0-' or event == '-EXIT1-' or event == '-EXIT2-' or event == '-EXIT3-' or event == '-EXIT4-' or event == '-EXIT5-' or event == '-EXIT6-':
            break
        # handle button clicks
        #if event == 'Invisible':
        #    window[tab_keys[int(values['-IN-'])-1]].update(visible=False)
        #if event == 'Visible':
        #    window[tab_keys[int(values['-IN-'])-1]].update(visible=True)
        #if event == 'Select':
        #    window[tab_keys[int(values['-IN-'])-1]].select()

    window.close()

if __name__ == '__main__':
    main()