import socket
import io
import cv2
import numpy as np
from paramiko.client import SSHClient
import time 

class CameraStreams:
    """
    Start Camera streams and detection for dart scoring. 
    """
    def __init__(self):
        
        self.TCP_IP = "192.168.0.2"
        self.TCP_PORT = 5090
        self.stream = False
        self.camTwoSock = None

        self.c1_frames = [None,None,None,None]
        self.c2_frames = [None,None,None,None]

        self.startCamTwoStream()
        #time.sleep(2)
        self.connectCamTwo()

    def connectCamTwo(self):
        """
        connect to the socket on camera 2.
        """
        self.camTwoSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con = False
        while not con:
            try:
                self.camTwoSock.connect((self.TCP_IP,self.TCP_PORT)) 
                con=True
            except:
                con=False
                time.sleep(0.5)
                print ("Retrying...")
            
    def startCamTwoStream(self):
        """
        Start ssh connection with camera 2 and start camera capture.
        """
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(self.TCP_IP, username='pi', password='dartsraspi')
        stdin,stdout,stderr = client.exec_command('python3 /home/pi/camera_2/camera_2.py')

    def getCamTwoFrame(self):
        """
        Return a captured frame from camera 2.
        param: sock - socket to receive data from.
        return: cam_2 - frame from camera 2.
        """
        self.camTwoSock.sendall(b'Hello')
        length = None
        print("Waiting on length...")
        length = self.camTwoSock.recv(7)
        print(length)
        cam_2_data = self.recvall(self.camTwoSock,int((length)))
        cam_2_frame = np.frombuffer(cam_2_data,dtype=np.uint8)
        cam_2 = cam_2_frame.reshape(720,1280,3)

        return cam_2
    
    def closeCamTwo(self):

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
        self.c2_frames[0] = self.getCamTwoFrame()
 
        #min and max threshold counts.
        t_min = 100
        t_max = 10000
        dart = 1
        
        #set comp_frame as background frame.
        comp_frame = cam.copy()

        print ("Waiting for dart...")

        while self.stream:
        
            #get difference between current frame and background
            ret,cam = cap.read()
            gray = cv2.cvtColor(cam.copy(), cv2.COLOR_BGR2GRAY)
            gray_diff = cv2.absdiff(gray, cv2.cvtColor(comp_frame,cv2.COLOR_BGR2GRAY))
            retval, thresh = cv2.threshold(gray_diff, 80, 255, cv2.THRESH_BINARY)
           
            #count non zero pixels after thresh  
            non_zero = cv2.countNonZero(thresh)
            print (non_zero)    
            #If within ranges save frames
            if non_zero > t_min and non_zero < t_max:
                time.sleep(0.5)          
                print("Dart Found")
                c1_fr = cv2.flip(cam.copy(),0)
                self.c1_frames[dart] = c1_fr#cam.copy()
                self.c2_frames[dart] = self.getCamTwoFrame()
                print ("Updating comp frame") 
                comp_frame = cam.copy()
   
                dart += 1
                #time.sleep(1) 
                print ("Waiting for dart ...")
                if dart > 3:

                    self.stream = False
                    self.closeCamTwo() 

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
        self.camTwoSock = None
        self.c1_frames = [None,None,None,None]
        self.c1_frames = [None,None,None,None]

    def shutdownSocket(self):
        """
        Shutdown the open socket after transfer is complete.
        """

        self.camTwoSock.shutdown()
        self.camTwoSock.close()

    def getFrames(self):
        """
        Return the frames captured from camera 1 and camera 2.
        """
        return (self.c1_frames,self.c2_frames)

    def getSock(self):
        """
        Get the socket for camera 2.
        """
        return self.camTwoSock


