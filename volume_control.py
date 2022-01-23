import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]

wCam = 800
hCam = 450
mainvideo = cv.VideoCapture(0)
mainvideo.set(3, wCam)
mainvideo.set(4, hCam)
detector = htm.HandDetector(detection_confidence=0.7)


while True:
    success, frame = mainvideo.read()
    if success:
        detector.findHands(frame)
        lmlist = detector.findPosition(frame, draw= False)

        if len(lmlist) != 0:
            #print(lmlist[4])
            #print(lmlist[8])

            x1 = lmlist[4][1]
            y1 = lmlist[4][2]

            x2 = lmlist[8][1]
            y2 = lmlist[8][2]

            cx = int(x1+x2)//2
            cy = int(y1+y2)//2        

            cv.circle(frame, (x1,y1), 10, (255,255,255), cv.FILLED)
            cv.circle(frame, (x2,y2), 10, (255,255,255), cv.FILLED)
            
            cv.circle(frame, (cx,cy), 10, (255,255,255), cv.FILLED)

            cv.line(frame, (x1,y1), (x2,y2), (255,255,255), 2)

            length = ((x1-x2)**(2) + (y1-y2)**(2))**(1/2)
            #print(length) 
            vol = np.interp(length, [25, 190], [minvol,maxvol])
            volume.SetMasterVolumeLevel(vol, None)
            showvol = int(np.interp(length, [25, 190], [0,100]))
            print(showvol)
            cv.putText(frame, f"Volume: {str(showvol)}",(20,40), cv.FONT_HERSHEY_TRIPLEX, 1, (0,0,0))
            if length <= 25:
                cv.circle(frame, (cx,cy), 10, (0,0,255), cv.FILLED)
        cv.imshow("Main", frame)
        key = cv.waitKey(1)
        if key == 81 or key == 113:
            break

    else:
        print("Isuue")

