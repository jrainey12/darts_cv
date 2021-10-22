from triangulate import main as triangulate
from Draw_board import main as draw
import logging
from test_find_coords_c1 import main as cam_1
#from camera_2.test_find_coords_c2 import main as cam_2
#from find_coords import FindCoords


def main():

    coords = [[[[457, 203]], [[718, 258]], [[747, 31]]], [[[355, 55]], [[363, 87]], [[252, 87]]]]



    cam_1_coords = coords[0]#cam_1()
    cam_2_coords = coords[1]#cam_2()

    print ("CAM 1:", cam_1_coords[0])
    print ("CAM 2:", cam_2_coords[0])


    d1_c1 = cam_1_coords[0][0]
    d1_c2 = cam_2_coords[0][0]
    print ("d1_c1:", d1_c1)
    d2_c1 = cam_1_coords[1][0]
    d2_c2 = cam_2_coords[1][0]

    d3_c1 = cam_1_coords[2][0]
    d3_c2 = cam_2_coords[2][0]


    if None in d1_c1 or None in d1_c2:
      
        print("Out of scoring area.")
        s_1 = [0,0]

    else:
   
        s_1 = triangulate(d1_c1,d1_c2)
    
    
    if None in d2_c1 or None in d2_c2:

        print("Out of scoring area.")
        s_2 = [0,0]

    else:

        s_2 = triangulate(d2_c1,d2_c2)

             
    if None in d3_c1 or None in d3_c1:
        
        print("Out of scoring area.")
        s_3 = [0,0]

    else:

        s_3 = triangulate(d3_c1,d3_c2)
     
   
    print(s_1,s_2,s_3)


#    score = triangulate([590, 232], [250, 250])
#    print (score)
#    score = triangulate([1007, 229], [1045, 186])
#    print (score)
    #draw(0,50)
    
if __name__=='__main__':

    logging.basicConfig(format='%(message)s',level=logging.INFO)

    main()

