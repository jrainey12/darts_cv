from player import Player
from x01 import x01

def player_tests():

    p1 = Player("Player 1",501)

    name = p1.getName()
    print ("Name: ", name)

    score = p1.getScore()
    print("Score: ", score)

    p1.setName("James")
    print("Name: ", p1.getName())
 
def x01_tests():

    players = [Player("James", 101),Player("Bill",101)]

    game = x01()
    game.changePlayer(players[0])

    game.updateDartOne(20,1)
    game.updateDartTwo(5,2)
    game.updateDartThree(1,3)

    d1,d1_mult = game.getDartOne()
    print ("Dart 1: ", d1 , " x ", d1_mult)

    d2,d2_mult = game.getDartTwo()
    print ("Dart 2: ", d2 , " x ", d2_mult)

    d3,d3_mult = game.getDartThree()
    print ("Dart 3: ", d3 , " x ", d3_mult)

    game.calculateScore()

    game.updatePlayerScore()

    game.checkPlayerScore()

    score = players[0].getScore()

    print ("Score: ", score)

    game.changePlayer(players[1])

    game.updateDartOne(20,3)
    game.updateDartTwo(20,2)
    game.updateDartThree(1,1)

    d1,d1_mult = game.getDartOne()
    print ("Dart 1: ", d1 , " x ", d1_mult)

    d2,d2_mult = game.getDartTwo()
    print ("Dart 2: ", d2 , " x ", d2_mult)

    d3,d3_mult = game.getDartThree()
    print ("Dart 3: ", d3 , " x ", d3_mult)

    game.calculateScore()

    game.updatePlayerScore()

    win = game.checkPlayerScore()
    if win:
        print ("GAME OVER!")
        print (game.getActivePlayer().getName() + " is the winner!")

    score = players[1].getScore()

    print ("Score: ", score)

    p1_score = players[0].getScore()
    
    print ("P1 Score: ", p1_score)

if __name__=='__main__':

   player_tests()
   x01_tests()
