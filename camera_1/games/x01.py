from games.game_type import GameType

class x01(GameType):
    """
    Implementation of the X01 game of darts.
    param: GameType - generic GameType class.
    """
    def __init__(self):
        super().__init__()

        self.dart_1 = None
        self.dart_1_mult = None
        self.dart_2 = None
        self.dart_2_mult = None
        self.dart_3 = None
        self.dart_3_mult = None

        self.throw_total = 0

    
    def calculateScore(self):
        """
        Calculate the final score for each dart and update the throw total.
        """
        d1 = self.dart_1 * self.dart_1_mult
        d2 = self.dart_2 * self.dart_2_mult
        d3 = self.dart_3 * self.dart_3_mult

        self.throw_total = d1 + d2 + d3

    def updatePlayerScore(self):
        """
        Calculate the players new score by subtracting the throw total.
        If the new score is below zero return False, otherwise update the players score 
        and return True.
        """
        newScore = self.active_player.getScore() - self.throw_total
        
        #reset throw total for next round
        self.throw_total = 0

        if newScore < 0:
            return False

        else:
            self.active_player.setScore(newScore)
            return True
        
    def checkPlayerScore(self):
        """
        Check if the players score has reached zero.
        If it has return True, otherwise return False.
        """
        score = self.active_player.getScore()
        
        if score == 0:

            return True

        else:
            
            return False
     
    def getDartOne(self):
        """
        return score and multiplier for dart 1
        """
        return self.dart_1,self.dart_1_mult

    def getDartTwo(self):
        """
        return score and multiplier for dart 2
        """

        return self.dart_2,self.dart_2_mult

    def getDartThree(self):
        """
        return score and multiplier for dart 3
        """

        return self.dart_3,self.dart_3_mult

    def updateDartOne(self,newDart1,newMult1):
        """
        update score and multiplier for dart 1
        """

        self.dart_1 = newDart1
        self.dart_1_mult = newMult1

    def updateDartTwo(self,newDart2,newMult2):
        """
        update score and multiplier for dart 2
        """
    
        self.dart_2 = newDart2
        self.dart_2_mult = newMult2

    def updateDartThree(self,newDart3,newMult3):
        """
        return score and multiplier for dart 3
        """
    
        self.dart_3 = newDart3
        self.dart_3_mult = newMult3

