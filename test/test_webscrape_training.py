import unittest
from code import webscrape_training as ws

class TestWebscrape(unittest.TestCase):
    def test_extractGamesFromSeason_extractsAllEndpoints(self):
        endpoints_game = ws.extractGamesFromSeason(2015)

        self.assertEqual(2465,len(endpoints_game))

if __name__ == "__main__":
    unittest.main()