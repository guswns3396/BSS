import unittest
from io import StringIO
from unittest.mock import patch
from code.Game import *
from code.Player import Hitter, Pitcher

class TestGame(unittest.TestCase):
    def test_str_printsCorrectLength(self):
        game = Game('',[],[],{})

        with patch('sys.stdout', new=StringIO()) as out:
            print(game)
            output = out.getvalue()

        output = output[:-1]
        expected = 1 + MAX_HITTERS * NUM_FEATURES_HITTER + MAX_PITCHERS * NUM_FEATURES_PITCHER + MAX_HITTERS
        self.assertEqual(expected, len(output.split(',')))

    def test_str_printsCorrectFormat(self):
        id = 'id'
        hitters = [Hitter('hitter1', 'endpoint1', 1, 2, 3, 4, 5),
                   Hitter('hitter2', 'endpoint2', 6, 7, 8, 9, 10)]
        pitchers = [Pitcher('pitcher1', 'endpoint1', 1, 2, 3, 4, 5, 6, 7),
                    Pitcher('pitcher2', 'endpoint2', 8, 9, 10, 11, 12, 13, 14)]
        outcome = {'endpoint1': .7, 'endpoint2': .3}
        game = Game(id,hitters,pitchers,outcome)

        with patch('sys.stdout', new=StringIO()) as out:
            print(game)
            output = out.getvalue()

        expected = 'id,1,2,3,4,5,6,7,8,9,10,'
        expected += '0,0,0,0,0,'*24
        expected += '1,2,3,4,5,6,7,8,9,10,11,12,13,14,'
        expected += '0,0,0,0,0,0,0,'*11
        expected += '0.7,0.3,'
        expected += '0,'*24
        expected = expected[:-1] + '\n'
        self.assertEqual(expected, output)
