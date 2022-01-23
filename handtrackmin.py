import cv2 as cv
import mediapipe as mp
vid_main = cv.VideoCapture(0)
mpHands = mp.solutions.hands    # Driving Class. Used in drawing connections.
hand = mpHands.Hands()          # Used to process results
mpDraw = mp.solutions.drawing_utils         #Used to draw dots on landmarks
while True:
    success, frame = vid_main.read()
    rgbFrame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = hand.process(rgbFrame)
    # print(results.multi_hand_landmarks)
    lmlist = []

    if results.multi_hand_landmarks:
        for hndlnd in results.multi_hand_landmarks:
            # print(hndlnd.landmark)
            for idx, lnd in enumerate(hndlnd.landmark):
                h,w,c = frame.shape
                
                # print(frame.shape)
                cx, cy = int(lnd.x*w), int(lnd.y*h)
                #print(f"{idx},{cx},{cy}")

                lmlist.append([idx,cx,cy])

                if idx == 4:
                   
                    cv.circle(frame, (cx,cy), 10, (255, 0, 255), cv.FILLED)

                if idx == 8:
                        
                    cv.circle(frame, (cx,cy), 10, (0, 0, 255), cv.FILLED)

                if idx == 12:
                    cv.circle(frame, (cx, cy), 10, (0, 255, 255), cv.FILLED)

                if idx == 16:
                    cv.circle(frame, (cx, cy), 10, (255, 0, 0), cv.FILLED)

                if idx == 20:
                    cv.circle(frame, (cx, cy), 10, (255, 255, 255), cv.FILLED)

                

                # print(lmlist)
            
                for item in lmlist:
                    if item[0] == 8 or item[0] == 6:
                        
                        # print(item)
                        print(item)
                        print(item[2])
                   

                    else:
                        pass

                    

            mpDraw.draw_landmarks(frame, hndlnd, mpHands.HAND_CONNECTIONS)
            
    
    cv.imshow("Main", frame)
    key = cv.waitKey(1)
    if key == 113 or key == 81:
        break