import unittest
import code.webscrape as webscrape

class TestWebscrape(unittest.TestCase):
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

        self.assertEqual(len(teams[0].batting), 25)

    def test_extractRoster_extractsAllPitchers(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        webscrape.extractRoster(teams)

        self.assertEqual(len(teams[0].pitching), 12)

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

if __name__ == "__main__":
    unittest.main()