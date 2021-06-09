import numpy as np
import cv2
from find_coords_c2 import FindCoords
#from triangulate import main as triangulate
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


                #cv2.imwrite("test_imgs/c1_back.png",back_1)
                    
                frames[x] = back
            
            #wait to allow time to throw
#            print ("Waiting for throw...")
            #time.sleep(5)

            #dart_1 = capFrames(cameraStreams)
            
            dartIm = cv2.imread("test_imgs/c2_dart_"+str(dart)+".png")
#            dartIm = cv2.imread("calib_imgs/test_dart_"+str(dart)+".jpg")
            #cv2.imwrite("test_imgs/c1_dart_"+str(dart)+".png",dart_1)
            
            frames[dart] = dartIm
        

        #    back_1 = cv2.imread("test_imgs/c1_back.png")
        #    dart_1 = cv2.imread("test_imgs/c1_dart_1.png")

        #    c1_x, c1_y = find_coords.findCoords(back_1,dart_1,1)

        #    back_2 = cv2.imread("test_imgs/c2_back.png")
        #    dart_2 = cv2.imread("test_imgs/c2_dart_1.png")
   
        #c2_x, c2_y = find_coords.findCoords(back_2,dart_2,2)

    except:
        print("Closing camera 2 stream.")
     #   cameraStreams.closeCamTwo()

#    print (c1_frames)
#    print (c2_frames)
#    print("Finding coordinates...")
    coords = find_coords.findCoordsMulti(frames)

    print(coords)
    #return coords    
#   cameraStreams.closeCamTwo()



def capFrames(cameraStreams):

    c1,c2 = cameraStreams.captureCalibFrame()
    
    return c1,c2

if __name__=='__main__':
    main()
