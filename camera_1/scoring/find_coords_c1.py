import cv2
import numpy as np
from skimage.metrics import structural_similarity
from multiprocessing import Process, Queue

class FindCoords():
    """
    Class for finding coordinates of darts from images.
    """
    def __init__(self):
        
        #bounds for image cropping (top,left, h, w)
        #cam 1
        #self.bounds = [150,0,530,1280]

        #cam 2
        self.bounds = [240,0,655,1280]

        self.Q = Queue()
 
    def findCoordsMulti(self,frames):
        """
        Find the coordinates a dart from a pair of dart images.
        param: frames - frames from camera.
        return: final_coords - list of the coordinates of each dart.
        """

        final_coords = [None,None,None]
        
        #Spawn each dart as a process
        jobs = []
        for d in range(3):
            print (d)
            p = Process(target=self.findDartCoords,args=(frames,d+1,))
            jobs.append(p)
            p.start()

        results = []
        for i,j in enumerate(jobs):
            results.append(self.Q.get())
            p.join()
           
        results.sort()
         
        for i,r in enumerate(results):
            final_coords[i] = r[1]
        
        return final_coords
        
    def findDartCoords(self,frames,dart):    
        """
        Find the coordinates for a single dart.
        param: frames - frames from camera.
        param: dart - dart to find coords of.
        """

        backFrame = self.cropFrame(frames[dart-1])
        dartFrame = self.cropFrame(frames[dart])
               
        cam = self.processFrames(backFrame, dartFrame,dart)
        
        #put result in queue
        self.Q.put((dart,[cam]))
        

    def processFrames(self,backFrame,dartFrame,dart):
        """
        Process a single pair of frames to determine the x,y coords.
        param: backFrame - background frame.
        param: dartFrame - frame containing dart.
        return: [x,y] - xy coords of dart from single cam.
        """
        #segment frames and get edges of dart.
        edges = self.segmentFrames(backFrame,dartFrame,dart)

        #use the edges to get the position from the contours 
        try:
            x,y = self.dartContours(edges, dartFrame,dart)
        except:
            #if dartContours fails return 0,0 for x and y.
            print ("FAILED!!")
            return [None,None]
        

        #adjust y coord for bounds
       # final_y = y + (720 - self.bounds[2])
        final_y = y + self.bounds[0]

        return [x,final_y]
   
    def cropFrame(self,frame):
        """
        Crop the frame to the bounds of the related camera.
        param: frame - frame to be cropped.
        return: outFrame - cropped frame.
        """

        outFrame = frame[self.bounds[0]:self.bounds[0]+self.bounds[2],
                self.bounds[1]:self.bounds[1]+self.bounds[3]].copy()

        return outFrame


    def findCoordsSingle(self,backFrame,dartFrame):
        """
        Find the coordinates a dart from a pair of dart images.
        param: backFrame - frame to be used as the background.
        param: dartFrame - frame containing the dart to be located.
        return: x,y - x and y coordinates of dart in dartFrame.
        """
          
        backFrame = backFrame[self.bounds[0]:self.bounds[0]+self.bounds[2],
                self.bounds[1]:self.bounds[1]+self.bounds[3]].copy()
        dartFrame = dartFrame[self.bounds[0]:self.bounds[0]+self.bounds[2],
                self.bounds[1]:self.bounds[1]+self.bounds[3]].copy()

        #segment frames and get edges of dart.
        edges = self.segmentFrames(backFrame,dartFrame,dart)

        #use the edges to get the position from the contours 
        try:
            x,y = self.dartContours(edges, dartFrame,dart)
        except:
            #if dartContours fails return 0,0 for x and y.
            print ("FAILED!!")
            return [None,None]

        #adjust y coord for bounds
        final_y = y + (720 - self.bounds[2])
        
    
        return [x,y]
        
        
    def segmentFrames(self, backFrame, dartFrame,dart):
        """
        Perform background subtraction and segmentation on the dart frame to 
        get a clean set of edges of the dart.
        param: backFrame - background frame.
        param: dartFrame - frame containing dart.
        return: edges - canny edges
        """
       
        #Convert both frames to grayscale
        grayBack = cv2.cvtColor(backFrame, cv2.COLOR_BGR2GRAY)
        grayDart = cv2.cvtColor(dartFrame, cv2.COLOR_BGR2GRAY)

        #get structural similarity of the two frames to show the differences.
        (_,diff) = structural_similarity(grayBack, grayDart, full=True)
        #diff = cv2.absdiff(grayBack,grayDart)

        #convert the diff output to a grayscale image
        diff_img = (diff*255).astype("uint8")
        diff_img_inv = np.invert(diff_img)
    
        cv2.imwrite("seg_out/"+str(dart)+"_1_diff_.jpg",diff_img)
        #cv2.imwrite("seg_out/21_diff_inv.jpg",diff_img_inv)

        #threshold the diff image
        th = np.mean(diff_img)/2
