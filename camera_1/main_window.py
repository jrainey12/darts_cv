from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from functools import partial
#from scoring.camera_1 import main as get_scores
import time
from scoring.camera_1 import CameraOne
from scoring.find_coords import FindCoords
from scoring.triangulate import main as triangulate

class MainWindow(QMainWindow):
    """
    Main game window showing scores.
    """
    def __init__(self,players, game):
        super().__init__()
        
        #self.image = "dartBoard_example.jpg"
        self.game = game
        self.players = players
        #Dart scores, d1,d1_mult,d2,d2_mult,d3,d3_mult
        #self.dart_scores = [[None,None],[None,None],[None,None]]
        self.D1 = [None,None]
        self.D2 = [None,None]
        self.D3 = [None,None]

        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle("Play Darts!")
        
        #Player Name
        self.player_label = QLabel(self)
        self.player_label.setText(self.game.getActivePlayer().getName())
        self.player_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.player_label.setFixedSize(200,60)
        self.player_label.move(400,25)
        self.player_label.setFont(QFont('Times', 30))

        #button to start turn
        self.start_button = QPushButton(self)
        self.start_button.clicked.connect(lambda: self.get_dart_scores())
        self.start_button.setText("Start Turn")
        self.start_button.setFixedSize(250,100)
        self.start_button.move(600,390)
        self.start_button.setFont(QFont('Times', 20))

        #End Turn Button
        self.end_button = QPushButton(self)
        self.end_button.clicked.connect(lambda: self.end_turn(self.game))
        self.end_button.setText("End Turn")
        self.end_button.setFixedSize(250,100)
        self.end_button.move(600,500)
        self.end_button.setFont(QFont('Times', 20))
        self.end_button.hide()
        
        #image of recent dart scores.
        #self.im_preview = QLabel(self)
        #self.im_preview.setText("Image Preview")
        #self.im_preview.setAlignment(QtCore.Qt.AlignCenter)
        #self.im_preview.setGeometry(300,50,400,350)
        #self.im_preview.setStyleSheet("border: 1px solid black;") 
        #pixmap = QtGui.QPixmap(self.image)
        #self.im_preview.setPixmap(pixmap.scaled(self.im_preview.size()))


        #Score Label
        self.score_label = QLabel(self)
        self.score_label.setText("Score")
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setFixedSize(100,100)
        self.score_label.move(600, 150)
        self.score_label.setFont(QFont('Times', 20))
       
       #Score value
        self.score = QLabel(self)
        self.score.setText(str(game.getActivePlayer().getScore()))
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.setFixedSize(150,100)
        self.score.move(700,150)
        self.score.setStyleSheet("border: 1px solid black;background-color: white") 
        self.score.setFont(QFont('Times', 20))

        #Dart 1 Score label
        self.D1_score_label = QLabel(self)
        self.D1_score_label.setText("Dart 1")
        self.D1_score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.D1_score_label.setFixedSize(75,100)
        self.D1_score_label.move(25, 150)
        self.D1_score_label.setFont(QFont('Times', 20))

        #Dart 1 Sector
        self.D1_sect = QLineEdit(self)
        self.D1_sect.setText("0")
        self.D1_sect.setAlignment(QtCore.Qt.AlignCenter)
        self.D1_sect.setFixedSize(100,100)
        self.D1_sect.move(125,150)
        self.D1_sect.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D1_sect.setFont(QFont('Times', 20))
        self.D1_sect.editingFinished.connect(lambda: self.update_scores(self.D1_sect.text(),0,0))
       
        #Dart 1 multiplier
        self.D1_mult = QLineEdit(self)
        self.D1_mult.setText("0")
        self.D1_mult.setAlignment(QtCore.Qt.AlignCenter)
        self.D1_mult.setFixedSize(100,100)
        self.D1_mult.move(250,150)
        self.D1_mult.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D1_mult.setFont(QFont('Times', 20))
        self.D1_mult.editingFinished.connect(lambda: self.update_scores(self.D1_mult.text(),0,1))
       
        #Dart 1 total Score
        self.D1_score = QLabel(self)
        self.D1_score.setText("0")
        self.D1_score.setAlignment(QtCore.Qt.AlignCenter)
        self.D1_score.setFixedSize(100,100)
        self.D1_score.move(375,150)
        self.D1_score.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D1_score.setFont(QFont('Times', 20))
       
        #Dart 2 Score label
        self.D2_score_label = QLabel(self)
        self.D2_score_label.setText("Dart 2")
        self.D2_score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.D2_score_label.setFixedSize(75,100)
        self.D2_score_label.move(25, 325)
        self.D2_score_label.setFont(QFont('Times', 20)) 
       
        #Dart 2 Sector
        self.D2_sect = QLineEdit(self)
        self.D2_sect.setText("0")
        self.D2_sect.setAlignment(QtCore.Qt.AlignCenter)
        self.D2_sect.setFixedSize(100,100)
        self.D2_sect.move(125,325)
        self.D2_sect.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D2_sect.setFont(QFont('Times', 20))
        self.D2_sect.editingFinished.connect(lambda: self.update_scores(self.D2_sect.text(),1,0))
       
        #Dart 2 multiplier
        self.D2_mult = QLineEdit(self)
        self.D2_mult.setText("0")
        self.D2_mult.setAlignment(QtCore.Qt.AlignCenter)
        self.D2_mult.setFixedSize(100,100)
        self.D2_mult.move(250,325)
        self.D2_mult.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D2_mult.setFont(QFont('Times', 20))
        self.D2_mult.editingFinished.connect(lambda: self.update_scores(self.D2_mult.text(),1,1))
       
        #Dart 2 total Score
        self.D2_score = QLabel(self)
        self.D2_score.setText("0")
        self.D2_score.setAlignment(QtCore.Qt.AlignCenter)
        self.D2_score.setFixedSize(100,100)
        self.D2_score.move(375,325)
        self.D2_score.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D2_score.setFont(QFont('Times', 20))
       
        #Dart 3 Score label
        self.D3_score_label = QLabel(self)
        self.D3_score_label.setText("Dart 3")
        self.D3_score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.D3_score_label.setFixedSize(75,100)
        self.D3_score_label.move(25, 500)
        self.D3_score_label.setFont(QFont('Times', 20)) 
       
        #Dart 3 Sector
        self.D3_sect = QLineEdit(self)
        self.D3_sect.setText("0")
        self.D3_sect.setAlignment(QtCore.Qt.AlignCenter)
        self.D3_sect.setFixedSize(100,100)
        self.D3_sect.move(125,500)
        self.D3_sect.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D3_sect.setFont(QFont('Times', 20))
        self.D3_sect.editingFinished.connect(lambda: self.update_scores(self.D3_sect.text(),2,0))
        
        #Dart 3 multiplier
        self.D3_mult = QLineEdit(self)
        self.D3_mult.setText("0")
        self.D3_mult.setAlignment(QtCore.Qt.AlignCenter)
        self.D3_mult.setFixedSize(100,100)
        self.D3_mult.move(250,500)
        self.D3_mult.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D3_mult.setFont(QFont('Times', 20))
        self.D3_mult.editingFinished.connect(lambda: self.update_scores(self.D3_mult.text(),2,1))
       
        #Dart 3 total Score
        self.D3_score = QLabel(self)
        self.D3_score.setText("0")
        self.D3_score.setAlignment(QtCore.Qt.AlignCenter)
        self.D3_score.setFixedSize(100,100)
        self.D3_score.move(375,500)
        self.D3_score.setStyleSheet("border: 1px solid black;background-color: white") 
        self.D3_score.setFont(QFont('Times', 20))
       
        
        self.show()

        # intialise camera streams class
        self.CameraOne = CameraOne()
        #self.update_scores(self.player)

    
    def update_scores(self,score,dart,item):
        """
        update the stored dart scores.
        param: score - score to add.
        param: dart - dart related to score
        param: item - int indicating sector or mult
        """
        #self.dart_scores[dart][item] = int(score)
       
        if dart == 0:

            self.D1[item] = int(score)

        elif dart == 1:

            self.D2[item] = int(score)

        else:

            self.D3[item] = int(score)


        self.update_total_score(dart)
        
    def update_total_score(self,dart):
        """
        Update the dart scores text.
        param: dart - dart to update.
        """
        if dart == 0:

            #self.D1_score.setText(str(self.dart_scores[0][0] * self.dart_scores[0][1]))
            self.D1_score.setText(str(self.D1[0]*self.D1[1]))
        
        elif dart == 1:

            #self.D2_score.setText(str(self.dart_scores[1][0] * self.dart_scores[1][1]))
            self.D2_score.setText(str(self.D2[0]*self.D2[1]))
        else:
            
            #self.D3_score.setText(str(self.dart_scores[2][0] * self.dart_scores[2][1]))
            self.D3_score.setText(str(self.D3[0]*self.D3[1]))

    def end_turn(self,game):
        """
        End the players turn, calculate and update the score, check for win conditions
        and check for bust. Then change to the next player and update the UI.
        param: game - game instance to be updated.
        """
        game.updateDartOne(self.D1[0],self.D1[1])
        game.updateDartTwo(self.D2[0],self.D2[1])
        game.updateDartThree(self.D3[0],self.D3[1])
       
        #game.updateDartOne(self.dart_scores[0][0],self.dart_scores[0][1])
        #game.updateDartTwo(self.dart_scores[1][0],self.dart_scores[1][1])
        #game.updateDartThree(self.dart_scores[2][0],self.dart_scores[2][1])
       
        game.calculateScore()

        notBust = game.updatePlayerScore()
    
        player_score = game.getActivePlayer().getScore()

        print (player_score)

        if not notBust:
            print ("Bust!")

        win = game.checkPlayerScore()

        if win:

            self.gameOver(game.getActivePlayer())
            
        idx = self.players.index(game.getActivePlayer())

        if idx == (len(self.players)-1):
            game.changePlayer(self.players[0])

        else:
            game.changePlayer(self.players[idx+1])


        #self.dart_scores = [[None,None],[None,None],[None,None]]

        #self.score.setText(str(game.getActivePlayer().getScore()))
        
        self.resetScores()

        self.player_label.setText(game.getActivePlayer().getName())
      
        self.score.setText(str(game.getActivePlayer().getScore()))
        #game.updateDartOne(0,0)
        #game.updateDartTwo(0,0)
        #game.updateDartThree(0,0)
                    

    #    pixmap = QtGui.QPixmap(image)
    #    self.im_preview.setPixmap(pixmap.scaled(self.im_preview.size()))

        self.cameraOne = CameraOne()
        self.start_button.show()
        self.end_button.hide()

    def resetScores(self):
        """
        Reset the scores on the UI to zeros.
        """
        self.D1_sect.setText("0")
        self.D1_mult.setText("0")
        self.D1_score.setText("0")

        self.D2_sect.setText("0")
        self.D2_mult.setText("0")
        self.D2_score.setText("0")
 
        self.D3_sect.setText("0")
        self.D3_mult.setText("0")
        self.D3_score.setText("0")


    #def selectionchange(self,i):

     #   self.input_type = self.cb.currentText()

      #  print ("Current index",i,"selection changed ",self.cb.currentText())


    def get_dart_scores(self):
        """
        Start recording and detection on the cameras streams.
        Get the saved frames and determine dart scores.
        Update the score variables and UI.
        """
        self.start_button.hide()
        self.CameraOne.startCamStreams()

        c1_coords,c2_coords = self.CameraOne.getCoords()

        D1_C1 = c1_coords[0]
        D1_C2 = c2_coords[0]
        
        D2_C1 = c1_coords[1]
        D2_C2 = c2_coords[1]

        D3_C1 = c1_coords[2]
        D3_C2 = c2_coords[2]
 
        D1 = triangulate(D1_C1,D1_C2) 
        D2 = triangulate(D2_C1,D2_C2) 
        D3 = triangulate(D3_C1,D3_C2) 

       
        
        self.D1 = D1#[20,1]
        self.D2 = D2#[5,3]
        self.D3 = D3#[1,1]
        #update dart score boxes    
        self.D1_sect.setText(str(self.D1[0]))
        self.D1_mult.setText(str(self.D1[1]))
        self.D1_score.setText(str(self.D1[0] * self.D1[1]))

        self.D2_sect.setText(str(self.D2[0]))
        self.D2_mult.setText(str(self.D2[1]))
        self.D2_score.setText(str(self.D2[0] * self.D2[1]))

        self.D3_sect.setText(str(self.D3[0]))
        self.D3_mult.setText(str(self.D3[1]))
        self.D3_score.setText(str(self.D3[0] * self.D3[1]))




