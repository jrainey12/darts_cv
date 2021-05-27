class GameType():
    """
    Generic game type class.
    """
    
    def __init__(self):

        self.active_player = None

        self.max_score = None


    def changePlayer(self,newPlayer):
        """
        Change the active player.
        param: newPlayer - new active player.
        """
        self.active_player = newPlayer

    def getActivePlayer(self):
        """
        Return the active player.
        """

        return self.active_player


    def setMaxScore(self,score):
        """
        Set the max score for the game.
        """
        self.max_score = score


    def getMaxScore(self):
        """
        Return the max score.
        """
        return self.max_score
