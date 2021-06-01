from camera_2 import CameraTwo

def main():

    #initialise camera two
    cameraTwo = CameraTwo()
    
    #connect to socket 
    cameraTwo.connectSocket()

    #send Coordinates
    cameraTwo.sendCoords()


if __name__=='__main__':
    main()
