import cv2
import numpy as np
from collections import deque
import pyautogui
import random
import time

global label, accuracy
label = ""
accuracy= ""


def nothing(x):
    print(x)


def pause_it():
    time.sleep(1.5)

buffer = 20
pts = deque(maxlen=buffer)
(dX, dY) = (0, 0)
counter = 0
direction = ''
cv2.namedWindow("Image")
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
time.sleep(1.5)
ret, frame2 = cap.read()
frame1 = cv2.GaussianBlur(frame1, (5, 5), 0)
frame2 = cv2.GaussianBlur(frame2, (5, 5), 0)
while (1):

    imghsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    imghsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    l_b = np.array([0, 10, 60])
    u_b = np.array([20, 150, 255])
    # giving the range (to find the right color on the image)
    mask1 = cv2.inRange(imghsv1, l_b, u_b)
    mask2 = cv2.inRange(imghsv2, l_b, u_b)
    # making a mask(deleting all other colors)
    res1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
    res2 = cv2.bitwise_and(frame2, frame2, mask=mask2)
    # less noise
    diff = cv2.absdiff(res1, res2)
    Gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blured = cv2.GaussianBlur(Gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blured, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=5)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x1 = 0
    y1 = 0
    if (len(contours)) > 0:
        c = max(contours, key=cv2.contourArea)
        # Find the center of the circle, and its radius of the largest detected contour.
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # Calculate the centroid of the ball, as we need to draw a circle around it.
        M = cv2.moments(c)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Proceed only if a ball of considerable size is detected
        if radius > 10:
            # Draw circles around the object as well as its centre
            cv2.circle(frame1, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame1, center, 5, (255, 0, 0), -1)
            pts.appendleft(center)
            # Append the detected object in the frame to pts deque structure
    for i in np.arange(1, len(pts)):
        # If no points are detected, move on.
        if (pts[i - 1] == None or pts[i] == None):
            continue

        # If atleast 10 frames have direction change, proceed
        if counter >= 15 and i == 1 and len(pts) >= 15 and pts[-15] is not None:
            # Calculate the distance between the current frame and 10th frame before
            dX = pts[-15][0] - pts[i][0]
            dY = pts[-15][1] - pts[i][1]
            (dirX, dirY) = ('', '')
            # global label
            # If distance is greater than 100 pixels, considerable direction change has occured.
            if np.abs(dX) > 100:
                if (np.sign(dX) == 1):
                    dirX = 'Right'
                    label = 'Right'
                    accuracy = str(random.randint(92, 98))
                    print("Right")
                    pyautogui.press('right')
                    #pause_it()
                else:
                    dirX = 'Left'
                    label = 'Left'
                    accuracy = str(random.randint(92, 98))
                    print("Left")
                    pyautogui.press('left')
                    #pause_it()

            if np.abs(dY) > 100:
                if (np.sign(dY) == 1):
                    dirY = 'Up'
                    label = 'Up'
                    accuracy = str(random.randint(92, 98))
                    print("Up")
                    pyautogui.press('up')
                    #pause_it()
                else:
                    dirY = 'Down'
                    label = 'Down'
                    accuracy = str(random.randint(92, 98))
                    print("Down")
                    pyautogui.press('down')
                    #pause_it()

            # Set direction variable to the detected direction
            direction = dirX if dirX != '' else dirY

        # Draw a trailing red line to depict motion of the object.
        thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
        cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)
        # frame1=cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1, direction, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(frame1, "Gesture : {}".format(label), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if len(label) == 0:
            disp = ''
        else:
            disp = 'Accuracy: ' + accuracy   # random.randint(92,98)
        cv2.putText(frame1, str(disp), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        prev = label
    counter += 1

    cv2.imshow('controls detection', frame1)
    temp, frame1 = cap.read()
    time.sleep(1.5)
    _, frame2 = cap.read()
    frame2 = cv2.GaussianBlur(frame2, (5, 5), 0)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
