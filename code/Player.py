class Player:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

class Hitter(Player):
    def __init__(self, name, endpoint, pa, h, so, r, l):
        super().__init__(name, endpoint)
        self.PA = pa
        self.H = h
        self.SO = so
        self.R = r
        self.L = l

    def updateStats(self, data):
        self.PA += data['PA']
        self.H += data['H']
        self.SO += data['SO']

class Pitcher(Player):
    def __init__(self, name, endpoint, sho, ip, h, so, bf, r, l):
        super().__init__(name, endpoint)
        self.SHO = sho
        self.IP = ip
        self.H = h
        self.SO = so
        self.BF = bf
        self.R = r
        self.L = l

    def updateStats(self, data):
        self.SHO += data['SHO']
        self.IP += data['IP']
        self.H += data['H']
        self.SO += data['SO']
        self.BF += data['BF']
