import cv2
import time


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    time.sleep(5)

    _, frame = cap.read()
    img = cv2.flip(frame,0)
      
    cv2.imwrite("calib_images/frame_10.jpg",img)
    cap.release()

if __name__=='__main__':

    main()

