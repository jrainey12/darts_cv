import numpy as np
import cv2
import time
import pickle
import socket
import select
from find_coords_c2 import FindCoords

class CameraTwo():

    def __init__(self):
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1280)
        self.cap.set(3,720)
        
        self.TCP_IP = '192.168.0.2'
        self.TCP_PORT = 5090
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None    

        self.frames=[None,None,None]

        self.coords = None

        self.findCoords = FindCoords()

    def connectSocket(self):
        """
        Connect to the socket to send data.
        """
        self.sock.bind((self.TCP_IP,self.TCP_PORT))
        sock.listen()
        self.conn, addr = sock.accept()


    def captureFrame(self,idx):
        """
        Capture a single frame and add it to the frames list.
        param: idx - index of dart.
        """
        _,cam = self.cap.read()
        self.frames[idx] = cv2.flip(cam,0)
        

    def determineCoords(self):
        """
        Determine coordinates of darts in the frames using FindCoords.
        """
        self.coords = self.findCoords.findCoordsMulti(self.frames)


    def sendCoords(self):
        """
        Send the coordinates of the darts to raspi 1.
        """
        dart = 1

        while True:
            
            l=b''

            timeout = 0.01
            ready_sockets,_,_=select.select[self.conn],[],[], timeout)
        
            if ready_sockets:
                l = self.conn.recv(5)

            if l == b'Hello':
                
                captureFrame(dart)
                dart += 1
                    
                if dart == 4:
                    
                    self.determineCoords()

                    c = pickle.dumps(self.coords)
                    print len(c)
                    
                    c_len = bytes(str(len(c)),"utf-8")
                    
                    conn.send(c_len)
                    conn.sendall(c)
                    
                    #reset dart and coords
                    dart = 1
                    self.coords = None


            elif l == b'Stop!':
                break

        self.close()


    def close(self): 
        # When everything done, release the capture
        self.cap.release()
        self.sock.close()

if __name__=='__main__':

    main()

