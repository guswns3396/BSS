import unittest
import webscrape

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

        teams = webscrape.extractRoster(teams)

        self.assertEqual(len(teams[0].batting), 25)

    def test_extractRoster_extractsAllPitchers(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        teams = webscrape.extractRoster(teams)

        self.assertEqual(len(teams[0].pitching), 12)

    def test_extractRoster_extractsNameAndEndpoint(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]

        teams = webscrape.extractRoster(teams)

        expected = "Carson Kelly /players/k/kellyca02.shtml"
        output = teams[0].batting[0].name + " " + teams[0].batting[0].endpoint
        self.assertEqual(expected, output)

if __name__ == "__main__":
    unittest.main()