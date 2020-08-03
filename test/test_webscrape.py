import unittest
from code import webscrape as ws

class TestWebscrape(unittest.TestCase):
    def test_extractGamesFromSeason_extractsAllEndpoints(self):
        endpoints_game = ws.extractGamesFromSeason(2015)

        self.assertEqual(2465,len(endpoints_game))

    def test_extractTeams_extractsTeams(self):
        endpoint_game = "/boxes/ARI/ARI201504060.shtml"
        page = ws.requests.get(ws.URL + endpoint_game)
        soup = ws.BeautifulSoup(page.content, 'html.parser')

        team_away, team_home = ws.extractTeams(soup)

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

    def test_extractPlayerHand_raisesExceptionIfInvalidArgument(self):
        endpoint = "/players/c/cokeph01.shtml"
        page = ws.requests.get(ws.URL + endpoint)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        selector = "#meta div[itemtype='https://schema.org/Person']"
        div = soup.select(selector)[0]

        with self.assertRaises(Exception) as ctx:
            r, l = ws.extractPlayerHand(div, '')

        self.assertIsInstance(ctx.exception, ValueError)

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

    def test_extractSeasonStatsFromTable_raisesExceptionIfInvalidArgument(self):
        table = ws.BeautifulSoup("")

        with self.assertRaises(Exception) as ctx:
            output = ws.extractSeasonStatsFromTable(table, '', 2010)

        self.assertIsInstance(ctx.exception, ValueError)

    def test_checkPlayersLastSeasonStats_raisesExceptionIfInvalidArgument(self):
        endpoint = "/players/c/carpema01.shtml"

        with self.assertRaises(Exception) as ctx:
            player = ws.checkPlayersLastSeasonStats(endpoint, '', 2020)

        self.assertIsInstance(ctx.exception, ValueError)

    def test_checkPlayersLastSeasonStats_extractsCorrectStatsHitter(self):
        endpoint = "/players/c/carpema01.shtml"

        hitter = ws.checkPlayersLastSeasonStats(endpoint, 'hitter', 2014)

        isCorrect = hitter.PA == 717 and hitter.H == 199
        isCorrect = isCorrect and hitter.SO == 98
        isCorrect = isCorrect and hitter.R == 0 and hitter.L == 1
        self.assertTrue(isCorrect)

    def test_checkPlayersLastSeasonStats_extractsCorrectStatsPichter(self):
        endpoint = "/players/w/wainwad01.shtml"

        pitcher = ws.checkPlayersLastSeasonStats(endpoint, 'pitcher', 2014)

        isCorrect = pitcher.SHO == 2 and pitcher.IP == 241.2
        isCorrect = isCorrect and pitcher.H == 223
        isCorrect = isCorrect and pitcher.SO == 219
        isCorrect = isCorrect and pitcher.BF == 956
        isCorrect = isCorrect and pitcher.R == 1 and pitcher.L == 0
        self.assertTrue(isCorrect)

    def test_checkPlayersLastSeasonStats_deafultIfNoTableHitter(self):
        endpoint = "/players/w/widenta01.shtml"

        hitter = ws.checkPlayersLastSeasonStats(endpoint, 'hitter', 2014)

        isCorrect = hitter.PA == 0 and hitter.H == 0
        isCorrect = isCorrect and hitter.SO == 0
        isCorrect = isCorrect and hitter.R == 0 and hitter.L == 1
        self.assertTrue(isCorrect)

    def test_checkPlayersLastSeasonStats_deafultIfNoTablePitcher(self):
        endpoint = "/players/c/carpema01.shtml"

        pitcher = ws.checkPlayersLastSeasonStats(endpoint, 'pitcher', 2014)

        isCorrect = pitcher.SHO == 0 and pitcher.IP == 0
        isCorrect = isCorrect and pitcher.H == 0
        isCorrect = isCorrect and pitcher.SO == 0
        isCorrect = isCorrect and pitcher.BF == 0
        isCorrect = isCorrect and pitcher.R == 1 and pitcher.L == 0
        self.assertTrue(isCorrect)

    def test_checkPlayersLastSeasonStats_deafultIfYearNotFoundHitter(self):
        endpoint = "/players/c/carpema01.shtml"

        hitter = ws.checkPlayersLastSeasonStats(endpoint, 'hitter', 2011)

        isCorrect = hitter.PA == 0 and hitter.H == 0
        isCorrect = isCorrect and hitter.SO == 0
        isCorrect = isCorrect and hitter.R == 0 and hitter.L == 1
        self.assertTrue(isCorrect)

    def test_checkPlayersLastSeasonStats_deafultIfYearNotFoundPitcher(self):
        endpoint = "/players/w/wainwad01.shtml"

        pitcher = ws.checkPlayersLastSeasonStats(endpoint, 'pitcher', 2012)

        isCorrect = pitcher.SHO == 0 and pitcher.IP == 0
        isCorrect = isCorrect and pitcher.H == 0
        isCorrect = isCorrect and pitcher.SO == 0
        isCorrect = isCorrect and pitcher.BF == 0
        isCorrect = isCorrect and pitcher.R == 1 and pitcher.L == 0
        self.assertTrue(isCorrect)

    def test_extractPlayerGamePerformance_extractsHitterData(self):
        endpoint_player = "/players/c/carpema01.shtml"
        endpoint_game = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint_game)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'StLouisCardinalsbatting')

        output = ws.extractPlayerGamePerformance(table, endpoint_player, 'hitter')

        expected = {'PA': 5, 'H': 2, 'SO': 0}
        self.assertEqual(expected, output)

    def test_extractPlayerGamePerformance_extractsPitcherData_noSHO(self):
        endpoint_player = "/players/w/wainwad01.shtml"
        endpoint_game = "/boxes/CHN/CHN201504050.shtml"
        page = ws.requests.get(ws.URL + endpoint_game)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'StLouisCardinalspitching')

        output = ws.extractPlayerGamePerformance(table, endpoint_player, 'pitcher')

        expected = {'IP': 6, 'H': 5, 'SO': 6, 'BF': 23, 'SHO': 0}
        self.assertEqual(expected, output)

    def test_extractPlayerGamePerformance_extractsPitcherData_SHO(self):
        endpoint_player = "/players/t/tanakma01.shtml"
        endpoint_game = "/boxes/TBA/TBA201807240.shtml"
        page = ws.requests.get(ws.URL + endpoint_game)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'NewYorkYankeespitching')

        output = ws.extractPlayerGamePerformance(table, endpoint_player, 'pitcher')

        expected = {'IP': 9, 'H': 3, 'SO': 9, 'BF': 29, 'SHO': 1}
        self.assertEqual(expected, output)

    def test_extractPlayerGamePerformance_raisesExceptionIfInvalidArgument(self):
        endpoint_player = "/players/t/tanakma01.shtml"
        endpoint_game = "/boxes/TBA/TBA201807240.shtml"
        page = ws.requests.get(ws.URL + endpoint_game)
        soup = ws.BeautifulSoup(page.content, 'html.parser')
        table = ws.searchForTable(soup, 'NewYorkYankeespitching')

        with self.assertRaises(Exception) as ctx:
            output = ws.extractPlayerGamePerformance(table, endpoint_player, '')

        self.assertIsInstance(ctx.exception, ValueError)

    def test_extractPlayerCareerStats_raisesExceptionIfInvalidArgument(self):
        with self.assertRaises(Exception) as ctx:
            ws.extractPlayerCareerStats("",{},'',0)

        self.assertIsInstance(ctx.exception, ValueError)

    def test_extractPlayerCareerStats_playerNotInDict(self):
        player_stats = {}
        endpoint_player = "/players/w/wainwad01.shtml"

        output = ws.extractPlayerCareerStats(endpoint_player, player_stats, 'pitcher', 2015)

        expected = ws.Pitcher('Adam Wainwright', endpoint_player, 3, 227.0, 184, 179, 898, 1, 0)
        self.assertEqual(expected, output)

    def test_extractPlayerCareerStats_playerInDict(self):
        endpoint_player = "/players/w/wainwad01.shtml"
        player_stats = {endpoint_player: ws.Pitcher('Adam Wainwright', endpoint_player, 3, 227.0, 184, 179, 898, 1, 0)}

        output = ws.extractPlayerCareerStats(endpoint_player, player_stats, 'pitcher', 2015)

        self.assertEqual(player_stats[endpoint_player], output)

    def test_extractPlayerCareerStats_addsPlayerToDict(self):
        player_stats = {}
        endpoint_player = "/players/w/wainwad01.shtml"

        output = ws.extractPlayerCareerStats(endpoint_player, player_stats, 'pitcher', 2015)

        self.assertTrue(endpoint_player in player_stats)

if __name__ == "__main__":
    unittest.main()