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
        
#        self.c1_bounds = [0,0,720,1280]
#        self.c2_bounds = [0,0,720,1280]
 
    def findCoordsMulti(self,c1_frames,c2_frames):
        """
        Find the coordinates a dart from a pair of dart images.
        param: c1_frames - frames from camera 1.
        param: dartFrame - frames from camera 2.
        return: final_coords - list of the coordinates of each dart.
        """

        #TODO:Add multi-threading. Spawn each findDartCoords
        #in a new thread.
        final_coords = [None,None,None]

        for d in range(3):
            print (d)
            final_coords[d] = self.findDartCoords(c1_frames,c2_frames,d+1)

        return final_coords
        
    def findDartCoords(self,c1_frames,c2_frames,dart):    
        """
        Find the coordinates for a single dart.
        param: c1_frames - frames from cam 1.
        param: c2_frames - frames from cam 2.
        param: dart - dart to find coords of.
        return: [cam_1,cam_2] - xy coords for cams 1 and 2. 
        """

        backFrame_1 = self.cropFrame(c1_frames[dart-1],1)
        backFrame_2 = self.cropFrame(c2_frames[dart-1], 2)
        dartFrame_1 = self.cropFrame(c1_frames[dart],1)
        dartFrame_2 = self.cropFrame(c2_frames[dart],2)
               
        cam_1 = self.processFrames(backFrame_1, dartFrame_1,1)
        cam_2 = self.processFrames(backFrame_2, dartFrame_2,2)

        return [cam_1,cam_2]

    def processFrames(self,backFrame,dartFrame,cam):
        """
        Process a single pair of frames to determine the x,y coords.
        param: backFrame - background frame.
        param: dartFrame - frame containing dart.
        param: cam - index of cam used.
        return: [x,y] - xy coords of dart from single cam.
        """
        #segment frames and get edges of dart.
        edges = self.segmentFrames(backFrame,dartFrame,cam)

        #use the edges to get the position from the contours 
        try:
            x,y = self.dartContours(edges, dartFrame, cam)
        except:
            #if dartContours fails return 0,0 for x and y.
            print ("FAILED!!")
            return [0,0]
            
        if cam == 1:
            bounds = self.c1_bounds
        else:
            bounds = self.c2_bounds

        #adjust y coord for bounds
        final_y = y + (720 - bounds[2])
        
        return [x,y]
   
    def cropFrame(self,frame,cam):
        """
        Crop the frame to the bounds of the related camera.
        param: frame - frame to be cropped.
        param: cam - index of cam bounds to be used.
        return: outFrame - cropped frame.
        """
        #Select appropriate bounds for camera.
        if cam == 1:
            
            bounds = self.c1_bounds

        else:

            bounds = self.c2_bounds
        
        print(type(frame))

        outFrame = frame[bounds[0]:bounds[0]+bounds[2],
                bounds[1]:bounds[1]+bounds[3]].copy()

        return outFrame

    def findCoordsSingle(self,backFrame,dartFrame,cam):
        """
        Find the coordinates a dart from a pair of dart images.
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

        #adjust y coord for bounds
        final_y = y + (720 - bounds[2])
        
    
        return [x,y]
        
        
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
    
#        cv2.imwrite("seg_out/"+str(cam)+"0_diff_.jpg",diff_img)
#        cv2.imwrite("seg_out/"+str(cam)+"1_diff_inv.jpg",diff_img_inv)

        #threshold the diff image
        th = np.mean(diff_img)/2
        print (th)
        _,thresh = cv2.threshold(diff_img, 170, 255, cv2.THRESH_BINARY_INV)
        
#        cv2.imwrite("seg_out/"+str(cam)+"2_thresh_1.jpg",thresh)

        
        #perform morphological operations to create a mask.
        kernel = np.ones((3,3), np.uint8)
        #kernel_2 = np.ones((10,10),np.uint8)
        kernel_2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)) 
        op = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel_2)
        cl = cv2.morphologyEx(op,cv2.MORPH_CLOSE, kernel_2,iterations=1)

#        cv2.imwrite("seg_out/"+str(cam)+"2_thresh_morph.jpg",cl)
        mask = cv2.dilate(cl, kernel_2,iterations=6)

#        cv2.imwrite("seg_out/"+str(cam)+"3_mask_.jpg",mask)
        
        #remove noise outside of the mask
        cut = cv2.bitwise_and(thresh,thresh, mask=mask)
        
#        cv2.imwrite("seg_out/"+str(cam)+"4_cut.jpg",cut)
        
        kernel_4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
        closing = cv2.morphologyEx(cut,cv2.MORPH_CLOSE,kernel_4,iterations=4)
        opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel_4,iterations=2)
        out = cv2.erode(opening,kernel_4,iterations=2)
        cv2.imwrite("seg_out/"+str(cam)+"5_closing.jpg",out)#opening)

        #Blur and canny edge detection
        #img = cv2.GaussianBlur(opening,(3,3),0)
        edges = cv2.Canny(out, 50, 150)
        
#        cv2.imwrite("seg_out/"+str(cam)+"6_edges.jpg",edges)

        return edges


    def dartContours(self, edges, dartFrame,cam):
        """
        Find the contours from the edges and use bounding box to determine position.
        """
    
        #get contours and sort
        contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
 #       sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
 #       print ("AREA: ")
 #       for c in contours:
 #           print (cv2.contourArea(c))

        #print ("C",cv2.contourArea(sorted_contours[0]))
      
        #print (len(sorted_contours))
        #get largest and calc moments
        #if cam == 1:
        #    c = sorted_contours[1]
        #else:
        #    c = sorted_contours[-1]

        c = max(contours,key=cv2.contourArea)
        #c = contours[2]
#        print ("C: ",cv2.contourArea(c))
        M = cv2.moments(c)
        #get bounding rectangle
        rect = cv2.minAreaRect(c)
        #print ("rect",rect)
        #x,y,w,h = cv2.boundingRect(c)
        #print ("XZ", x,y,w,h)
        x,y,w,h = int(rect[0][0]),int(rect[0][1]),int(rect[1][0]),int(rect[1][1])
        print ("XYWH", x,y,w,h)
        
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
        print ("box",box)
       
        cir_x = box[2][0]
        print ("X:",cir_x)
       
        cir_y = tuple(c[c[:,:,1].argmax()][0])
        print ("Y:",cir_y) 
        
        
        rectangle = cv2.drawContours(dartFrame,[box],0,(0,255,0),2)
        
        circle = cv2.circle(rectangle,(xcoord_cen,cir_y[1]), 2, (0,0,255), 2)

        cv2.imwrite("seg_out/"+str(cam)+"6_rectangle.jpg",rectangle)
 
        print("X centre: ", xcoord_cen, "Y centre: ", y+h)

        return xcoord_cen, cir_y[1]