#        self.D1_sect.setText(str(self.dart_scores[0][0]))
#        self.D1_mult.setText(str(self.dart_scores[0][1]))
#        self.D1_score.setText(str(self.dart_scores[0][0] * self.dart_scores[0][1]))

#        self.D2_sect.setText(str(self.dart_scores[1][0]))
#        self.D2_mult.setText(str(self.dart_scores[1][1]))
#        self.D2_score.setText(str(self.dart_scores[1][0] * self.dart_scores[1][1]))

#        self.D3_sect.setText(str(self.dart_scores[2][0]))
#        self.D3_mult.setText(str(self.dart_scores[2][1]))
#        self.D3_score.setText(str(self.dart_scores[2][0] * self.dart_scores[2][1]))



        #update Image
     #   self.image = "dartBoard.png"
     #   self.image_open(self.image)
        #calculate score
        
        self.end_button.show()

    def gameOver(self,player):
        """
        show the end window if a win condition is met.
        param: player - winning player.
        """
        self.w = EndWindow(self,player)
        self.w.show()



class EndWindow(QMainWindow):
    """
    Free floating window showing the winner.
    """
    def __init__(self,w,player):
        super().__init__()
        
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Game Over!")
        
        self.win_lab = QLabel(self)
        self.win_lab.setText("The winner is:")
        self.win_lab.setFixedSize(200,100)
        self.win_lab.move(150, 50)
        self.win_lab.setFont(QFont('Times', 20))
        self.win_lab.setAlignment(QtCore.Qt.AlignCenter)

        self.p = QLabel(self)
        self.p.setText(player.getName())
        self.p.setFixedSize(200,100)
        self.p.move(150, 150)
        self.p.setFont(QFont('Times', 30))
        self.p.setAlignment(QtCore.Qt.AlignCenter)

        self.button = QPushButton(self)
        self.button.setText("Close")
        self.button.clicked.connect(lambda: self.close_windows(w))
        self.button.setFixedSize(100,100)
        self.button.move(200,300)   
        self.button.setFont(QFont('Times', 20))


    def close_windows(self,w):
        """
        Close selected windows.
        param: w - window to close.
        """

        w.close()
        self.close()




#if __name__=='__main__':

    #Initialise GUI and show main window
#    app = QApplication(sys.argv)
#    GUI = StartWindow()
#    GUI.show()
#    sys.exit(app.exec_())
