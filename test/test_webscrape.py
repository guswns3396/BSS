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

    def test_searchForTable_parsesCommentedOutBattingTable(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]
        teams[0].batting.append(webscrape.Member("Luke Weaver", "/players/w/weavelu01.shtml"))
        page = webscrape.requests.get(webscrape.URL + teams[0].batting[0].endpoint)
        soup = webscrape.BeautifulSoup(page.content, 'html.parser')

        table = webscrape.searchForTable(soup, "batting_standard")

        a = table.find("a", string="162 Game Avg.")
        th = a.find_parent("th")
        plate_appearance = int(th.find_next_sibling(attrs={"data-stat": "PA"}).string)
        self.assertEqual(238, plate_appearance)

    def test_searchForTable_parsesCommentedOutPitchingTable(self):
        # could not find example where pitching table is commented out
        pass

    def test_searchForTable_returnsNoneIfNotFound(self):
        teams = [webscrape.Team("Arizona Diamondbacks", "/teams/ARI/")]
        teams[0].batting.append(webscrape.Member("Taylor Widener", "/players/w/widenta01.shtml"))
        page = webscrape.requests.get(webscrape.URL + teams[0].batting[0].endpoint)
        soup = webscrape.BeautifulSoup(page.content, 'html.parser')

        table = webscrape.searchForTable(soup, "batting_standard")

        self.assertEqual(None, table)

    def test_extractFromTable_extractsBattingData(self):
        page = webscrape.requests.get(webscrape.URL + "/players/k/kellyca02.shtml")
        soup = webscrape.BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id='batting_standard')

        output = webscrape.extractFromTable(table,'hitter')

        expected = {'rhp': 0, 'lhp': 1, 'pow': 2, 'avg': 3, 'fin': 4,
                    'gro': 5, 'fly': 6, 'hme': 7, 'awy': 8}
        self.assertEqual(expected, output)

    def test_extractFromTable_extractsPitchingData(self):
        page = webscrape.requests.get(webscrape.URL + "/players/b/bumgama01.shtml")
        soup = webscrape.BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id='pitching_standard')

        output = webscrape.extractFromTable(table, 'pitcher')

        expected = {'rhb': 192 / 218, 'lhb': 1}
        self.assertEqual(expected, output)

    def test_extractFromTable_returnDefaultIfBattingTableNotFound(self):
        table = None

        output = webscrape.extractFromTable(table, 'hitter')

        expected = {'rhp': 0, 'lhp': 1, 'pow': 2, 'avg': 3, 'fin': 4,
                    'gro': 5, 'fly': 6, 'hme': 7, 'awy': 8}
        self.assertEqual(expected, output)

    def test_extractFromTable_returnDefaultIfPitchingTableNotFound(self):
        table = None

        output = webscrape.extractFromTable(table, 'pitcher')

        expected = {'rhb': 0, 'lhb': 1}
        self.assertEqual(expected, output)

    def test_extractFromTable_raisesExceptionIfInvalidArgument(self):
        table = None

        with self.assertRaises(Exception) as context:
            output = webscrape.extractFromTable(table)

        self.assertIsInstance(context.exception, ValueError)

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

    def test_exportPitchersToCSV_outputsCorrectData(self):
        pitchers = [webscrape.Player.Pitcher("test", 0, 1)]

        webscrape.exportPitchersToCSV(pitchers)

        with open("../data/pitchers.csv", "r") as f:
            f.readline()
            row = f.readline()
            row = row.split(",")
        self.assertEqual(row[1], str(0))

if __name__ == "__main__":
    unittest.main()