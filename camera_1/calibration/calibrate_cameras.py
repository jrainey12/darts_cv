import numpy as np
import cv2
import glob
import pickle as pkl
import logging

def main():
    """
    Calibrate the stero cameras and save the paramaters to a pkl file.
    """
    logging.info("Calibrating stero cameras...")

    #focal length
    f = 3.6/0.0014
    #Principal point
    c_x,c_y = 640,360
    #horizonal translation
    #h_t = 800*f

    #camera intrinsic matrix
    intrinsic = np.array([[f,0,c_x],[0,f,c_y],[0,0,1]], np.int32)

    #Get object points from calib images for each camera
    #camera 1
    objpoints_1, imgpoints_1, img_1 = get_obj_img_points("1",intrinsic)

    #camera 2
    objpoints_2, imgpoints_2, img_2 = get_obj_img_points("2",intrinsic)

    #Get left, right, top and bottom calibration points
    #TODO: Automatically get points using segmentation method.

    #coords of four outer points. format: [[cam1 X,cam1 Y],[cam2 X,cam2 Y]].
    left = [[802,470],[475,493]]
    right = [[722,350],[575,376]]
    top = [[1202,384],[998,422]]
    bot = [[300,396],[98,405]]


    # Calibrate the cameras in stereo
    calib_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    calib_flags = cv2.CALIB_FIX_PRINCIPAL_POINT + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_USE_INTRINSIC_GUESS

    _,mtx_1,dist_1,mtx_2,dist_2, R,T,_,_ = cv2.stereoCalibrate(objpoints_1, imgpoints_1,imgpoints_2,intrinsic, None, intrinsic, None, img_1.shape[::-1], criteria=calib_criteria, flags=calib_flags )


    #Get rotation and projection matrices for stereo cameras. 
    #rect_flags=cv2.CALIB_ZERO_DISPARITY
    R1,R2,P1,P2,_,_,_ = cv2.stereoRectify(mtx_1,dist_1,mtx_2,dist_2,(1280,720),R,T)#,flags=rect_flags)

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

    logging.info("Calibration parameters saved to calib_params.pkl")



def get_obj_img_points(camera,intrinsic):
    """
    Perform calibration on a single camera.
    param: camera - index of the camera to be calibrated.
    return: camera parameter, object points, image points and gray image
    """
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)#[0:9,0:6]

    #square_size = 0.023
    #objp = objp * square_size

    # Lists to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob("calib_images_triang/calib_images/cam_"+ camera + "/*.jpg")
    #print(images)

    for fname in images:
        logging.debug(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        #Test sharpness of images
        _, sharp = cv2.estimateChessboardSharpness(gray,(9,6),corners)

        sh = 0
        for x in sharp:
            sh +=x[2]

        avg_sh = sh/len(sharp)
        logging.debug("sharpness:" + str(avg_sh))
        #check if average sharpness is under 3
        if avg_sh > 3:
            logging.debug("NOT SHARP ENOUGH!")

        # If found, add object points, image points (after refining them)
        if ret:
            logging.debug("TRUE")
            objpoints.append(objp)
            imgpoints.append(corners)



    cv2.destroyAllWindows()
   

    if logging.root.level == logging.DEBUG:

        logging.info("Calculating error...")

        #Calculate the error of the calibration points.
        mean_error = 0
        #get rvecs and tvecs
        ret,mtx,dist,rvecs,tvecs =cv2.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],intrinsic,None)

        #calculate calibration error
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error
        logging.debug("total error: " + str(mean_error/len(objpoints)))

    return objpoints,imgpoints,gray



if __name__=='__main__':
    
    logging.basicConfig(format='%(message)s',level=logging.INFO)

    main()
