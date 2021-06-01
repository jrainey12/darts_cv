from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from calibration.calibrate_cameras import main as calibrate
from scoring.find_coords_single import main as find_coords_single
import time
from scoring.camera_streams import CameraStreams

class CalibWindow(QMainWindow):
    """
    Window showing calbration points and allowing new calibration points to 
    be determined.
    """
    def __init__(self):
        super().__init__()

        #initialise calibration points
        self.calib_max = 4
        self.calib_point = 1
        self.calib_coords = []
        self.default_img = "calibration/calib_point_images/default_board.jpg"

        self.c1_frames = [None,None,None,None,None]
        self.c2_frames = [None,None,None,None,None]

        #set up window
        self.setGeometry(100,100,1400,800)
        self.setWindowTitle("Dart Calibration")
       
        #exit button
        self.exit_button = QPushButton(self)
        self.exit_button.clicked.connect(self.close_window)
        self.exit_button.setText("CLOSE")
        self.exit_button.setFixedSize(300,100)
        self.exit_button.move(550,670)
        self.exit_button.setFont(QFont('Times', 35))
        self.exit_button.hide()

        #calibrate button
        self.calibrate_button = QPushButton(self)
        self.calibrate_button.clicked.connect(lambda: self.get_calib_point(self.calib_point))
        self.calibrate_button.setText("Calibrate")
        self.calibrate_button.setFixedSize(300,100)
        self.calibrate_button.move(550,670)
        self.calibrate_button.setFont(QFont('Times', 35))

        #Instruction window
        self.base_inst = "To calibrate, place a dart at the blue mark shown on the right, then click the calibrate button.\n "
        self.first_inst = "Repeat this for the remaining " +  str(self.calib_max-1) + " points."
        self.inst_window = QLabel(self)
        self.inst_window.setText(self.base_inst +  self.first_inst)
        self.inst_window.setAlignment(QtCore.Qt.AlignCenter)
        self.inst_window.setFixedSize(655,610)
        self.inst_window.move(30,30)
        self.inst_window.setFont(QFont('Times', 20))
        self.inst_window.setStyleSheet("border: 1px solid black;background-color: white")
        self.inst_window.setWordWrap(True)

        #Instruction image
        self.im_view = QLabel(self)
        self.im_view.setFixedSize(655,610)
        self.im_view.move(715,30)
        self.im_view.setStyleSheet("border: 1px solid black;") 
        pixmap = QtGui.QPixmap("calibration/calib_point_images/point_1_board.jpg")
        self.im_view.setPixmap(pixmap.scaled(self.im_view.size()))


        #Initialise CameraStreams, start and connect to camera 2.
        self.cameraStreams = CameraStreams()
        self.cameraStreams.startCamTwoStream()
        self.connectCamTwo()
        
        #get background images
        self.getCalibPoint(0)



    def update_image(self,image_no):
       
        if image_no == 4:
            image = self.default_img
        else:
            image = "calibration/calib_point_images/point_" + str(image_no+1) +"_board.jpg" 
        pixmap = QtGui.QPixmap(image)
        self.im_view.setPixmap(pixmap.scaled(self.im_view.size()))

    def get_calib_point(self,calib_point):
    
        if calib_point > self.calib_max:
           
            #shutdown cam 2 socket
            cameraStreams.shutdownSocket()

            #Use find_coords single to determine the coords of each of the four points
            left = find_coords_single(c1_frames[0:1],c2_frames[0:1])
            right = find_coords_single(c1_frames[1:2],c2_frames[1:2])
            top = find_coords_single(c1_frames[2:3],c2_frames[2:3])
            bot = find_coords_single(c1_frames[3:4],c2_frames[3:4])

            #Run stereo calibration
            calibrate_cameras(left,right,top,bot)

            self.first_inst = "Calibration Complete. Parameters saved in 'calib_params.pkl'"
            sec_inst = "\nClose and restart calibration process to recalibrate."

            self.inst_window.setText(self.first_inst + sec_inst)

            self.calibrate_button.hide()
            self.exit_button.show()
            print ("All calibration points captured. Restart GUI to recalibrate.")
       
        elif calib_point == 0:
            
            #get a background frame from each camera
            f1, f2 = self.cameraStreams.captureCalibFrame()
            c1_frames[calib_point] = f1
            c2_frames[calib_point] = f2

        else:
            print ("CALIB DART AT POINT : ", calib_point)
            
            #get a single frame from each camera
            f1, f2 = self.cameraStreams.captureCalibFrame()
            c1_frames[calib_point] = f1
            c2_frames[calib_point] = f2
                  
            self.calib_point = self.calib_point + 1 
            
            iters_left = str(self.calib_max - self.calib_point + 1)
            self.update_image(calib_point)
            if calib_point < 4:
                self.first_inst = "Repeat this " + iters_left + " more time(s)."
                self.inst_window.setText(self.base_inst +  self.first_inst)
            else:
                self.first_inst = "Calibration Complete."
                self.inst_window.setText(self.first_inst)

        print (self.calib_coords)

    def close_window(self):
        if self.calib_point == 5:
            self.close()

if __name__=='__main__':

    app = QApplication(sys.argv)
    GUI = CalibWindow()
    GUI.show()
    sys.exit(app.exec_())

