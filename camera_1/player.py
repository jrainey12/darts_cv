

class Player():
    """
    Basic player class holding a name and a score.

    """
    def __init__(self,name,score):

        self.name = name
        self.score = score

        
    def getName(self):
        """
        Get the player name.
        return: name - players name.
        """
        return self.name

    def getScore(self): 
        """
        Get the players score.
        return: score
        """
        return self.score

    def setName(self,newName):
        """
        Update the players name.
        param: newName - new name to set.
        """
        self.name = newName

    def setScore(self,newScore):
        """
        Update the players score.
        param: newScore - and int for X01 or a list for cricket.
        """
        self.score = newScore

    
