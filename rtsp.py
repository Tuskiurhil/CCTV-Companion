#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import webbrowser
# Simple example of TabGroup element and the options available to it

sg.theme('Dark Amber')     # Please always add color to your window

#try:
#    splashscreen = ("splashscreen.png")
#    DISPLAY_TIME_MILLISECONDS = 1000
#
#    sg.Window('Window Title', [[sg.Image(splashscreen)]], transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
#except:
#    pass

def opencamerastream():
    global ADDRESS, USERNAME, PASSWORD, CHANNELSELECT
    capture = cv2.VideoCapture("rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+'/cam/realmonitor?channel=1&subtype='+CHANNELSELECT)
    #capture = cv2.VideoCapture("rtsp://admin:123456789a@192.168.178.222/cam/realmonitor?channel=1&subtype=1")

    while(capture.isOpened()):
        ret, frame = capture.read()
        #   Allowing to resize the window
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('Q'):
            break
        #   Checks if the Window is being closed by pressing the "X" button, if the window becomes invisible it'll break
        if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) <1:
            break
    capture.release()
    cv2.destroyAllWindows()


# The tab 1, 2, 3 layouts - what goes inside the tab



tab1_layout = [[sg.Text('RTSP Stream')],      
        [sg.Text('IP Address & Port'), sg.Input(key='-ADDRESS-')],
        [sg.Text('Username'), sg.Input(key='-USERNAME-')],
        [sg.Text('Password'), sg.Input(password_char = "•", key='-PASSWORD-')],
        [sg.Radio('Main Stream', 'CHANNEL', default=True, key='-CHANNEL0-'), sg.Radio('Sub Stream', 'CHANNEL', key='-CHANNEL1-')],
        [sg.Button('Open'), sg.Button('Web Interface'), sg.Exit(), sg.Button('Help')]]


tab2_layout = [[sg.Text('Capacity Calculation')]]
tab3_layout = [[sg.Text('IP Calculation')]]
tab4_layout = [[sg.Text('Lens Calculation')]]
tab5_layout = [[sg.Text('Controlex')],
                [sg.Button('Website'), sg.Button('Online Shop'), sg.Exit(), sg.Button('Help', key='-CONTROLEXHELP-')]]



tab6_layout = [[sg.Text('Controlex CCTV Companion\n\n'
                        'Version 0.1\n')]]


# The TabgGroup layout - it must contain only Tabs
tab_group_layout = [[sg.Tab('RTSP Stream', tab1_layout, key='-TAB1-'),
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

tab_keys = ('-TAB1-','-TAB2-','-TAB3-', '-TAB4-','-TAB5-','-TAB6-',)         # map from an input value to a key

while True:
    event, values = window.read()
    #print(event, values)
    if event == 'Open':
        ADDRESS = values['-ADDRESS-']
        USERNAME = values['-USERNAME-']
        PASSWORD = values['-PASSWORD-']
        if values["-CHANNEL0-"] == True:
            CHANNELSELECT = '0'
        elif values["-CHANNEL1-"] == True:
            CHANNELSELECT = '1'
        ###ADDRESS = values['-ADDRESS-']
        opencamerastream()
    if event == 'Web Interface':
        ADDRESS = values['-ADDRESS-']
        webbrowser.open(ADDRESS)
    if event == 'Help':
        sg.popup(
            'RTSP Stream\n\n'
            'This Window can be used to open the RTSP Stream of an IP-Camera.\n\n'
            "Enter the IP-Address of your desired Camera (If you're using the Default RTSP-Port 554 then you don't need to enter the Port)\n\n"
            "If you click on the Button 'Web Interface' it'll open your default Webbrowser and navigate you to the entered IP-Address\n\n"
            "You can select which Stream you want to see by clicking either 'Main Stream' or 'Sub Stream'\n")
    if event == '-CONTROLEXHELP-':
        #   works!
        [sg.Popup('Test')]
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # handle button clicks
    #if event == 'Invisible':
    #    window[tab_keys[int(values['-IN-'])-1]].update(visible=False)
    #if event == 'Visible':
    #    window[tab_keys[int(values['-IN-'])-1]].update(visible=True)
    #if event == 'Select':
    #    window[tab_keys[int(values['-IN-'])-1]].select()

window.close()