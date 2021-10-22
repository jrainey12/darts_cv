import numpy as np
import cv2
import glob
import pickle as pkl
import logging

#TODO: Need to rewrite this and simplify it.
def main():
    """
    Calibrate the stero cameras and save the paramater to a pkl file.
    """
    
    #Perform calibration for each camera
    #TODO: Add a way to easily get frames for calibration.
    #Use solvePnP rather than calibrate
    #camera 1
    ret, mtx_1, dist_1, rvecs_1, tvecs_1, objpoints_1, imgpoints_1, img_1 = calibrate("1")
    #ret, mtx_1, dist_1, rvecs_1, tvecs_1, objpoints_1, imgpoints_1, img_1 = calibrate_circles("1")

    #camera 2
    ret_2, mtx_2, dist_2, rvecs_2, tvecs_2, objpoints_2, imgpoints_2, img_2 = calibrate("2")
    #ret_2, mtx_2, dist_2, rvecs_2, tvecs_2, objpoints_2, imgpoints_2, img_2 = calibrate_circles("2")

    #Get left, right, top and bottom points 
    #TODO: Automatically get points using segmentation method.


    #coords of four outer points. format: [[cam1 X,cam1 Y],[cam2 X,cam2 Y]].

#    left = [[707,527],[418,461]]
#    right = [[534,367],[641,322]]
#    top = [[1063,414],[1110,405]] 
#    bot = [[29,414],[96,323]]
    
    f = 3.6/0.0014
    c_x,c_y = 640,360
    h_t = 800*f

    intrinsic = np.array([[f,0,c_x],[0,f,c_y],[0,0,1]], np.int32)

    left = [[802,470],[475,493]]
    right = [[722,350],[575,376]]
    top = [[1202,384],[998,422]] 
    bot = [[300,396],[98,405]]

    # Calibrate the cameras in stereo
#mtx_1,dist_1,mtx_2,dist_2,R,T,_,_ = calibrate_stereo(mtx_1,dist_1,mtx_2,dist_2,
           # objpoints_1,imgpoints_1,imgpoints_2,img_1)
    mtx_1,dist_1,mtx_2,dist_2,R,T,_,_ = calibrate_stereo(intrinsic,dist_1,intrinsic,dist_2,
            objpoints_1,imgpoints_1,imgpoints_2,img_1)
    #Get rotation and projection matrices for stereo cameras. 
    rect_flags=cv2.CALIB_ZERO_DISPARITY
    R1,R2,P1,P2,_,_,_ = cv2.stereoRectify(mtx_1,dist_1,mtx_2,dist_2,(1280,720),R,T)#,flags=rect_flags)


    #P1 = np.array([[f,0,-c_x,0],[0,f,c_y,0],[0,0,1,0]],np.float32)
    #P2 = np.array([[f,0,-c_x,h_t],[0,f,c_y,0],[0,0,1,0]],np.float32)

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

    print(params)

def calibrate_stereo(mtx_1,dist_1,mtx_2,dist_2,objpoints,imgpoints_1,imgpoints_2,img_1):
    """
    Perform stereo calibration.
    """
    calib_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #calib_flags = cv2.CALIB_USE_INTRINSIC_GUESS
    #calib_flags = cv2.CALIB_FIX_INTRINSIC
    calib_flags = cv2.CALIB_FIX_PRINCIPAL_POINT + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_USE_INTRINSIC_GUESS
    
    #ret,mtx_1,dist_1,mtx_2,dist_2, R,T,E,F = cv2.stereoCalibrate(objpoints, imgpoints_1,imgpoints_2,mtx_1, dist_1, mtx_2, dist_2, img_1.shape[::-1], criteria=calib_criteria, flags=calib_flags )
    ret,mtx_1,dist_1,mtx_2,dist_2, R,T,E,F = cv2.stereoCalibrate(objpoints, imgpoints_1,imgpoints_2,mtx_1, None, mtx_2, None, img_1.shape[::-1], criteria=calib_criteria, flags=calib_flags )
    
    return mtx_1,dist_1,mtx_2,dist_2,R,T,E,F


def calibrate_circles(camera):
    """
    Perform calibration on a single camera using a circle pattern.
    """

    #termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

    #setup simple blob detector params
    blobParams = cv2.SimpleBlobDetector_Params()

    #Set Thresholds
    blobParams.minThreshold = 8
    blobParams.maxThreshold = 255

    #Filter by areas
    blobParams.filterByArea = True
    blobParams.minArea = 512 #Can be adjusted
    blobParams.maxArea = 2500 #Can be adjusted

    #Filter by circularity
#    blobParams.filterByCircularity = True
#    blobParams.minCircularity = 0.1

    #Filter by convexity
#    blobParams.filterByConvexity = True
#    blobParams.minConvexity = 0.87

    #Filter by Intertia
