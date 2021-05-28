import cv2
import numpy as np
from scoring.Draw_board import main as board
from skimage.metrics import structural_similarity

#TODO: Rewrite this more cleanly.


def main(c1_frames,c2_frames):
    """
    Get the pixel location of the dart from each camera for a single dart.
    param: c1_frames - list containing background and dart frame from camera 1.
    param: c2_frames - list containing background and dart frame from camera 2.
    return: ([c1_x,c1_y],[c2_x,c2_y]) - tuple of the xy coordinates of the darts
    from the two cameras.
    """
   
    top = 150 
    left = 0
    h = 530
    w = 1280

    top_2 = 240
    left_2 = 0
    h_2 = 655
    w_2 = 1280

   #Get the dart  coords
    
    #DART
    d1_c1 = [c1_frames[0],c1_frames[1]]
    d1_c2 = [c2_frames[0],c2_frames[1]]
    # Dart  X COORD
    c1_x,c1_y = get_coord(d1_c1[0][top:top+h,left:left+w],d1_c1[1][top:top+h,left:left+w].copy(),1)
    # Dart  Y COORD
    c2_x,c2_y = get_coord(d1_c2[0][top_2:top_2+h_2,left_2:left_2+w_2],d2_c2[1][top_2:top_2+h_2,left_2:left_2+w_2].copy(),1)

    #if c1_x == None or c2_x == None:
    #    c1_x = 1280
    #    c1_y = 0
    #    c2_x = 0
    #    c2_y = 0

    print ("Dart Coords: ", c1_x,c1_y,c2_x, c2_y)

    d_score = triangulate([c1_x,c1_y],[c2_x, c2_y])

    return d_score
    
def get_coord(frame_1, frame_2, dart):

    """
    Segment the dart, clean up the image and detect the edges.
    """
    #diff_img = cv2.absdiff(cv2.cvtColor(frame_1,cv2.COLOR_BGR2GRAY),cv2.cvtColor(frame_2,cv2.COLOR_BGR2GRAY))
    grayA = cv2.cvtColor(frame_1,cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(frame_2,cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff_img = (diff * 255).astype("uint8")
    diff_img_2 = np.invert(diff_img)

    th = np.mean(diff_img)/2
    ret, thresh = cv2.threshold(diff_img,th,255,cv2.THRESH_BINARY_INV)
    
    cv2.imwrite("seg_out/thresh"+str(dart)+".jpg",thresh)

    m_kernel = np.ones((5,5),np.uint8)
    m_kernel_2 = np.ones((15,15),np.uint8)
    #m_kernel_3 = np.ones((20,20),np.uint8)
    mask = cv2.erode(thresh, m_kernel)
    #mask_2 = cv2.erode(mask,m_kernel)
    mask_3 = cv2.dilate(mask, m_kernel_2)
    #mask_4 = cv2.erode(mask_3,m_kernel_3)
   # mask_3 = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,m_kernel_2,iterations=5)
    cut = cv2.bitwise_and(diff_img_2, diff_img_2, mask=mask_3)
    ret, thresh_2 = cv2.threshold(cut,100,255,cv2.THRESH_BINARY)

    kernel_2 = np.ones((5,5),np.uint8)
    #dilate = cv2.dilate(thresh_2,kernel_2)
    kernel_3 = np.ones((2,2),np.uint8)
    ero_1 = cv2.erode(thresh_2, kernel_3)
    closing = cv2.morphologyEx(ero_1,cv2.MORPH_CLOSE,kernel_2,iterations=4)
    #out = cv2.erode(closing, kernel_2)
    #out_2 = cv2.morphologyEx(out,cv2.MORPH_CLOSE,kernel_3,iterations=4)
    img = cv2.GaussianBlur(closing,(3,3),0)
    edges = cv2.Canny(img, 50,150)
    #cv2.imshow("edges",edges)
    cv2.imwrite("seg_out/edges_"+str(dart)+"_.png",edges)
    try:
        xcoord,ycoord = contours(edges,diff_img_2,frame_2)
    except:
        return None,None
    return xcoord,ycoord#, edges

def contours(thresh,image,img_2):
    """
    Find the contours from the edges of the dart and use the bounding box of the contours
    to determine the coordinates of the dart.
    """
    #TODO: Improve this process to account for dart angle.

    contours, hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)#False)

    print(len(sorted_contours))

    largest_item= sorted_contours[-1]

    #print(largest_item)

    M = cv2.moments(largest_item)
    #print (M)
    x,y,w,h = cv2.boundingRect(largest_item)

    y = int(h - h/3)
    h = int((h/3))
    
    print (x,y,w,h)

    xcoordinate1 = x 
    xcoordinate2 = x + w
    xcoordinate_center = int(M['m10']/M['m00'])

    ycoordinate1 = y 
    ycoordinate2 = y + h
    ycoordinate_center= int(M['m01']/M['m00'])

    rectangle = cv2.rectangle(image, (x,y), (x+w,y+h),(255,0,0),2)

    #cv2.imshow("rect", rectangle)
    #print("y coordinate 1: ", str(ycoordinate1))
    #print("y coordinate 2: ", str(ycoordinate2))
    #print("y center coordinate ", str(ycoordinate_center))
    print("X centre: ", xcoordinate_center, " Y centre: ", ycoordinate_center)

#    start = (xcoordinate_center,ycoordinate_center-50)
#    end = (xcoordinate_center,ycoordinate_center+50)
#    image_cen = cv2.line(img_2,start,end,(255,0,0),4)

    #cv2.imshow("centre", image_cen)
    cv2.imwrite("seg_out/centre.jpg",rectangle)
    print(image_cen.shape)
    #final_coord = (xcoordinate_center, ycoordinate_center)#/(image_cen.shape[1]))*100
    #print ("Final Position: ", final_coord)

    return xcoordinate_center,ycoordinate_center# final_coord


if __name__=='__main__':
    
    main()
