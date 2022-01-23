import cv2 as cv
import mediapipe as mp


class HandDetector():
    def __init__(self, mode = False, maxHands = 2, detection_confidence=.6, tracking_confidence=.6):
        self.mode = mode
        self.maxHands = maxHands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.detection_confidence,self.tracking_confidence)
        self.mpdraw = mp.solutions.drawing_utils


    def findHands(self, frame, draw = True):


        rgbframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        
            
        self.results = self.hands.process(rgbframe)

        if self.results.multi_hand_landmarks:
            for handlandmarks in self.results.multi_hand_landmarks:
                if draw:

                    self.mpdraw.draw_landmarks(frame, handlandmarks, self.mphands.HAND_CONNECTIONS)
        return frame
        
            
    def findPosition(self, frame, handno=0, draw = True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]

            for idofpoint, landmarks in enumerate(myhand.landmark):
                h,w,c = frame.shape
                            
                x_points = int(landmarks.x*w)
                y_points = int(landmarks.y*h)
                lmlist.append([idofpoint, x_points, y_points])
                if draw:
                    cv.circle(frame, (x_points,y_points), 15, (255,0,255),cv.FILLED)

        return lmlist

def main():

    mainwindow = cv.VideoCapture(0)

    detector = HandDetector()
    while True:
        success, frame = mainwindow.read()
        frame = detector.findHands(frame)

        mylistofpoints = detector.findPosition(frame)
        if len(mylistofpoints) != 0:
            print(mylistofpoints[4])




        cv.imshow("HELLO", frame)
        key = cv.waitKey(1)
        if key == 81 or key == 113:
            break


if __name__ == "__main__":
    main()