class Player:
    def __init__(self, row):
        self.name = row['Player Name']
        self.RHP = row["HPRHP"]
        self.LHP = row["HPLHP"]
        self.HPFlyball = row['HPFlyball']
        self.HPPower = row['HPPower']
        self.HPAvg = row['HPAvg']
        self.HPFinese = row['HPFinese']
        self.HPHome = row['HPHome']
        self.HPAway = row['HPAway']
        self.HPGroundball = row['HPGroundball']