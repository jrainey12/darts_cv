import numpy as np
import cv2
import pickle as pkl
from Draw_board import main as get_score
#from  scoring.Draw_board import main as get_score
import logging 


def main():#c1_coords,c2_coords):
    """
    Triangulate the position of a dart and get the score.
    return: score - the score of the dart.
    """

    #Dart pixel location
#    dart = [c1_coords,c2_coords]
#dart = [[802,470], [475,493]]#left
    #dart =  [[722,350], [575,376]]#right
    #dart =  [[1202,384], [998,422]]#top
    #bot =  [[300,396], [98,405]]#bot

    dart = [[1015,389],[808,420]]#trip20
    #dart = [[801, 456],[352,348]]#14(eg1)
    print ("DART: ", dart)

    #Load camera calibration params and boundary points from pkl file.
    params = pkl.load(open("calib_params.pkl",'rb'))
 
    #format: [[cam1 X,cam1 Y],[cam2 X,cam2 Y]].
    left = params["left"]
    right = params["right"]
    top = params["top"]
    bot = params["bot"]

    print ("Left: ", left) 
    print ("right: ", right)
    print ("top: ", top)
    print ("bot: ", bot)
    #Check if dart is within outer bounds
#    if check_bounds(0,dart,left,right,top,bot) or check_bounds(1,dart,left,right,top,bot):
        
#        logging.info("Dart is outside of camera bounds.")
        
#        score = [0,0]

#        return score
     
    #Array of outer points and dart points
    #x1 = cam 1, x2 = cam 2
    x1 = np.array([left[0],right[0],top[0],bot[0],dart[0]],dtype=np.float32)
    x2 = np.array([left[1],right[1],top[1],bot[1],dart[1]],dtype=np.float32)

    #Undistort the outer points and dart points
    #x1_und = np.array([])
    #x2_und = np.array([])
    
    x1_und = cv2.undistortPoints(x1,params["mtx_1"],params["dist_1"],
            None,params["R1"],params["P1"])

    x2_und = cv2.undistortPoints(x2,params["mtx_2"],params["dist_2"],
            None,params["R2"],params["P2"])


    #triangulate the outer points and dart points 
#    points4d = cv2.triangulatePoints(params["P1"],params["P2"],x1_und,x2_und)
   
    points4d = cv2.triangulatePoints(params["P1"],params["P2"],x1_und,x2_und)
    print ("Points4d: ", points4d)
    
    #scale points to get euclidian points
    points_3d = (points4d[:3, :]/points4d[3, :]).T

    #points_3d = []
    #for i,j in enumerate(points4d[0]):
        #scaling factor
    #    sf = points4d[3][i]
        
    #    x = j/sf
    #    y = points4d[1][i]/sf
    #    z = points4d[2][i]/sf
    
    #    points_3d.append([x,y,z])

    print ("3D points: ",points_3d)

    #get x and z values from each 3D point
    x_vals = []
    z_vals = []
    for i in points_3d:
        x_vals.append(i[0])
        z_vals.append(i[2])

    print ("Unknown point: ", points_3d[-1])

    #Normalise the Z and X values in the range 0 to 100.
    print ("Z axis")
    z_norm = normalise(points_3d[-1][2],z_vals)
    print ("X axis")
    x_norm = normalise(points_3d[-1][0],x_vals)

    logging.debug("z Norm: "+ str(z_norm))
    logging.debug("x Norm: " + str(x_norm))

    #Convert the coords to work with Draw_board
    board_x = z_norm
    board_y = 100 - x_norm

    print ("BD:",board_x,board_y)
    #Get score and board model from Draw_board
    sector,mult, board = get_score(board_x,board_y)
#    logging.info("Dart Score: " + str(score))

    return [sector,mult]

    #show board
    cv2.imshow("board", board)
    cv2.waitKey(0)


def check_bounds(idx,dart,left,right,top,bot):
    """ Check if the dart point is within the outer bounds of the scoring 
    area of the dart board.
    param: idx - index of camera
    param: dart - dart coords
    param: left - left bound
    param: right - right bound
    param: top - top bound
    param: bot - bottom bound
    return: True if dart outside of boundaries
    """
    logging.debug("idx: " + str(idx))
    #camera 1
    if idx == 0:
        if ((dart[idx][1] > left[idx][1]) or (dart[idx][1] < right[idx][1]) or
            (dart[idx][0] < bot[idx][0]) or (dart[idx][0] > top[idx][0])):
 
            logging.debug("idx: " +  str(idx) + " " + str(dart[idx][0]) +
                    " " + str(left[idx][0])) 

            return True

        else:

            return False
    #camera 2
    else:
        if (dart[idx][1] > left[idx][1] or dart[idx][1] < right[idx][1] or
            dart[idx][0] < bot[idx][0] or dart[idx][0] > top[idx][0]):

            logging.debug("idx: " + str(idx) + " " + str(dart[idx][1]) +
                    " " + str(top[idx][1])) 
            return True    

        else:

            return False

def normalise(x_i,x):
    """ Normalise the x_i value in the range 0 to 100.
    param: x_i - value to be normalised.
    param: x - outer bounds values.
    return: norm - normalised value. """    


    x_min = np.min(x)
    x_max = np.max(x)
    logging.debug( "MIN: " + str(x_min))
    logging.debug("MAX: " + str(x_max))
    logging.debug("x_i: " + str( x_i))

    norm =  ((x_i - x_min)/(x_max - x_min))*100

    return norm


if __name__=='__main__':

    logging.basicConfig(format='%(message)s',level=logging.DEBUG)

    main()
