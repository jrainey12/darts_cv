import numpy as np
import cv2
import time
import pickle
import socket
import select

def main():

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(cv2.CAP_PROP_FPS, 10)
    print ("FPS 1: ", cap.get(cv2.CAP_PROP_FPS))
    print("ex:", cap.get(cv2.CAP_PROP_EXPOSURE))
    
    TCP_IP = '192.168.0.2'
    TCP_PORT = 5090
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect((TCP_IP,TCP_PORT))
    sock.bind((TCP_IP,TCP_PORT))
    sock.listen()

    ret,cam = cap.read()
    frame = cv2.flip(frame,0)

        
    conn, addr = sock.accept()
    
    print("Sending Frames...")
    while(True):
        # Capture frame-by-frame
        ret,cam = cap.read()
        frame = cv2.flip(frame,0)
 
        s = frame.tobytes()
        #print(len(bytes(s)))
        #sock.send(bytes(len(s)))
        l=b''
        
        timeout = 0.01  # in seconds
        ready_sockets, _, _ = select.select(
        [conn], [], [], timeout)
        
        if ready_sockets: 
            l = conn.recv(5)

        if l == b'Hello':
            print ("Hello")
            #time.sleep(1)
            print("Sending Length")
            s_len = bytes(str(len(s)),"utf-8")
            #print(s_len)
            conn.send(s_len)
            conn.sendall(s)

        elif l == b'Stop!':
            break
        else:
            print ("Empty")
        
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    sock.close()

if __name__=='__main__':

    main()