#        print (th)
        _,thresh = cv2.threshold(diff_img, 170, 255, cv2.THRESH_BINARY_INV)
        
        cv2.imwrite("seg_out/"+str(dart)+"_2_thresh_1.jpg",thresh)

        
        #perform morphological operations to create a mask.
        kernel_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6)) 
        op = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel_1,iterations=1)
        cl = cv2.morphologyEx(op,cv2.MORPH_CLOSE, kernel_1,iterations=4)

        cv2.imwrite("seg_out/"+str(dart)+"_2_thresh_morph.jpg",cl)
        
        #erode
        kernel_2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
        erode = cv2.erode(cl, kernel_2, iterations=3)
        #dilate
        kernel_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
        mask = cv2.dilate(erode, kernel_3,iterations=6)#6)

        cv2.imwrite("seg_out/"+str(dart)+"_3_mask_.jpg",mask)
        
        #remove noise outside of the mask
        cut = cv2.bitwise_and(thresh,thresh, mask=mask)
        
        cv2.imwrite("seg_out/"+str(dart)+"_4_cut.jpg",cut)
        
        #kernel_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))

        closing = cv2.morphologyEx(cut,cv2.MORPH_CLOSE,kernel_2,iterations=4)
        cv2.imwrite("seg_out/"+str(dart)+"_5_closing.jpg",closing)

        kernel_4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        out = cv2.erode(closing,kernel_4,iterations=2)
        cv2.imwrite("seg_out/"+str(dart)+"_6_erode.jpg",out)
     
        #Blur and canny edge detection
        #out = cv2.GaussianBlur(out,(3,3),0)
        #edges = cv2.Canny(out, 50, 150)
        
        #cv2.imwrite("seg_out/"+str(dart)+"_6_edges.jpg",edges)

        return out#edges


    def dartContours(self, edges, dartFrame,dart):
        """
        Find the contours from the edges and use bounding box to determine position.
        """
    
        #get contours and sort
        contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        c = max(contours,key=cv2.contourArea)
        
        #M = cv2.moments(c)
        
        #get bounding rectangle
        rect = cv2.minAreaRect(c)
        #print ("rect",rect)

        #draw rectangle on frame
        #box outputs 4 coords starting with the lowest and working clockwise.
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print ("box",box)
        
        #get second lowest y point
        #(the box if often slightly larger than the dart so getting the second
        #lowest y point give a closer result)  
   #     low = box[0]
   #     for x in box:
   #         if x[1] <= low[1]:
   #             low = x
   #             low_2 = low
   #         elif x[1] < low_2[1]:
   #             low_2 = x
        sorted_box = sorted(box, key=lambda x: x[1],reverse=True)
        #print (sorted_box)
        print(sorted_box[1])
        
        low_2 = sorted_box[1]

        if low_2[0] < box[0][0]:
            print("lowest on right")
            box_l = box[1][0]
            box_r = box[0][0]
            mid_x = box_l - int(abs(box_l - box_r)/2)

        else:
            print("lowest on left")
            #otherwise second lowest is box[3]
            box_l = box[0][0]
            box_r = box[3][0]
        
        mid_x = box_l + int(abs(box_l - box_r)/2)


        low_y = low_2[1]
        print ("Y:",low_y)

        #find mid point between lowest x points
        #box_l = box[0][0]
        #box_r = box[3][0]

               
        print("X:", mid_x)

        #draw the rectangle and a circle marking the point
        rectangle = cv2.drawContours(dartFrame,[box],0,(0,255,0),2)
        
        circle = cv2.circle(rectangle,(mid_x,low_y), 2, (0,0,255), 2)

        cv2.imwrite("seg_out/"+str(dart)+"_7_rectangle_"+str(dart)+".jpg",rectangle)
 
        #print("X centre: ", xcoord_cen, "Y centre: ", y+h)

        return mid_x, low_y



