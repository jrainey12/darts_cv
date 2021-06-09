import numpy as np
import cv2
from find_coords_c2 import FindCoords
import time
import pickle
from camera_2 import CameraTwo

def main():

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    dart = 0

    timer = 1
    loop = 0
    find_coords = FindCoords()
    cameraTwo = CameraTwo()

    while True:
        loop += 1
        #print ("Loop: ",loop)
        _,cam = cap.read()
        
        if timer % 5 == 0:
            timer = timer + 1
            print ("saving frame ", dart)
            frame = cv2.flip(cam.copy(),0)
            cameraTwo.setFrame(dart,frame)
            dart = dart + 1
            print("Throw "+ str(dart))
            #time.sleep(3)
            if dart == 4:
                break
        if loop % 30 == 0:
            #print("sleeping")
            time.sleep(1)
            timer = timer + 1
            print("Timer: ", timer)
    #_,cam = cap.read()
    #frame = cv2.flip(cam.copy(),0)
    #cameraTwo.setFrame(1,frame)

    #print("Throw")
    #time.sleep(3)
    #_,cam = cap.read()
    #frame = cv2.flip(cam.copy())
    #cameraTwo.setFrame(2,frame)

   # print ("Throw")
    #time.sleep(3)
   # _,cam = cap.read()
   # frame = cv2.flip(cam.copy(),0)
   # cameraTwo.setFrame(3,frame)

    cameraTwo.determineCoords()

    coords = cameraTwo.getCoords()
    
    c = pickle.dumps(coords)
    print(len(c))
                
    c_len = bytes(str(len(c)),"utf-8")

    print(c_len)

    print (coords)
    return coords

if __name__=='__main__':
    main()
