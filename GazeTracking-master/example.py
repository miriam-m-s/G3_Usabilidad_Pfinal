"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    horizontal_ratio = gaze.horizontal_ratio()
    vertical_ratio = gaze.vertical_ratio()

    if (horizontal_ratio != None) :
        horizontal_ratio = round(horizontal_ratio, 2)

    if (vertical_ratio != None) :
        vertical_ratio = round(vertical_ratio, 2)

    #if (horizontal_ratio is not None | vertical_ratio is not None) :
    cv2.putText(frame, "Horizontal:  " + str(horizontal_ratio), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)
    cv2.putText(frame, "Vertical at:  " + str(vertical_ratio), (90, 210), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)

    # left_pupil = gaze.pupil_left_coords()
    # right_pupil = gaze.pupil_right_coords()
    # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
