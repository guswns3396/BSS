class Hitter:
    def __init__(self, row):
        self.name = row['Player Name']
        self.RHP = float(row["HPRHP"])
        self.LHP = float(row["HPLHP"])
        self.HPFlyball = float(row['HPFlyball'])
        self.HPPower = float(row['HPPower'])
        self.HPAvg = float(row['HPAvg'])
        self.HPFinese = float(row['HPFinese'])
        self.HPHome = float(row['HPHome'])
        self.HPAway = float(row['HPAway'])
        self.HPGroundball = float(row['HPGroundball'])

class Pitcher:
    def __init__(self, row):
        self.name = row['Player Name']
        self.RHB = float(row["HPRHB"])
        self.LHB = float(row["HPLHB"])