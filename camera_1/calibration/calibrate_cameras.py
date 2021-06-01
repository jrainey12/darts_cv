import numpy as np
import cv2
import glob
import pickle as pkl
import logging

def main():
    """
    Calibrate the stero cameras and save the paramater to a pkl file.
    """
    
    #Perform calibration for each camera
    #TODO: Add a way to easily get frames for calibration.
    #camera 1
    ret, mtx_1, dist_1, rvecs_1, tvecs_1, objpoints_1, imgpoints_1, img_1 = calibrate("1")
    
    #camera 2
    ret_2, mtx_2, dist_2, rvecs_2, tvecs_2, objpoints_2, imgpoints_2, img_2 = calibrate("2")
    
    #Get left, right, top and bottom points 
    #TODO: Automatically get points using segmentation method.


    #coords of four outer points. format: [[cam1 X,cam1 Y],[cam2 X,cam2 Y]].
#    left = [[874,485],[554,532]]
#    right = [[622,337],[717,378]]
#    top = [[1177,393],[1236,458]] 
#    bot = [[146,379],[174,408]]

    c1_bounds = [150,0,530,1280]
    c2_bounds = [240,0,655,1280]

#    left = [[886,349],[571,288]]
#    right = [[631,165],[714,117]]    
#    top = [[1188,239],[1239,213]]
#    bot = [[161,210],[175,115]]

    left = [[886,349],[571,288]]
    right = [[631,165],[714,117]]    
    top = [[1188,239],[1239,213]]
    bot = [[161,210],[175,115]]



    # Calibrate the cameras in stereo
    mtx_1,dist_1,mtx_2,dist_2,R,T,_,_ = calibrate_stereo(mtx_1,dist_1,mtx_2,dist_2,
            objpoints_1,imgpoints_1,imgpoints_2,img_1)
   

    #Get rotation and projection matrices for stereo cameras. 
    R1,R2,P1,P2,_,_,_ = cv2.stereoRectify(mtx_1,dist_1,mtx_2,dist_2,(1280,720),R,T)

    params = { "left" : left,
             "right" : right,
             "top" : top,
             "bot" : bot,
             "mtx_1" : mtx_1,
             "dist_1" : dist_1,
             "mtx_2" : mtx_2,
             "dist_2" : dist_2,
             "R1" : R1,
             "P1" : P1,
             "R2" : R2,
             "P2" : P2}

    pkl.dump(params, open("calib_params.pkl", 'wb'))

    logging.info("Parameters saved to calib_params.pkl")

def calibrate_stereo(mtx_1,dist_1,mtx_2,dist_2,objpoints,imgpoints_1,imgpoints_2,img_1):
    """
    Perform stereo calibration.
    """
    calib_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    calib_flags = cv2.CALIB_FIX_INTRINSIC
    
    ret,mtx_1,dist_1,mtx_2,dist_2, R,T,E,F = cv2.stereoCalibrate(objpoints, imgpoints_1,imgpoints_2,mtx_1, dist_1, mtx_2, dist_2, img_1.shape[::-1], criteria=calib_criteria, flags=calib_flags )
    
    
    return mtx_1,dist_1,mtx_2,dist_2,R,T,E,F


def calibrate(camera):
    """
    Perform calibration on a single camera.
    param: camera - index of the camera to be calibrated.
    return: camera parameter, object points, image points and gray image
    """
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob("calib_images/test/cam_"+ camera + "/*.jpg")
    #print(images)
    for fname in images:
        logging.info(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            logging.debug("TRUE")
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            #img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
            #cv2.imshow('img',img)
            #cv2.imwrite("calib_images/calib_img.jpg",img)
            #cv2.waitKey(500)

    #cv2.destroyAllWindows()
   
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    
    #Calculate the error of the calibration points.
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    logging.debug("total error: " + str(mean_error/len(objpoints)))
    

    return ret,mtx,dist,rvecs,tvecs,objpoints,imgpoints,gray



if __name__=='__main__':
    
    logging.basicConfig(format='%(message)s',level=logging.INFO)

    main()
