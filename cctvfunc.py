#!/usr/bin/env python3
import cv2
import webbrowser

class CCTV:
#   Main function for RTSP stream. Will receive Arguments, construct them to a full address and then grab
#   the stream with cv2.
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
    #   Checks if the Window is being closed by pressing the "X" button, if the window becomes invisible it'll break
            if cv2.getWindowProperty(str(ADDRESS), cv2.WND_PROP_VISIBLE) <1:
                break
        capture.release()
        cv2.destroyAllWindows()



    def webbrowserapiwindow(ADDRESS, USERNAME, PASSWORD, TARGETAPI):
        webbrowser.open("http://"+USERNAME+":"+PASSWORD+"@"+ADDRESS+TARGETAPI)