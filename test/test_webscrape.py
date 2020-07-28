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

if __name__ == "__main__":
    unittest.main()