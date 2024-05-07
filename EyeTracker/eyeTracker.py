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
        self.inited = True

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

        left_pupil = self.gaze.pupil_left_coords()
        right_pupil = self.gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        return frame
    
    def release(self):
        assert(self.inited)
        self.webcam.release()
        
    