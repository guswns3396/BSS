import code.Player as Player

class Game:
    def __init__(self, id, hitters, pitchers, outcome):
        """
        instantiates Game object
        :param id: id of the game (endpoint_game + '-A' or '-H' for away or home)
        :param hitters: list of Hitter objects
        :param pitchers: list of Pitcher objects
        :param outcome: dictionary that maps hitter to percentage
         the player contributed to team's hits
        """
        self.id = id
        self.hitters = hitters
        self.pitchers = pitchers
        self.outcome = outcome

    def convertToNDArray(self):
        """
        converts the object into ND array for model input
        so that the model can actually do calculations with it
        :return: X, y
        """
        pass