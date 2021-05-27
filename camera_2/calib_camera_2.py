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
    sock.bind((TCP_IP,TCP_PORT))
    sock.listen()

   
    conn, addr = sock.accept()


    ret,cam = cap.read()
    frame = cv2.flip(cam,0)
    
    s = frame.tobytes()
    l=b''
        
    timeout = 0.01  # in seconds
    ready_sockets, _, _ = select.select(
        [conn], [], [], timeout)
        
    if ready_sockets: 
        l = conn.recv(5)

    if l == b'Hello':
        s_len = bytes(str(len(s)),"utf-8")
        conn.send(s_len)
        conn.sendall(s)




    # When everything done, release the capture
    cap.release()
    sock.close()

if __name__=='__main__':

    main()

