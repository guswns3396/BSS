import unittest
import os
import code.webscrape as webscrape

class TestWebscrape(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        if os.path.isfile("../data/hitters.csv"):
            os.remove("../data/hitters.csv")
        if os.path.isfile("../data/pitchers.csv"):
            os.remove("../data/pitchers.csv")

    def test_extractTeams_extractsAllActiveTeams(self):
        teams = webscrape.extractTeams()

        self.assertEqual(len(teams),30)

    def test_extractTeams_extractsNameAndEndpoint(self):
        teams = webscrape.extractTeams()

        expected = "Arizona Diamondbacks /teams/ARI/"
        self.assertEqual(teams[0].name + " " + teams[0].endpoint, expected)

    def test_extractRoster_extractsAllBatters(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        webscrape.extractRoster(teams)

        self.assertEqual(len(teams[0].batting), 28)

    def test_extractRoster_extractsAllPitchers(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        webscrape.extractRoster(teams)

        self.assertEqual(len(teams[0].pitching), 14)

    def test_extractRoster_extractsNameAndEndpoint(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        webscrape.extractRoster(teams)

        expected = "Carson Kelly /players/k/kellyca02.shtml"
        output = teams[0].batting[0].name + " " + teams[0].batting[0].endpoint
        self.assertEqual(expected, output)

    def test_extractData_extractsBattingData(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]
        teams[0].batting.append(webscrape.Member("Carson Kelly", "/players/k/kellyca02.shtml"))

        hitters, pitchers = webscrape.extractData(teams)

        self.assertEqual(hitters[0].RHP, 86 / 461)

    def test_extractData_extractsPitchingData(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]
        teams[0].pitching.append(webscrape.Member("Madison Bumgarner", "/players/b/bumgama01.shtml"))

        hitters, pitchers = webscrape.extractData(teams)

        self.assertEqual(pitchers[0].RHB, 192 / 218)

    def test_exportHittersToCSV_createsCSVInDataFolder(self):
        hitters = [webscrape.Player.Hitter("test",0,1,2,3,4,5,6,7,8)]

        webscrape.exportHittersToCSV(hitters)

        self.assertTrue(os.path.isfile("../data/hitters.csv"))

    def test_exportHittersToCSV_outputsCorrectData(self):
        hitters = [webscrape.Player.Hitter("test", 0, 1, 2, 3, 4, 5, 6, 7, 8)]

        webscrape.exportHittersToCSV(hitters)

        with open("../data/hitters.csv","r") as f:
            f.readline()
            row = f.readline()
            row = row.split(",")

        self.assertEqual(row[1],str(0))

    def test_exportPitchersToCSV_createsCSVInDataFolder(self):
        pitchers = [webscrape.Player.Pitcher("test",0,1)]

        webscrape.exportPitchersToCSV(pitchers)

        self.assertTrue(os.path.isfile("../data/pitchers.csv"))

    def test_exportPitcherssToCSV_outputsCorrectData(self):
        pitchers = [webscrape.Player.Pitcher("test", 0, 1)]

        webscrape.exportPitchersToCSV(pitchers)

        with open("../data/pitchers.csv", "r") as f:
            f.readline()
            row = f.readline()
            row = row.split(",")

        self.assertEqual(row[1], str(0))

if __name__ == "__main__":
    unittest.main()