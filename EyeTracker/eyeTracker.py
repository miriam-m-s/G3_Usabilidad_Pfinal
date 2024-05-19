import sys
sys.path.append("./GazeTracking-master")

import cv2
from gaze_tracking import GazeTracking 

class EyeTracker:
    
    inited = False

    def setUp(self):
        assert(not self.inited)
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        if (not self.webcam.isOpened()):
            return False
        
        self.inited = True

        return True

    def getFrame(self):
        # We get a new frame from the webcam
        _, frame = self.webcam.read()

        # We send this frame to GazeTracking to analyze it
        self.gaze.refresh(frame)

        frame = self.gaze.annotated_frame()
        text = ""

        if self.gaze.is_blinking():
            text = "Blinking"
        elif self.gaze.is_right():
            text = "Looking right"
        elif self.gaze.is_left():
            text = "Looking left"
        elif self.gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        horizontal_ratio =  self.gaze.horizontal_ratio()
        vertical_ratio =  self.gaze.vertical_ratio()

        if (horizontal_ratio != None) :
            horizontal_ratio = round(horizontal_ratio, 2)

        if (vertical_ratio != None) :
            vertical_ratio = round(vertical_ratio, 2)

        #if (horizontal_ratio is not None | vertical_ratio is not None) :
        cv2.putText(frame, "Horizontal:  " + str(horizontal_ratio), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)
        cv2.putText(frame, "Vertical at:  " + str(vertical_ratio), (90, 210), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)
        left_pupil = self.gaze.pupil_left_coords()
        right_pupil = self.gaze.pupil_right_coords()
        # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        return frame, horizontal_ratio, vertical_ratio
    
    def release(self):
        assert(self.inited)
        self.webcam.release()
        
    