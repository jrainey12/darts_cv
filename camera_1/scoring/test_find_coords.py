from find_coords_single import main as find_coords
import cv2
from triangulate import main as triangulate

def main():

    c1_frames = []
    c2_frames = []

    c1_frames.append(cv2.imread("calib_images/test/test_frame_1.jpg"))
    c1_frames.append(cv2.imread("calib_images/test/back_1.jpg"))
    c2_frames.append(cv2.imread("calib_images/test/test_frame_2.jpg"))
    c2_frames.append(cv2.imread("calib_images/test/back_2.jpg"))
    
    
    find_coords(c1_frames, c2_frames, 1)

    triangulate()    


if __name__=='__main__':

    main()
