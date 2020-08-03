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

    def __deepcopy__(self, memodict={}):
        id_self = id(self)
        _copy = memodict.get(id_self)
        if _copy is None:
            _copy = Hitter(self.name, self.endpoint, self.PA, self.H, self.SO, self.R, self.L)
            memodict[id_self] = _copy
        return _copy

    def __eq__(self, other):
        if not isinstance(other, Hitter):
            raise NotImplemented
        eqName = self.name == other.name
        eqEndpoint = self.endpoint == other.endpoint
        eqPA = self.PA  == other.PA
        eqH = self.H == other.H
        eqSO = self.SO == other.SO
        eqR = self.R == other.R
        eqL = self.L == other.L
        if eqName and eqEndpoint and eqPA and eqH and eqSO and eqR and eqL:
            return True
        else:
            return False

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

    def __deepcopy__(self, memodict={}):
        id_self = id(self)
        _copy = memodict.get(id_self)
        if _copy is None:
            _copy = Pitcher(self.name, self.endpoint, self.SHO, self.IP, self.H, self.SO, self.BF, self.R, self.L)
            memodict[id_self] = _copy
        return _copy

    def __eq__(self, other):
        if not isinstance(other, Pitcher):
            raise NotImplemented
        eqName = self.name == other.name
        eqEndpoint = self.endpoint == other.endpoint
        eqSHO = self.SHO  == other.SHO
        eqIP = self.IP == other.IP
        eqH = self.H == other.H
        eqSO = self.SO == other.SO
        eqBF = self.BF == other.BF
        eqR = self.R == other.R
        eqL = self.L == other.L
        if eqName and eqEndpoint and eqSHO and eqIP and eqH and eqSO and eqBF and eqR and eqL:
            return True
        else:
            return False

    def updateStats(self, data):
        self.SHO += data['SHO']
        self.IP += data['IP']
        self.H += data['H']
        self.SO += data['SO']
        self.BF += data['BF']
