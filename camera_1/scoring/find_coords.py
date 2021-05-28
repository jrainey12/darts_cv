import cv2
import numpy as np
from skimage.metrics import structural_similarity

class FindCoords():
    """
    Class for finding coordinates of darts from images.
    """
    def __init__(self):
        
        #bounds for image cropping (top,left, h, w)
        self.c1_bounds = [150,0,530,1280]
        self.c2_bounds = [240,0,655,1280]

    
    def findCoords(self,backFrame,dartFrame,cam):
        """
        Find the coordinates a dart from a pair of darts.
        param: backFrame - frame to be used as the background.
        param: dartFrame - frame containing the dart to be located.
        param: cam - idx of camera, 1 or 2.
        return: x,y - x and y coordinates of dart in dartFrame.
        """
   
        #Select appropriate bounds for camera.
        if cam == 1:
            
            bounds = self.c1_bounds

        else:

            bounds = self.c2_bounds


        backFrame = backFrame[bounds[0]:bounds[0]+bounds[2],
                    bounds[1]:bounds[1]+bounds[3]].copy()
        dartFrame = dartFrame[bounds[0]:bounds[0]+bounds[2],
                    bounds[1]:bounds[1]+bounds[3]].copy()

        #segment frames and get edges of dart.
        edges = self.segmentFrames(backFrame,dartFrame,cam)

        #use the edges to get the position from the contours 
        try:
            x,y = self.dartContours(edges, dartFrame, cam)
        except:
            #if dartContours fails return 0,0 for x and y.
            print ("FAILED!!")
            return 0,0

        return x,y
        
        
    def segmentFrames(self, backFrame, dartFrame,cam):
        """
        Perform background subtraction and segmentation on the dart frame to 
        get a clean set of edges of the dart.
        param: backFrame - background frame.
        param: dartFrame - frame containing dart.
        return: edges - canny edges
        """
       
        #TODO: Look into methods of feature extraction.

        #Convert both frames to grayscale
        grayBack = cv2.cvtColor(backFrame, cv2.COLOR_BGR2GRAY)
        grayDart = cv2.cvtColor(dartFrame, cv2.COLOR_BGR2GRAY)

        #get structural similarity of the two frames to show the differences.
        (_,diff) = structural_similarity(grayBack, grayDart, full=True)
     
        #convert the diff output to a grayscale image
        diff_img = (diff*255).astype("uint8")
        diff_img_inv = np.invert(diff_img)
    
        cv2.imwrite("seg_out/"+str(cam)+"0_diff_.jpg",diff_img)
        cv2.imwrite("seg_out/"+str(cam)+"1_diff_inv.jpg",diff_img_inv)

        #threshold the diff image
        th = np.mean(diff_img)/2
        print (th)
        _,thresh = cv2.threshold(diff_img, 170, 255, cv2.THRESH_BINARY_INV)
        
        cv2.imwrite("seg_out/"+str(cam)+"2_thresh_1.jpg",thresh)

        
        #perform morphological operations to create a mask.
        kernel = np.ones((3,3), np.uint8)
        kernel_2 = np.ones((10,10),np.uint8)
        ero = cv2.erode(thresh, kernel,iterations=2)
        #ero = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel,iterations=5)
        mask = cv2.dilate(ero, kernel_2,iterations=2)

        cv2.imwrite("seg_out/"+str(cam)+"3_mask_.jpg",mask)
        #remove noise outside of the mask
        cut = cv2.bitwise_and(thresh,thresh, mask=mask)
        
        cv2.imwrite("seg_out/"+str(cam)+"4_cut.jpg",cut)
        
        kernel_4 = np.ones((4,4),np.uint8)
        closing = cv2.morphologyEx(cut,cv2.MORPH_CLOSE,kernel_4,iterations=2)
        opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel_4,iterations=2)

        cv2.imwrite("seg_out/"+str(cam)+"5_closing.jpg",opening)

        #Blur and canny edge detection
        #img = cv2.GaussianBlur(opening,(3,3),0)
        edges = cv2.Canny(opening, 50, 150)
        
        cv2.imwrite("seg_out/"+str(cam)+"6_edges.jpg",edges)

        return edges


    def dartContours(self, edges, dartFrame,cam):
        """
        Find the contours from the edges and use bounding box to determine position.
        """
    
        #get contours and sort
        contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        for c in sorted_contours:
            print (cv2.contourArea(c))

        print ("C",cv2.contourArea(sorted_contours[0]))
      
        print (len(sorted_contours))
        #get largest and calc moments
        if cam == 1:
            largest_item = sorted_contours[0]
        else:
            largest_item = sorted_contours[-1]
        M = cv2.moments(largest_item)
        #get bounding rectangle
        rect = cv2.minAreaRect(largest_item)
        
        x,y,w,h = cv2.boundingRect(largest_item)

        #find x and y coord centres
        xcoord1 = x
        xcoord2 = x + w
        xcoord_cen = int(M['m10']/M['m00'])

        ycoord1 = y
        ycoord2 = y + h
        ycoord_cen = int(M['m01']/M['m00'])
 
        #draw rectangle on frame
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print (box)
        cir_x = box[2][0]
        print (cir_x)
        circle = cv2.circle(dartFrame,(cir_x ,y+h), 5, (0,0,255), 2)

        rectangle = cv2.drawContours(circle,[box],0,(0,255,0),2)
        
        cv2.imwrite("seg_out/"+str(cam)+"6_rectangle.jpg",rectangle)
 
        print("X centre: ", xcoord_cen, "Y centre: ", y+h)

        return cir_x, y+h #ycoord_cen



