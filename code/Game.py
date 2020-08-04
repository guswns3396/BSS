MAX_HITTERS = 26
MAX_PITCHERS = 13

class Game:
    def __init__(self, id, hitters, pitchers, outcome):
        """
        instantiates Game object
        :param id: id of the game (endpoint_game + '-A' or '-H' for away or home)
        :param hitters: list of Hitter objects
        :param pitchers: list of Pitcher objects
        :param outcome: dictionary that maps endpoint of hitter to percentage
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

    def __str__(self):
        row = []
        row.append(self.id)
        i = 0
        for hitter in self.hitters:
            row.append(hitter.PA)
            row.append(hitter.H)
            row.append(hitter.SO)
            row.append(hitter.R)
            row.append(hitter.L)
            i += 1
        while i < MAX_HITTERS:
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            i += 1
        i = 0
        for pitcher in self.pitchers:
            row.append(pitcher.SHO)
            row.append(pitcher.IP)
            row.append(pitcher.H)
            row.append(pitcher.SO)
            row.append(pitcher.BF)
            row.append(pitcher.R)
            row.append(pitcher.L)
            i += 1
        while i < MAX_PITCHERS:
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            row.append(0)
            i += 1
        return ','.join(row)
