import unittest
from code import webscrape_training as ws

class TestWebscrape(unittest.TestCase):
    def test_extractGamesFromSeason_extractsAllEndpoints(self):
        endpoints_game = ws.extractGamesFromSeason(2015)

        self.assertEqual(2465,len(endpoints_game))

    def test_extractTeams_extractsTeams(self):
        endpoint_game = "/boxes/ARI/ARI201504060.shtml"

        team_away, team_home = ws.extractTeams(endpoint_game)

        isAway = team_away == "San Francisco Giants"
        isHome = team_home == "Arizona Diamondbacks"
        self.assertTrue(isAway and isHome)

if __name__ == "__main__":
    unittest.main()