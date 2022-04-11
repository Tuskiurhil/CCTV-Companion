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
                    [sg.Text('1 Megapixel'), sg.Input('', key='-#1MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL1', default=True, key='#1MPh265'), sg.Radio('H.264', 'CODECSEL1', key='#1MPh264'), sg.Radio('MJPEG', 'CODECSEL1', key='#1MPMJPEG')],
                    [sg.Text('2 Megapixel'), sg.Input('', key='-#2MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL2', default=True, key='#2MPh265'), sg.Radio('H.264', 'CODECSEL2', key='#2MPh264'), sg.Radio('MJPEG', 'CODECSEL2', key='#2MPMJPEG')],
                    [sg.Text('4 Megapixel'), sg.Input('', key='-#4MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL4', default=True, key='#4MPh265'), sg.Radio('H.264', 'CODECSEL4', key='#4MPh264'), sg.Radio('MJPEG', 'CODECSEL4', key='#4MPMJPEG')],
                    [sg.Text('5 Megapixel'), sg.Input('', key='-#5MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL5', default=True, key='#5MPh265'), sg.Radio('H.264', 'CODECSEL5', key='#5MPh264'), sg.Radio('MJPEG', 'CODECSEL5', key='#5MPMJPEG')],
                    [sg.Text('6 Megapixel'), sg.Input('', key='-#6MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL6', default=True, key='#6MPh265'), sg.Radio('H.264', 'CODECSEL6', key='#6MPh264'), sg.Radio('MJPEG', 'CODECSEL6', key='#6MPMJPEG')],
                    [sg.Text('8 Megapixel'), sg.Input('', key='-#8MP-', size=(4, 1)), sg.Radio('H.265', 'CODECSEL8', default=True, key='#8MPh265'), sg.Radio('H.264', 'CODECSEL8', key='#8MPh264'), sg.Radio('MJPEG', 'CODECSEL8', key='#8MPMJPEG')],
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