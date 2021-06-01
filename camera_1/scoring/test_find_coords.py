import numpy as np
import cv2
from find_coords import FindCoords
from triangulate import main as triangulate
from camera_streams import CameraStreams
import time

def main():

    find_coords = FindCoords()
    #cameraStreams = CameraStreams()

#    cameraStreams.startCamTwoStream()   
#    time.sleep(3)
#    cameraStreams.connectCamTwo()
    
    c1_frames = [None,None,None,None]
    c2_frames = [None,None,None,None]

    try:

        for x in range(3):
            print (x)
            dart = x+1
            print("dart:",dart)
            if x == 0:
                
                #back_1,back_2 = capFrames(cameraStreams) 
                
                back_1 = cv2.imread("test_imgs/c1_back.png")
                back_2 = cv2.imread("test_imgs/c2_back.png")


                #cv2.imwrite("test_imgs/c1_back.png",back_1)
                #cv2.imwrite("test_imgs/c2_back.png",back_2)
                    
                c1_frames[x] = back_1
                c2_frames[x] = back_2
            
            #wait to allow time to throw
#            print ("Waiting for throw...")
            #time.sleep(5)

            #dart_1,dart_2 = capFrames(cameraStreams)
            
            dart_1 = cv2.imread("test_imgs/c1_dart_"+str(dart)+".png")
            dart_2 = cv2.imread("test_imgs/c2_dart_"+str(dart)+".png")

            #cv2.imwrite("test_imgs/c1_dart_"+str(dart)+".png",dart_1)
            #cv2.imwrite("test_imgs/c2_dart_"+str(dart)+".png",dart_2)
            
            c1_frames[dart] = dart_1
            c2_frames[dart] = dart_2
        

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
    print("Finding coordinates...")
    coords = find_coords.findCoordsMulti(c1_frames,c2_frames)

#    print(coords)

    s_1 = triangulate(coords[0][0],coords[0][1])
    s_2 = triangulate(coords[1][0],coords[1][1])
    s_3 = triangulate(coords[2][0],coords[2][1])

    print(s_1,s_2,s_3)
#  cameraStreams.closeCamTwo()
 
#    score = triangulate([c1_x,c1_y],[c2_x,c2_y])

 #   print (score)

def capFrames(cameraStreams):

    c1,c2 = cameraStreams.captureCalibFrame()
    
    return c1,c2

if __name__=='__main__':
    main()
