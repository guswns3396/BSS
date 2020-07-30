import unittest
from code import webscrape as ws

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

    def test_extractTeamID_extractsSameCapitalization(self):
        team_name = "Los Angeles Angels of Anaheim"

        team_id = ws.extractTeamID(team_name)

        self.assertEqual("LosAngelesAngelsofAnaheim", team_id)

    def test_extractTeamID_extractsOnlyAlphabets(self):
        team_name = "St. Louis Cardinals"

        team_id = ws.extractTeamID(team_name)

        self.assertEqual("StLouisCardinals", team_id)

    def test_searchForTable_searchesTableWithID(self):
        endpoint = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        search_id = "StLouisCardinalsbatting"

        table = ws.searchForTable(soup, search_id)

        caption = table.find("caption").string
        self.assertEqual("St. Louis Cardinals Table", caption)

    def test_searchForTable_returnsNoneIfNotFound(self):
        endpoint = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        search_id = "this_is_a_test_id"

        table = ws.searchForTable(soup, search_id)

        self.assertEqual(None, table)

if __name__ == "__main__":
    unittest.main()