class Player:
    def __init__(self, name):
        self.name = name

class Hitter(Player):
    def __init__(self, name, rhp, lhp, power, avg, finesse, ground, fly, home, away):
        super().__init__(name)
        self.HPRHP = rhp
        self.HPLHP = lhp
        self.HPPower = power
        self.HPAvg = avg
        self.HPFinesse = finesse
        self.HPGroundball = ground
        self.HPFlyball = fly
        self.HPHome = home
        self.HPAway = away

class Pitcher(Player):
    def __init__(self, name, rhb, lhb):
        super().__init__(name)
        self.RHB = rhb
        self.LHB = lhb