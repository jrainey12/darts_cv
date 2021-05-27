import socket
import io
import cv2
import numpy as np
from paramiko.client import SSHClient

class CameraStreams:
    """
    Start Camera streams and detection for dart scoring. 
    """
    def __init__(self):
        
        self.TCP_IP = "192.168.0.2"
        self.TCP_PORT = 5090
        self.stream = False
        self.camTwoSock = None

        c1_frames = [None,None,None,None]
        c2_frames = [None,None,None,None]

        #self.backFrame1 = None
        #self.backFrame2 = None
        #self.d1_frame1 = None
        #self.d1_frame2 = None
        #self.d2_frame1 = None
        #self.d2_frame2 = None
        #self.d3_frame1 = None
        #self.d3_frame2 = None



    def connectCamTwo(self):
        """
        connect to the socket on camera 2.
        """
        self.camTwoSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.camTwoSock.connect((self.TCP_IP,self.TCP_PORT))

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
        cam_2_data = recvall(self.camTwoSock,int((length)))
        cam_2_frame = np.frombuffer(cam_2_data,dtype=np.uint8)
        cam_2 = cam_2_frame.reshape(1280,720,3)

        return cam_2

    def startCamStreams(self):
        """
        Start both cameras streaming and start the detection loop.
        When a dart is detected capture frames and end when 3 darts have 
        been captured.
        """
        #TODO: Update this to allow single darts to be captured.

        self.stream = True
        self.startCamTwoStream()
        self.connectCamTwo()

        #start camera 1
        cap = cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)
        ret,frame = cap.read()
            
        #discard first 10 frames
        for x in range(10):
            ret,frame = cap.read()
            
        # save background frames
        ret, cam = cap.read()
        self.c1_frames[0] = cam
        self.c2_frames[0] = self.getCamTwoFrames()

                
        #min and max threshold counts.
        t_min = 5
        t_max = 10000
        dart = 1

        while self.stream:

            #set comp_frame as background frame.
            comp_frame = self.c1_frames[0].copy()
            #get difference between current frame and background
            ret,cam = cap.read()
            gray = cv2.cvtColor(cam.copy(), cv2.COLOR_BGR2GRAY)
            gray_diff = cv2.absdiff(gray, cv2,cvtColor(comp_frame,cv2.COLOR_BGR2GRAY))
            retval, thresh = cv2.threshold(gray_diff, 80, 255, cv2.THRESH_BINARY)
           
            #count non zero pixels after thresh  
            non_zero = cv2.countNonZero(thresh)
            
            #If within ranges save frames
            if non_zero > t_min and non_zero < t_max:
                          
                print("Dart Found")
                self.d1_frames[dart] = cam.copy()
                self.d2_frames[dart] = getCamTwoFrame(self.camTwoSock)
                comp_frame = self.d1_frames[dart].copy()
   
                dart += 1
                
                if dart > 3:

                    self.stream = False
                
    
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

    def getFrames(self):
        """
        Return the 8 frames captured.
        """
        return (self.c1_frames,self.c2_frames)
        #return ([self.backFrame1,self.d1_frame1,self.d2_frame1,self.d3_frame1,
        #    self.backFrame2,self.d1_frame2,self.d2_frame2,self.d3_frame2])

    def getSock(self):
        """
        Get the socket for camera 2.
        """
        return self.camTwoSock


