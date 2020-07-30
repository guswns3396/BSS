import unittest
from code import webscrape_training as wst

class TestWebscrape(unittest.TestCase):
    def test_extractGamesFromSeason_extractsAllEndpoints(self):
        endpoints_game = wst.extractGamesFromSeason(2015)

        self.assertEqual(2465,len(endpoints_game))

    def test_extractTeams_extractsTeams(self):
        endpoint_game = "/boxes/ARI/ARI201504060.shtml"

        team_away, team_home = wst.extractTeams(endpoint_game)

        isAway = team_away == "San Francisco Giants"
        isHome = team_home == "Arizona Diamondbacks"
        self.assertTrue(isAway and isHome)

    def test_extractTeamID_extractsSameCapitalization(self):
        team_name = "Los Angeles Angels of Anaheim"

        team_id = wst.extractTeamID(team_name)

        self.assertEqual("LosAngelesAngelsofAnaheim", team_id)

    def test_extractTeamID_extractsOnlyAlphabets(self):
        team_name = "St. Louis Cardinals"

        team_id = wst.extractTeamID(team_name)

        self.assertEqual("StLouisCardinals", team_id)

if __name__ == "__main__":
    unittest.main()