import PySimpleGUI as sg    
import cv2  





def opencamerastream():
    global ADDRESS, USERNAME, PASSWORD
    capture = cv2.VideoCapture("rtsp://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+"/cam/realmonitor?channel=1&subtype=1")
    #capture = cv2.VideoCapture("rtsp://admin:123456789a@192.168.178.222/cam/realmonitor?channel=1&subtype=1")

    while(capture.isOpened()):
        ret, frame = capture.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()



sg.theme('DarkAmber')  

layout = [[sg.Text('RTSP Stream')],      
          [sg.Text('IP Address'), sg.Input(key='-ADDRESS-')],
          [sg.Text('Username'), sg.Input(key='-USERNAME-')],
          [sg.Text('Password'), sg.Input(key='-PASSWORD-')],      
          [sg.Button('Open'), sg.Exit()]]      

window = sg.Window('Window that stays open', layout)      

while True:                             # The Event Loop
    event, values = window.read() 
    if event == 'Open':
        ADDRESS = values['-ADDRESS-']
        USERNAME = values['-USERNAME-']
        PASSWORD = values['-PASSWORD-']
        ###ADDRESS = values['-ADDRESS-']
        opencamerastream()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      







window.close()