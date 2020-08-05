import unittest
import copy

import sys
import pathlib
path_dir = pathlib.Path(__file__).parent.absolute()
path_repo = path_dir.parent.absolute()
sys.path.insert(1, path_repo)

import Player

class TestPlayer(unittest.TestCase):
    def test_constructor_constructsHitter(self):
        player = Player.Hitter('Test Name','Test End',0,0,0,0,0)

        self.assertIsInstance(player, Player.Hitter)

    def test_constructor_constructsCorrectHitter(self):
        player = Player.Hitter('Test Name', 'Test End', 0, 0, 0, 0, 0)

        self.assertEqual(player.name, 'Test Name')

    def test_constructor_constructsPitcher(self):
        player = Player.Pitcher('Test Name','Test End',0,0,0,0,0,0,0)

        self.assertIsInstance(player, Player.Pitcher)

    def test_constructor_constructsCorrectPitcher(self):
        player = Player.Pitcher('Test Name', 'Test End', 0, 0, 0, 0, 0, 0, 0)

        self.assertEqual(player.name, 'Test Name')

    def test_equalOverload_returnsTrueIfSameHitter(self):
        p1 = Player.Hitter('1','1',0,0,0,0,0)
        p2 = Player.Hitter('1','1',0,0,0,0,0)

        isEqual = p1 == p2

        self.assertTrue(isEqual)

    def test_equalOverload_returnsFalseIfDifferentHitter(self):
        p1 = Player.Hitter('1', '1', 0, 0, 0, 0, 0)
        p2 = Player.Hitter('2', '2', 0, 0, 0, 0, 0)

        isNotEqual = p1 != p2

        self.assertTrue(isNotEqual)

    def test_equalOverload_returnsTrueIfSamePitcher(self):
        p1 = Player.Pitcher('1', '1', 0, 0, 0, 0, 0, 0, 0)
        p2 = Player.Pitcher('1', '1', 0, 0, 0, 0, 0, 0, 0)

        isEqual = p1 == p2

        self.assertTrue(isEqual)

    def test_equalOverload_returnsFalseIfDifferentPitcher(self):
        p1 = Player.Pitcher('1', '1', 0, 0, 0, 0, 0, 0, 0)
        p2 = Player.Pitcher('2', '2', 0, 0, 0, 0, 0, 0, 0)

        isNotEqual = p1 != p2

        self.assertTrue(isNotEqual)

    def test_update_updatesHitter(self):
        data = {'PA': 1, 'H': 1, 'SO': 1}
        player = Player.Hitter('', '', 0, 0, 0, 0, 0)

        player.updateStats(data)

        expected = Player.Hitter('','',1,1,1,0,0)
        self.assertEqual(expected, player)

    def test_update_updatesPitcher(self):
        data = {'SHO': 1, 'IP': 1, 'H': 1, 'SO': 1, 'BF': 1}
        player = Player.Pitcher('', '', 0, 0, 0, 0, 0, 0, 0)

        player.updateStats(data)

        expected = Player.Pitcher('', '', 1, 1, 1, 1, 1, 0, 0)
        self.assertEqual(expected, player)

    def test_deepcopy_copiesHitter(self):
        hitters = []
        hitter = Player.Hitter('','',0,0,0,0,0)

        hitters.append(copy.deepcopy(hitter))

        hitter.updateStats({'PA': 1, 'H': 1, 'SO': 1})
        self.assertNotEqual(hitters[0], hitter)

    def test_deepcopy_copiesPitcher(self):
        pitchers = []
        pitcher = Player.Pitcher('', '', 0, 0, 0, 0, 0, 0, 0)

        pitchers.append(copy.deepcopy(pitcher))

        pitcher.updateStats({'SHO': 1, 'IP': 1, 'H': 1, 'SO': 1, 'BF': 1})
        self.assertNotEqual(pitchers[0], pitcher)

if __name__ == '__main__':
    unittest.main()
