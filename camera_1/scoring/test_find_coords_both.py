import numpy as np
import cv2
from find_coords_c1 import FindCoords
from triangulate import main as triangulate
from camera_1 import CameraOne
import time

def main():

    find_coords = FindCoords()
    cameraOne = CameraOne()

    cameraOne.startCamStreams()


    coords = cameraOne.getCoords()

    print(coords)
 
    c1 = coords[0]
    c2 = coords[1]

    print("C1: ", c1)

    print("C2: ", c2)

    d1_c1 = c1[0][0]
    d1_c2 = c2[0][0]
    d2_c1 = c1[1][0]
    d2_c2 = c2[1][0]
    d3_c1 = c1[2][0]
    d3_c2 = c2[2][0]

    print (d1_c1)

    if None in d1_c1 or None in d1_c2:
 
        print("Out of scoring area.")
        s_1 = [0,0]
 
    else:
        s_1 = triangulate(d1_c1,d1_c2)
 
  
    if None in d2_c1 or None in d2_c2:
        print("Out of scoring area.")
        s_2 = [0,0]
  
    else:
  
        s_2 = triangulate(d2_c1,d2_c2)
  
  
    if None in d3_c1 or None in d3_c1:
  
        print("Out of scoring area.")
        s_3 = [0,0]
  
    else:
  
        s_3 = triangulate(d3_c1,d3_c2)
 
    print(s_1,s_2,s_3)


    cameraOne.closeCamTwo()

def capFrames(cameraStreams):

    c1,c2 = cameraStreams.captureCalibFrame()
    
    return c1,c2

if __name__=='__main__':
    main()
