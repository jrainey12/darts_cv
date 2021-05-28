import numpy as np
import cv2
from find_coords import FindCoords
from triangulate import main as triangulate

def main():

    find_coords = FindCoords()

    coords =[None,None,None,None]

    back = cv2.imread("test_imgs/c1_back.png")
    dart = cv2.imread("test_imgs/c1_dart_1.png")
    c1_x, c1_y = find_coords.findCoords(back,dart,1)

    back_2 = cv2.imread("test_imgs/c2_back.png")
    dart_2 = cv2.imread("test_imgs/c2_dart_1.png")
    c2_x, c2_y = find_coords.findCoords(back_2,dart_2,2)

 
#    score = triangulate([c1_x,c1_y],[c2_x,c2_y])

#    print (score)

if __name__=='__main__':
    main()
