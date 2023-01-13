import cv2 as cv
from datetime import datetime
import os
from PIL import Image
import numpy as np

if __name__ == '__main__':



    # lower bound and upper bound for Green color
    ORANGE_MIN = np.array([5, 50, 225],np.uint8)
    ORANGE_MAX = np.array([20, 255, 255],np.uint8)


    cap = cv.VideoCapture(0)

    # Object detection from Stable camera
    while cap.isOpened():
        ret, frame = cap.read()
        height, width, _ = frame.shape

        # convert to hsv colorspace
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # find the colors within the boundaries
        mask = cv.inRange(hsv, ORANGE_MIN, ORANGE_MAX)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_SIMPLE)

    
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 300:
                cv.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv.boundingRect(cnt)
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv.imshow('Capturing', frame)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            cv.destroyAllWindows()
            cap.release()
            quit()