class Player:
    def __init__(self, name):
        self.name = name

class Hitter(Player):
    def __init__(self, name, pa, h, so, r, l):
        super().__init__(name)
        self.PA = pa
        self.H = h
        self.SO = so
        self.R = r
        self.L = l

class Pitcher(Player):
    def __init__(self, name, sho, ip, h, so, bf, r, l):
        super().__init__(name)
        self.SHO = sho
        self.IP = ip
        self.H = h
        self.SO = so
        self.BF = bf
        self.R = r
        self.L = l