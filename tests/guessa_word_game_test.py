import unittest
from guessa_word_game import GuessResult


class WorldGameTest(unittest.TestCase):

    def test_guess_result(self):
        self.assertEqual("CCWWG", GuessResult("hello", "heyal").create_matching_info_str())
        self.assertEqual("GWCGW", GuessResult("sweet", "toesn").create_matching_info_str())
        self.assertEqual("GCCCG", GuessResult("sweet", "twees").create_matching_info_str())
        self.assertEqual("CCWCC", GuessResult("sigma", "siama").create_matching_info_str())
