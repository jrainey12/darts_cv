import cv2 import numpy as np

def main():


    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    for x in range(10):

        ret,cam = cap.read()

    frame = cam.copy()
    
    cap.release()

    cv2.imwrite(frame, "triang_out/frame.jpg")



if __name__=='__main__':
    main()
