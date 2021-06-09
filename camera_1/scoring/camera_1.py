import socket
import io
import cv2
import numpy as np
from paramiko.client import SSHClient
import time 
from find_coords_c1 import FindCoords
import pickle

class CameraOne:
    """
    Start Camera one streaming and detection for dart scoring. 
    """
    def __init__(self):
        
        self.TCP_IP = "192.168.0.2"
        self.TCP_PORT = 5090
        self.stream = False
        self.camTwoSock = None

        self.c1_frames = [None,None,None,None]

        self.c1_coords = []
        self.c2_coords = []

#        self.startCamTwoStream()
        #time.sleep(2)
        self.connectCamTwo()

        self.findCoords = FindCoords()

    def connectCamTwo(self):
        """
        connect to the socket on camera 2.
        """
        self.camTwoSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = False
        while not conn:
            try:
                self.camTwoSock.connect((self.TCP_IP,self.TCP_PORT)) 
                conn = True
            except:
                conn = False
                time.sleep(1)
                print ("Retrying...")
            
    def startCamTwoStream(self):
        """
        Start ssh connection with camera 2 and start camera capture.
        """
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(self.TCP_IP, username='pi', password='dartsraspi')
        stdin,stdout,stderr = client.exec_command('python3 /home/pi/camera_2/start_camera_2.py')

    def captureCamTwoFrame(self,idx):
        """
        Save a captured frame from camera 2.
        param: idx - index of frame.
        """
        print("hello ", idx)
        self.camTwoSock.sendall(b'Hello')
        time.sleep(1)             
        
        if idx == 3:
            self.determineCoords()
            length = None
            print("Waiting on length...")
            #length = self.camTwoSock.recv(7)
            #print(length)
            cam_2_data = self.camTwoSock.recv(500)
            #cam_2_data = self.recvall(self.camTwoSock,int((199)))
            self.c2_coords = pickle.loads(cam_2_data)
            print ("c2 coords:", self.c2_coords)

    def closeCamTwo(self):
        """
        Send a message two camera two to stop streaming.
        """
        self.camTwoSock.sendall(b'Stop!')
        #self.camTwoSock.close()

    def startCamStreams(self):
        """
        Start both cameras streaming and start the detection loop.
        When a dart is detected capture frames and end when 3 darts have 
        been captured.
        """
        #TODO: Update this to allow single darts to be captured.

        self.stream = True
        #self.startCamTwoStream()
        #time.sleep(3)
        #self.connectCamTwo()

        #start camera 1
        cap = cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)
        #ret,frame = cap.read()
                    
        #discard first 10 frames
        #for x in range(10):
        #    ret,frame = cap.read()

        # save background frames
        ret, cam = cap.read()
        frame = cv2.flip(cam,0)
        self.c1_frames[0] = frame
       # self.captureCamTwoFrame(0)
 
        #min and max threshold counts.
        t_min = 900#500
        t_max = 100000
        dart = 1
        
        #set comp_frame as background frame.
        comp_frame = cam.copy()

        print ("Waiting for dart...")

        while self.stream:
        
            #get difference between current frame and background
            ret,cam = cap.read()
            gray = cv2.cvtColor(cam.copy(), cv2.COLOR_BGR2GRAY)
            gray_diff = cv2.absdiff(gray, cv2.cvtColor(comp_frame,cv2.COLOR_BGR2GRAY))

            retval, thresh = cv2.threshold(gray_diff, 50, 255, cv2.THRESH_BINARY)#80
           
            #count non zero pixels after thresh  
            non_zero = cv2.countNonZero(thresh)
            print (non_zero)    
            #If within ranges save frames
            if non_zero > t_min and non_zero < t_max:
 
                time.sleep(0.5)          
                cv2.imwrite("seg_out/detection_frame_"+str(dart)+".jpg", thresh)
                print("Dart Found")
                c1_fr = cv2.flip(cam.copy(),0)
                self.c1_frames[dart] = c1_fr#cam.copy()
                self.captureCamTwoFrame(dart)
                print ("Updating comp frame")
                comp_frame = cam.copy()
                dart += 1
                #time.sleep(1) 
                print ("Waiting for dart ...")
                if dart == 4:
                    print("Ending...")
                    #self.determineCoords()
                    self.stream = False
                    
    def determineCoords(self):
        """
        Determine the coordinates of the darts in the camera 1 frames using FindCoords.
        """
        for i,x in enumerate(self.c1_frames):
            print(i,type(x))
            cv2.imwrite("seg_out/test_examples/frame_"+str(i)+".jpg",x)
        
        
        self.c1_coords = self.findCoords.findCoordsMulti(self.c1_frames)

    def captureCalibFrame(self):
        """
        Capture a frame from each camera to be used for calibration.
        return: f1,f2 - frames from cameras 1 and 2.
        """

        #TODO: Rename and adapt this for all single frame capture.

        #start camera 1
        cap = cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)
        #ret,frame = cap.read()
            
        #discard first 10 frames
        #for x in range(10):
        #    ret,frame = cap.read()
            
        # save background frames
        ret, cam = cap.read()
        f1 = cv2.flip(cam,0)
        f2 =  self.getCamTwoFrame()
        
        cap.release()

        return f1,f2


    def recvall(self,sock, count):
        """
        Receive values from a socket.
        param: sock - socket to receive from.
        param: count - length of data to receive.
        """
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def reset(self):
        """
        Reset the frames at the end of a turn.
        """
        self.stream = False
        #self.camTwoSock = None
        self.c1_frames = [None,None,None,None]
        #self.c1_frames = [None,None,None,None]

    def shutdownSocket(self):
        """
        Shutdown the open socket after transfer is complete.
        """

        self.camTwoSock.shutdown()
        self.camTwoSock.close()

    def getCoords(self):
        """
        Return the coords captured from camera 1 and camera 2.
        """
        return (self.c1_coords,self.c2_coords)

    def getSock(self):
        """
        Get the socket for camera 2.
        """
        return self.camTwoSock


