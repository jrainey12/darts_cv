import numpy as np
import cv2
import math
import argparse

#TODO: Rewrite this more cleanly.

def main(x,y):
    """
    Draw a mockup of a dart board, determine the location of a detected dart
    and calculate the score of the dart.
    """
    width = 800
    height = 800
  

    #sector numbers
    nums = [10,15,2,17,3,19,7,16,8,11,14,9,12,5,20,1,18,4,13,6]

    img = np.zeros((width,height,3), np.uint8)
#    total_h = 40
    total_h = 45
    mults = [int((17/total_h)*width),
            int((16/total_h)*width),
            int((10.5/total_h)*width),
            int((9.5/total_h)*width),
            int((1.625/total_h)*width),
            int((0.75/total_h)*width)] 

    #Scale the values to the outer double size.
    scalar = (mults[0]*2)/100
#    diff = 4 - scalar/2
    #print ("Scalar: ", scalar, "Diff: ", diff)

#    point = (np.float32(((100-x)*scalar)+(100*diff)), np.float32(((100-y)*scalar)+(100*diff))) 
 
    flat_diff = 60
    x = np.float32(((100-x)*scalar)+flat_diff)
    y = np.float32(((100-y)*scalar)+flat_diff)     

    point = (x,y)
    point_v = (point[0]-(width/2), point[1]-(width/2))
    print ("POINT: ",point, "Point_v: ", point_v)

    sectorangle = 2 * math.pi / 20  

    c_x = int(width/2)
    c_y = int(height/2)

    #print(c_x, c_y)
    
    #Draw mult circles

    #outer double
    cv2.circle(img, (c_x, c_y), mults[0], (255, 255, 255), 1)
    #inner double
    cv2.circle(img, (c_x, c_y), mults[1], (255, 255, 255), 1)
    #outer triple
    cv2.circle(img, (c_x, c_y), mults[2], (255, 255, 255), 1)
    #inner triple
    cv2.circle(img, (c_x, c_y), mults[3], (255, 255, 255), 1)
    #25 outer
    cv2.circle(img, (c_x, c_y), mults[4], (255, 255, 255), 1)
    #Bullseye
    cv2.circle(img, (c_x, c_y), mults[5], (255, 255, 255), 1)

    lines = []

    #Draw sector lines on the board
    i = 0
    while (i < 20):
        start = (c_x,c_y)
        end = (int(c_x + mults[0] * math.cos((0.5 + i) * sectorangle)),int(c_y + mults[0] * math.sin((0.5 + i) * sectorangle)))
        line_v = (start[0] - end[0],start[1]-end[1])
        cv2.line(img, start, end, (255, 255, 255), 1)
        lines.append([start,end,line_v])
        i = i + 1

    #cv2.line(img, lines[0][0], lines[0][1], (0, 255, 0), 1)

    #find sector in which the point lies
    sector = 0
    for i in range(0,len(lines)):
        #print (i)
        line_1 = lines[i]
        if i < 19:
            line_2 = lines[i+1]
        else:
            line_2 = lines[0]
        #print (line_1)
        #print(line_2)
        #if clockwise of line one and counterclockwise of line two
        # then the sector is found
        if clockwise(line_1[2],point_v):
         #   print ("clockwise") 
         #   print(i)
            cv2.line(img, line_1[0], line_1[1], (255, 0, 0), 1)
            if not clockwise(line_2[2], point_v):
          #      print ("counterclockwise")
                cv2.line(img, line_2[0], line_2[1], (0, 0, 255), 1)
                sector = nums[i]
                break

    print("Sector: ", sector)
    
    #get multiplier
    mult = get_mult(point_v, mults)

    print("Multiplier: ", mult)

    #calculate final score
    if mult < 25: 
        score = sector*mult

    else:
        score = mult
    print("SCORE: ", score)
    cv2.circle(img, (int(point[0]),int(point[1])), 3, (0,0,255),2) 
    cv2.imwrite("dartBoard.png", img)
   # cv2.imshow("img",img)
   # cv2.waitKey(0)
    
    return sector, mult, img

def clockwise(v1,v2):
    """
    Determine if v2 is clockwise of v1
    """
    #calc normal vector of v1
    n1 = (-v1[1],v1[0])
    
    #Find size of the projection of v2 on the normal
    projection = v2[0]*n1[0] + v2[1]*n1[1]
   
    #print(projection)
    
    #negative projection = clockwise, positive = counterclockwise
    if projection < 0:
        return True
    else:
        return False

def get_mult(v,mults):
    """
    get multiplier by finding which radii the point falls between.
    """

    #miss
    if not within_radius(v,(mults[0]*mults[0])):
        print("MISS!")
        mult = 0
    #double
    elif within_radius(v,(mults[0]*mults[0])) and not within_radius(v,(mults[1]*mults[1])):
        mult = 2
    #triple
    elif within_radius(v,(mults[2]*mults[2])) and not within_radius(v,(mults[3]*mults[3])):
        mult = 3
    #25
    elif within_radius(v,(mults[4]*mults[4])) and not within_radius(v,(mults[5]*mults[5])):
        mult = 25
    #bull
    elif within_radius(v,(mults[5]*mults[5])) and not within_radius(v,(0)):
        mult = 50
    #bull - dead centre
    elif v == (0,0):
        mult = 50
    #default multiplier
    else:
        mult = 1

    return mult

def within_radius(v, radiusSquared):
    """
    See if point v is within radius(squared to avoid sqrt)
    """

    within = v[0]*v[0] + v[1]*v[1] <= radiusSquared

    return within

if __name__=='__main__':
   
    parser = argparse.ArgumentParser(description='Draw dart board and calculate score based on xy coordinate of a dart.')


    parser.add_argument(
    'x',
    type=float,
    help="x coordinate of dart.")

    parser.add_argument(
    'y',
    type=float,
    help="y coordinate of dart.")

    args = parser.parse_args()


    main(args.x, args.y)
