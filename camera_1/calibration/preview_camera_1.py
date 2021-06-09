import cv2
import time

def main():

    #capture cam 1
    cam = cv2.VideoCapture(0)
    cam.set(3,1280)
    cam.set(4,720)
    
    time.sleep(5)

    _,frame = cam.read()
    img = cv2.flip(frame,0)

    cv2.imwrite("calib_images/frame_10.jpg", img)
    cam.release()

if __name__=='__main__':


    main()

