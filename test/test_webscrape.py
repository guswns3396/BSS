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

    def test_extractPlayerEndpointsFromTable_extractsCorrectEndpoint(self):
        endpoint = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        search_id = "StLouisCardinalsbatting"
        table = ws.searchForTable(soup, search_id)

        endpoint_players = ws.extractPlayerEndpointsFromTable(table)

        self.assertEqual("/players/c/carpema01.shtml", endpoint_players[0])

    def test_extractPlayerEndpointsFromTable_extractsAllEndpoints(self):
        endpoint = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        search_id = "StLouisCardinalsbatting"
        table = ws.searchForTable(soup, search_id)

        endpoint_players = ws.extractPlayerEndpointsFromTable(table)

        self.assertEqual(14, len(endpoint_players))

    def test_extractHitterOutcome_extractsCorrectOutcome(self):
        endpoint = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        search_id = "StLouisCardinalsbatting"
        table = ws.searchForTable(soup, search_id)
        endpoint_player = "/players/h/heywaja01.shtml"

        h_contribution = ws.extractHitterOutcome(table, endpoint_player)

        self.assertEqual(3/10, h_contribution)

    def test_extractPlayerName_extractsCorrectName(self):
        endpoint = "/players/p/peraljh01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        name = ws.extractPlayerName(div)

        self.assertEqual("Jhonny Peralta", name)

    def test_extractPlayerHand_extractsHitterRight(self):
        endpoint = "/players/p/peraljh01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        r, l = ws.extractPlayerHand(div, 'hitter')

        self.assertTrue(r == 1 and l == 0)

    def test_extractPlayerHand_extractsHittersLeft(self):
        endpoint = "/players/c/carpema01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        r, l = ws.extractPlayerHand(div, 'hitter')

        self.assertTrue(r == 0 and l == 1)

    def test_extractPlayerHand_extractsHitterBoth(self):
        # cannot find case (not in bio)
        pass

    def test_extractPlayerHand_extractsPitcherRight(self):
        endpoint = "/players/w/wainwad01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        r, l = ws.extractPlayerHand(div, 'pitcher')

        self.assertTrue(r == 1 and l == 0)

    def test_extractPlayerHand_extractsPitcherLeft(self):
        endpoint = "/players/c/cokeph01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        r, l = ws.extractPlayerHand(div, 'pitcher')

        self.assertTrue(r == 0 and l == 1)

    def test_extractPlayerHand_extractsPitcherBoth(self):
        # cannot find case (not in bio)
        pass

    def test_extractSeasonStatsFromTable_defaultIfTableNotFoundHitter(self):
        output = ws.extractSeasonStatsFromTable(None, 'hitter', 2020)

        expected = {'PA': 0, 'H': 0, 'SO': 0}
        self.assertEqual(expected, output)

    def test_extractSeasonStatsFromTable_defaultIfTableNotFoundPitcher(self):
        output = ws.extractSeasonStatsFromTable(None, 'pitcher', 2020)

        expected = {'SHO': 0, 'IP': 0.0, 'H': 0, 'SO': 0, 'BF': 0}
        self.assertEqual(expected, output)

    def test_extractSeasonStatsFromTable_defaultIfYearNotFoundHitter(self):
        endpoint = "/players/w/wainwad01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'batting_standard')

        output = ws.extractSeasonStatsFromTable(table, 'hitter', 2021)

        expected = {'PA': 0, 'H': 0, 'SO': 0}
        self.assertEqual(expected, output)

    def test_extractSeasonStatsFromTable_defaultIfYearNotFoundPitcher(self):
        endpoint = "/players/w/wainwad01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'pitching_standard')

        output = ws.extractSeasonStatsFromTable(table, 'pitcher', 2021)

        expected = {'SHO': 0, 'IP': 0.0, 'H': 0, 'SO': 0, 'BF': 0}
        self.assertEqual(expected, output)

    def test_extractSeasonStatsFromTable_extractsStatsHitter(self):
        endpoint = "/players/w/wainwad01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'batting_standard')

        output = ws.extractSeasonStatsFromTable(table, 'hitter', 2007)

        expected = {'PA': 74, 'H': 18, 'SO': 18}
        self.assertEqual(expected, output)

    def test_extractSeasonStatsFromTable_extractsStatsPitcher(self):
        endpoint = "/players/w/wainwad01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'pitching_standard')

        output = ws.extractSeasonStatsFromTable(table, 'pitcher', 2010)

        expected = {'SHO': 2, 'IP': 230.1, 'H': 186, 'SO': 213, 'BF': 910}
        self.assertEqual(expected, output)

    def test_checkPlayersLastSeasonStats_(self):
        endpoint = "/players/c/carpema01.shtml"

        ws.checkPlayersLastSeasonStats(endpoint, 'hitter', 2020)

if __name__ == "__main__":
    unittest.main()