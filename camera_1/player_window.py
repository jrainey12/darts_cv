from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_window import MainWindow
from player import Player

class PlayerWindow(QMainWindow):
    """
    window for assigning player names
    """
   
    def __init__(self, player_count, game_type):
        super().__init__()
     
        #Initialise UI gametype and add players up to player_count
        self.height = 200 + (player_count * 125)
        self.setGeometry(100, 100, 600,self.height)
        self.setWindowTitle("Player Names!")
        self.w = None   
        self.game_type = game_type
       
        self.players = []

        for x in range(player_count):

            self.players.append(Player(str(x),game_type.getMaxScore()))

        game_type.changePlayer(self.players[0])

        #TODO: Come up with a more dynamic way to update ui for differing numbers of 
        #players.

        #player one name
        self.p1 = QLineEdit(self)
        self.p1.setText("Player 1")
        self.updatePlayers(self.p1.text(),0)
        self.p1.setFixedSize(200,100)
        self.p1.move(200, 25)
        self.p1.setAlignment(QtCore.Qt.AlignHCenter)
        self.p1.setFont(QFont('Times', 20))
        self.p1.editingFinished.connect(lambda: self.updatePlayers(self.p1.text(),0))

        if player_count > 1:
            #player two name
            self.p2 = QLineEdit(self)
            self.p2.setText("Player 2")
            self.updatePlayers(self.p2.text(),1)
            self.p2.setFixedSize(200,100)
            self.p2.move(200, 150)
            self.p2.setAlignment(QtCore.Qt.AlignHCenter)
            self.p2.setFont(QFont('Times', 20))
            self.p2.editingFinished.connect(lambda: self.updatePlayers(self.p2.text(),1))
        
        if player_count > 2:
            #player 3 name
            self.p3 = QLineEdit(self)
            self.p3.setText("Player 3")
            self.updatePlayers(self.p3.text(),2)
            self.p3.setFixedSize(200,100)
            self.p3.move(200, 275)
            self.p3.setAlignment(QtCore.Qt.AlignHCenter)
            self.p3.setFont(QFont('Times', 20))
            self.p3.editingFinished.connect(lambda: self.updatePlayers(self.p3.text(),2))


        if player_count > 3:
            #player 4 name
            self.p4 = QLineEdit(self)
            self.p4.setText("Player 4")
            self.updatePlayers(self.p4.text(),3)
            self.p4.setFixedSize(200,100)
            self.p4.move(200, 400)
            self.p4.setAlignment(QtCore.Qt.AlignHCenter)
            self.p4.setFont(QFont('Times', 20))
            self.p4.editingFinished.connect(lambda: self.updatePlayers(self.p4.text(),3))


        if player_count > 4:
            #player 5 name
            self.p5 = QLineEdit(self)
            self.p5.setText("Player 5")
            self.updatePlayers(self.p5.text(),4)
            self.p5.setFixedSize(200,100)
            self.p5.move(200, 525)
            self.p5.setAlignment(QtCore.Qt.AlignHCenter)
            self.p5.setFont(QFont('Times', 20))
            self.p5.editingFinished.connect(lambda: self.updatePlayers(self.p5.text(),4))


        #Show main window and start game.
        self.button = QPushButton(self)
        self.button.setText("Start Game")
        self.button.clicked.connect(self.show_new_window)
        self.button.setFixedSize(200,100)
        self.button.move(200, self.height - 125)
        self.button.setFont(QFont('Times', 20))

        print(self.getPlayerNames())
   
    def getPlayerNames(self):
        """
        Return a list of the names of all players.
        return: names - list of names.
        """
        names = []
        for p in self.players:
            names.append([p.getName(),p.getScore()])

        return names
            
    def updatePlayers(self,player_name,idx):
        """
        Update the name of the player.
        param: player_name - name of player
        param: idx - index of player
        """
        self.players[idx].setName(player_name)

        print (self.getPlayerNames())
    
    def show_new_window(self, checked):
        """
        Show main game window.
        """
        if self.w is None:
            self.w = MainWindow(self.players,self.game_type)
        self.w.show()
        self.close()
