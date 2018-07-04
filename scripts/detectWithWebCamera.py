import cv2
import numpy as np
import time
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

from api import detectTrafficSign

camera = cv2.VideoCapture(0)

def findTrafficSign():
    '''
    This function find blobs with blue color on the image.
    After blobs were found it detects the largest square blob, that must be the sign.
    '''
    # define range HSV for blue color of the traffic sign
    # lower_blue = np.array([85,100,70])
    # upper_blue = np.array([115,255,255])
    lower_red = np.array([160,20,70])
    upper_red = np.array([190,255,255])

    i = 0

    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        
        if not grabbed:
            print("No input image")
            break
        
        frame = imutils.resize(frame, width=500)
        frameArea = frame.shape[0]*frame.shape[1]
        
        # convert color image to HSV color scheme
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define kernel for smoothing   
        kernel = np.ones((3,3),np.uint8)
        # extract binary image with active blue regions
        mask = cv2.inRange(hsv, lower_red, upper_red)
        # morphological operations
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        # defite string variable to hold detected sign description
        # detectedTrafficSign = None
        
        # define variables to hold values during loop
        largestArea = 0
        largestRect = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            for cnt in cnts:
                # Rotated Rectangle. Here, bounding rectangle is drawn with minimum area,
                # so it considers the rotation also. The function used is cv2.minAreaRect().
                # It returns a Box2D structure which contains following detals -
                # ( center (x,y), (width, height), angle of rotation ).
                # But to draw this rectangle, we need 4 corners of the rectangle.
                # It is obtained by the function cv2.boxPoints()
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.intc(box)
                
                # count euclidian distance for each side of the rectangle
                sideOne = np.linalg.norm(box[0]-box[1])
                sideTwo = np.linalg.norm(box[0]-box[3])
                # count area of the rectangle
                area = sideOne*sideTwo
                # find the largest rectangle within all contours
                if area > largestArea:
                    largestArea = area
                    largestRect = box
            

        # draw contour of the found rectangle on the original image
        
        if largestArea > frameArea*0.02:
            points = {
                'xStart': 0,
                'xEnd': 0,
                'yStart': 0,
                'yEnd': 0
            }
            if largestRect[0][0] <= largestRect[1][0] and largestRect[0][0] > 0 and largestRect[1][0]:
                points['xStart'] = largestRect[0][0]
            else:
                points['xStart'] = largestRect[1][0]

            if largestRect[2][0] >= largestRect[3][0]  and largestRect[2][0] > 0 and largestRect[3][0]:
                points['xEnd'] = largestRect[2][0]
            else:
                points['xEnd'] = largestRect[3][0]

            if largestRect[1][1] <= largestRect[2][1]  and largestRect[1][1] > 0 and largestRect[2][1]:
                points['yStart'] = largestRect[1][1]
            else:
                points['yStart'] = largestRect[2][1]

            if largestRect[0][1] >= largestRect[3][1]  and largestRect[0][1] > 0 and largestRect[3][1]:
                points['yEnd'] = largestRect[0][1]
            else: 
                points['yEnd'] = largestRect[3][1]
            
            if points['xStart'] < 0:
                points['xStart'] = 0
            
            if points['yStart'] < 0:
                points['yStart'] = 0
            
            if points['xEnd'] < 0:
                points['xEnd'] = 0
            
            if points['yEnd'] < 0:
                points['yEnd'] = 0
            # print largestRect
            # print points
            croped = frame[points['yStart']:points['yEnd'],points['xStart']:points['xEnd']]
            
            cv2.imwrite('../data/cropped'+str(i)+'.png', croped)
            # cv2.imshow('cropped', croped)
            cv2.drawContours(frame,[largestRect],0,(0,0,255),2)
            signName = detectTrafficSign(i)
            i+=1
        #if largestRect is not None:
            # cut and warp interesting area
            warped = four_point_transform(mask, [largestRect][0])
            
            # show an image if rectangle was found
            #cv2.imshow("Warped", cv2.bitwise_not(warped))
            
            # use function to detect the sign on the found rectangle
            # detectedTrafficSign = identifyTrafficSign(warped)
            #print(detectedTrafficSign)

            if signName == 'no sign':
            # write the description of the sign on the original image
                signName = ''
            cv2.putText(frame, signName, tuple(largestRect[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        
        # show original image
        cv2.imshow("Original", frame)
        
        # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF is ord('q'):
            cv2.destroyAllWindows()
            print("Stop programm and close all windows")
            break
# ====================== main function of program ========================
def main():
    findTrafficSign()


if __name__ == '__main__':
    main()

