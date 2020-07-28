import unittest
import webscrape

class TestWebscrape(unittest.TestCase):
    def test_extractTeams_extractsAllActiveTeams(self):
        teams = webscrape.extractTeams()

        self.assertEqual(len(teams),30)

if __name__ == "__main__":
    unittest.main()