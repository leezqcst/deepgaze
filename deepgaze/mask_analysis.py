#!/usr/bin/env python

#The MIT License (MIT)
#Copyright (c) 2016 Massimiliano Patacchiola
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import cv2
import sys

class BinaryMaskAnalyser:
    """This class analyses binary masks, like the ones returned by
       the color detection classes.

    The class implements function for finding the contour with the
    largest area and its properties (centre, sorrounding rectangle).
    There are also functions for noise removal.
    """

    def returnNumberOfContours(self, mask):
        """it returns the total number of contours present on the mask
 
        this method must be used during video analysis to check if the frame contains
        at least one contour before calling the other function below.
        @param mask the binary image to use in the function
        @return get the number of contours 
        """
        if(mask is None): return None
        mask = np.copy(mask) #doing a copy otherwise findContours modify the original(?)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        if(hierarchy is None): return 0
        else: return len(hierarchy)

    def returnMaxAreaCenter(self, mask):
        """it returns the centre of the contour with largest area.
 
        This method could be useful to find the center of a face when a skin detector filter is used.
        @param mask the binary image to use in the function
        @return get the x and y center coords of the contour whit the largest area 
        """
        if(mask is None): return None
        mask = np.copy(mask)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours)) #contains the area of the contours
        counter = 0
        for cnt in contours:   
                #cv2.drawContours(image, [cnt], 0, (0,255,0), 3)
                #print("Area: " + str(cv2.contourArea(cnt)))
                area_array[counter] = cv2.contourArea(cnt)
                counter += 1
        if(area_array.size==0): return None #the array is empty
        max_area_index = np.argmax(area_array) #return the index of the max_area element
        #cv2.drawContours(image, [contours[max_area_index]], 0, (0,255,0), 3)
        #Get the centre of the max_area element
        cnt = contours[max_area_index]
        M = cv2.moments(cnt) #calculate the moments
        cx = int(M['m10']/M['m00']) #get the center from the moments
        cy = int(M['m01']/M['m00'])
        return (cx, cy) #return the center coords

    def returnMaxAreaContour(self, mask):
        """it returns the contour with largest area.
 
        This method could be useful to find a face when a skin detector filter is used.
        @param mask the binary image to use in the function
        @return get the x and y center coords of the contour whit the largest area 
        """
        if(mask is None): return None
        mask = np.copy(mask)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours)) #contains the area of the contours
        counter = 0
        for cnt in contours:   
                #cv2.drawContours(image, [cnt], 0, (0,255,0), 3)
                #print("Area: " + str(cv2.contourArea(cnt)))
                area_array[counter] = cv2.contourArea(cnt)
                counter += 1
        if(area_array.size==0): return None #the array is empty
        max_area_index = np.argmax(area_array) #return the index of the max_area element
        cnt = contours[max_area_index]
        return cnt #return the max are contour

    def returnMaxAreaRectangle(self, mask):
        """it returns the rectangle sorrounding the contour with the largest area.
 
        This method could be useful to find a face when a skin detector filter is used.
        @param mask the binary image to use in the function
        @return get the coords of the upper corner of the rectangle (x, y) and the rectangle size (widht, hight)
        """
        if(mask is None): return None
        mask = np.copy(mask)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours)) #contains the area of the contours
        counter = 0
        for cnt in contours:   
                area_array[counter] = cv2.contourArea(cnt)
                counter += 1
        if(area_array.size==0): return None #the array is empty
        max_area_index = np.argmax(area_array) #return the index of the max_area element
        cnt = contours[max_area_index]
        (x, y, w, h) = cv2.boundingRect(cnt)
        return (x, y, w, h)

    def returnMaxAreaCircle(self, mask):
        """it returns the circle sorrounding the contour with the largest area.
 
        @param mask the binary image to use in the function
        @return get the center (x, y) and the radius of the circle
        """
        if(mask is None): return None
        mask = np.copy(mask)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours)) #contains the area of the contours
        counter = 0
        for cnt in contours:   
                area_array[counter] = cv2.contourArea(cnt)
                counter += 1
        if(area_array.size==0): return None #the array is empty
        max_area_index = np.argmax(area_array) #return the index of the max_area element
        cnt = contours[max_area_index]
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        return (int(x),int(y)), int(radius)
