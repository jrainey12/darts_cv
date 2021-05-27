import numpy as np
import cv2
import time
import pickle


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(cv2.CAP_PROP_FPS, 15)
    print ("FPS: ", cap.get(cv2.CAP_PROP_FPS))
    print("ex:", cap.get(cv2.CAP_PROP_EXPOSURE))
    #camera calibration

    ret, img_1 = cap.read()
    #camera 2
#    cam_1_p = pickle.load(open( "cam_1_640.pkl", "rb" ))
#    c1_h,  c1_w = img_1.shape[:2]
#    newcameramtx_1, roi_1=cv2.getOptimalNewCameraMatrix(cam_1_p[0],cam_1_p[1],(c1_w,c1_h),1,(c1_w,c1_h))


#    top = 200
#    left = 0
#    h = 100
#    w = roi_1[2]#1600 

#    line_start = (int(w/2),top+5)
#    line_end = (int(w/2),top+h-5)
    
    ret,cam = cap.read()
    # undistort
#    frame = cv2.undistort(cam, cam_1_p[0], cam_1_p[1], None, newcameramtx_1)
    # crop the image 
#    x_c1,y_c1,w_c1,h_c1 = roi_1
#    frame = frame[y_c1:y_c1+h_c1, x_c1:x_c1+w_c1]

#    frame = cv2.flip(frame,0)
    frame = cv2.flip(cam,0)


#    rectangle = cv2.rectangle(frame, (left,top), (left+w,top+h),(255,0,0),2)
   

#    line = cv2.line(frame,line_start,line_end,(0,255,0),2)
      
    cv2.imwrite("camera_2_preview.png",frame)

    while(True):
        # Capture frame-by-frame
        ret,cam = cap.read()
        # undistort
#        frame = cv2.undistort(cam, cam_1_p[0], cam_1_p[1], None, newcameramtx_1)
        # crop the image 
#        x_c1,y_c1,w_c1,h_c1 = roi_1
#        frame = frame[y_c1:y_c1+h_c1, x_c1:x_c1+w_c1]
#        frame = cv2.flip(frame,0)
        frame = cv2.flip(cam,0)


 
#        rectangle = cv2.rectangle(frame, (left,top), (left+w,top+h),(255,0,0),2)
#        line = cv2.line(frame,line_start,line_end,(0,255,0),2)
      
        cv2.imshow('frame',frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':

    main()

