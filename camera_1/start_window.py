from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from player_window import PlayerWindow
from games.x01 import x01
from calibration.calibrate_cameras import main as calibrate

class StartWindow(QMainWindow):
    """
    Start window for selecting the number of players and
    the dart game to be played. 
    Also allows access to the calbration screen.
    """
    def __init__(self):
        super().__init__()
        
        #Player count min of 1, max of 5
        self.player_count = 1
        #Game Type: 0 = 501, 1 = Cricket 
        self.game_type = None

        #Initialise window
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle("Player Select!")
        self.w = None
        
        #Dropdown to select number of players
        self.player_num = QComboBox(self)
        self.player_num.setFixedSize(225,100)
        self.player_num.move(450,50)
        self.player_num.setFont(QFont('Times',20))
        self.player_num.addItems(['1','2','3','4','5'])
        self.player_num.setEditable(True)
        self.player_num.lineEdit().setReadOnly(True)
        self.player_num.lineEdit().setAlignment(QtCore.Qt.AlignCenter) 
        self.player_num.currentIndexChanged.connect(self.updatePlayerCount)

        #Label for number of players
        self.num_lab = QLabel(self)
        self.num_lab.setText("Number of Players:")
        self.num_lab.setFixedSize(225,100)
        self.num_lab.move(125, 50)
        self.num_lab.setAlignment(QtCore.Qt.AlignVCenter)
        self.num_lab.setFont(QFont('Times', 20))

        #Game type label
        self.game_lab = QLabel(self)
        self.game_lab.setText("Game Type:")
        self.game_lab.setFixedSize(250,100)
        self.game_lab.move(125, 200)
        self.game_lab.setAlignment(QtCore.Qt.AlignVCenter)
        self.game_lab.setFont(QFont('Times', 20))

        #Dropdown for selecting game type
        self.game = QComboBox(self)
        self.game.setFixedSize(225,100)
        self.game.move(450,200)
        self.game.setFont(QFont('Times',20))
        self.game.addItems([" ","X01","Cricket"])
        self.game.setEditable(True)
        self.game.lineEdit().setReadOnly(True)
        self.game.lineEdit().setAlignment(QtCore.Qt.AlignCenter) 
        self.game.currentIndexChanged.connect(self.updateGameType)
         
        #Game score label
        self.score_lab = QLabel(self)
        self.score_lab.setText("Game Score:")
        self.score_lab.setFixedSize(250,100)
        self.score_lab.move(125, 350)
        self.score_lab.setAlignment(QtCore.Qt.AlignVCenter)
        self.score_lab.setFont(QFont('Times', 20))
        self.score_lab.hide()

        #Optional dropdown for selecting max score that shows when X01 is 
        #selected as the game type
        self.score = QComboBox(self)
        self.score.setFixedSize(225,100)
        self.score.move(450,350)
        self.score.setFont(QFont('Times',20))
        self.score.addItems(["101","201","301","401","501"])
        self.score.setEditable(True)
        self.score.lineEdit().setReadOnly(True)
        self.score.lineEdit().setAlignment(QtCore.Qt.AlignCenter) 
        self.score.currentIndexChanged.connect(self.updateGameScore)
        self.score.hide()

        #Open the calibration window
        self.button1 = QPushButton(self)
        self.button1.setText("Calibrate")
        self.button1.clicked.connect(self.show_calib_window)
        self.button1.setFixedSize(250,100)
        self.button1.move(125,600)
        self.button1.setFont(QFont('Times', 20))

        #Open the player window to name the players
        self.button2 = QPushButton(self)
        self.button2.setText("Start Game")
        self.button2.clicked.connect(self.show_new_window)
        self.button2.setFixedSize(250,100)
        self.button2.move(425,600)
        self.button2.setFont(QFont('Times', 20))


    def updateUI(self,gt):
        """
        Update the UI to show score dropdown in the X01 game type is selected.
        param: gt - int representing gametype 
        """
        if gt == 1:
           
            self.score_lab.show()
            self.score.show()

        elif gt == 2:

            self.score_lab.hide()
            self.score.hide()
           
    def updatePlayerCount(self, count):
        """
        Update the player count for the selected game.
        param: count - number of players to update to.
        """

        self.player_count = count + 1
        print ("Player count updated to " + str(self.player_count))

    def updateGameType(self, gt):
        """
        Update the game type.
        param: gt - int representing game type.
        """

        if gt == 1:
            self.game_type = x01()

        print ("Game type updated to " + str(gt)) 
        self.updateUI(gt)

    def updateGameScore(self, score):
        """
        Update the max score to be used in X01.
        param: score - the max score to set.
        """

        self.game_type.setMaxScore(int(self.score.currentText()))
        print (self.score.currentText())

    def show_calib_window(self, checked):
        """
        Show the calibration window.
        """
        print("Starting calibration!") 
        #CalibWindow().show()
        calibrate()

    def show_new_window(self, checked):
        """
        Open the player window if a game type has been selected.
        """

        print (self.game.currentText())
        if self.game.currentText() != " ":
            if self.w is None:
                self.w = PlayerWindow(self.player_count, self.game_type)
            self.w.show()
            self.close()
        else:
            print ("Select a game type.")

if __name__=='__main__':
    
    #Initialise the app and show the UI
    app = QApplication(sys.argv)
    GUI = StartWindow()
    GUI.show()
    sys.exit(app.exec_())
