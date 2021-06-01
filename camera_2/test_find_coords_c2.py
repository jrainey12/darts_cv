import numpy as np
import cv2
from camera_2.find_coords_c2 import FindCoords
import time

def main():

    find_coords = FindCoords()
    #cameraStreams = CameraStreams()

#    cameraStreams.startCamTwoStream()   
#    time.sleep(3)
#    cameraStreams.connectCamTwo()
    
    frames = [None,None,None,None]

    try:

        for x in range(3):
            print (x)
            dart = x+1
            print("dart:",dart)
            if x == 0:
                
                #back_1,back_2 = capFrames(cameraStreams) 
                
                back = cv2.imread("test_imgs/c2_back.png")


                #cv2.imwrite("test_imgs/c2_back.png",back)
                    
                frames[x] = back
            
            #wait to allow time to throw
#            print ("Waiting for throw...")
            #time.sleep(5)

            #dart_1,dart_2 = capFrames(cameraStreams)
            
            dartIm = cv2.imread("test_imgs/c2_dart_"+str(dart)+".png")

            #cv2.imwrite("test_imgs/c2_dart_"+str(dart)+".png",dart)
        
            frames[dart] = dartIm
        
    except:
        print("Closing camera 2 stream.")
     #   cameraStreams.closeCamTwo()

#    print (c1_frames)
#    print (c2_frames)
#    print("Finding coordinates...")
    coords = find_coords.findCoordsMulti(frames)

    print (coords)
    return coords

if __name__=='__main__':
    main()