#    blobParams.filterByInertia = True
#    blobParams.minInertiaRatio = 0.01

    #Create a detector
    blobDetector = cv2.SimpleBlobDetector_create(blobParams)

    #Initialise blob coords
    objp = np.zeros((44, 3), np.float32)

    objp[0]  = (0  , 0  , 0)
    objp[1]  = (0  , 72 , 0)
    objp[2]  = (0  , 144, 0)
    objp[3]  = (0  , 216, 0)
    objp[4]  = (36 , 36 , 0)
    objp[5]  = (36 , 108, 0)
    objp[6]  = (36 , 180, 0)
    objp[7]  = (36 , 252, 0)
    objp[8]  = (72 , 0  , 0)
    objp[9]  = (72 , 72 , 0)
    objp[10] = (72 , 144, 0)
    objp[11] = (72 , 216, 0)
    objp[12] = (108, 36,  0)
    objp[13] = (108, 108, 0)
    objp[14] = (108, 180, 0)
    objp[15] = (108, 252, 0)
    objp[16] = (144, 0  , 0)
    objp[17] = (144, 72 , 0)
    objp[18] = (144, 144, 0)
    objp[19] = (144, 216, 0)
    objp[20] = (180, 36 , 0)
    objp[21] = (180, 108, 0)
    objp[22] = (180, 180, 0)
    objp[23] = (180, 252, 0)
    objp[24] = (216, 0  , 0)
    objp[25] = (216, 72 , 0)
    objp[26] = (216, 144, 0)
    objp[27] = (216, 216, 0)
    objp[28] = (252, 36 , 0)
    objp[29] = (252, 108, 0)
    objp[30] = (252, 180, 0)
    objp[31] = (252, 252, 0)
    objp[32] = (288, 0  , 0)
    objp[33] = (288, 72 , 0)
    objp[34] = (288, 144, 0)
    objp[35] = (288, 216, 0)
    objp[36] = (324, 36 , 0)
    objp[37] = (324, 108, 0)
    objp[38] = (324, 180, 0)
    objp[39] = (324, 252, 0)
    objp[40] = (360, 0  , 0)
    objp[41] = (360, 72 , 0)
    objp[42] = (360, 144, 0)
    objp[43] = (360, 216, 0)

    objpoints = []
    imgpoints = []

    images = sorted(glob.glob("calib_images_triang/calib_images/circles/v1/cam_"+ camera + "/*.jpg"))
    for fname in images:
        print(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #Detect blobs
        keypoints = blobDetector.detect(gray)

        #Draw blobs as red circles
        im_with_keypoints = cv2.drawKeypoints(img,keypoints,np.array([]), (0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints_gray = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
        #find the circle grid
        ret, corners = cv2.findCirclesGrid(im_with_keypoints, (4,11), None, flags = cv2.CALIB_CB_ASYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING)
        print (ret)
        if ret:

            objpoints.append(objp)
            
            #corners2 = cv2.cornerSubPix(im_with_keypoints_gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)#2)

            im_with_keypoints = cv2.drawChessboardCorners(img, (4,11), corners,ret)#corners2

            #cv2.imshow("img", im_with_keypoints)
            #cv2.waitKey(500)
    #print("Getting camera params...")
    #focal length in pixels
    f = 3.6/0.0014
    c_x,c_y = 640,360
    #camera intrinsic matrix
    intrinsic = np.array([[f,0,c_x],[0,f,c_y],[0,0,1]], np.int32)
    print("intrinsic", intrinsic)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],intrinsic,None,flags=cv2.CALIB_FIX_PRINCIPAL_POINT + cv2.CALIB_FIX_FOCAL_LENGTH)
    #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],None,None)
    #print("calculating error...")
    #Calculate the error of the calibration points.
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
        print(mean_error)
    logging.debug("total error: " + str(mean_error/len(objpoints)))
    
    print("intrinsic2", mtx)

    return ret,mtx,dist,rvecs,tvecs,objpoints,imgpoints,gray

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
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)#[0:9,0:6]

    square_size = 0.023
    #objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob("calib_images_triang/calib_images/cam_"+ camera + "/*.jpg")
    #print(images)
    for fname in images:
        logging.info(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points (after refining them)
        if ret:
            logging.debug("TRUE")
            objpoints.append(objp)

            #corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)#2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9,6), corners,ret)#corners2
            #cv2.imshow('img',img)
            #cv2.imwrite("calib_images/calib_img.jpg",img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()
   
    logging.info("Calculating error..") 
    #Calculate the error of the calibration points.
    mean_error = 0

    f = 3.6/0.0014
    c_x,c_y = -640,360

    intrinsic = np.array([[f,0,c_x],[0,f,c_y],[0,0,1]], np.int32)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],intrinsic,None)

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
        logging.debug("Error: " + str(mean_error))
    logging.debug("total error: " + str(mean_error/len(objpoints)))

    return ret,mtx,dist,rvecs,tvecs,objpoints,imgpoints,gray



if __name__=='__main__':
    
    logging.basicConfig(format='%(message)s',level=logging.DEBUG)

    main()
