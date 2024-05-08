import unittest
from guessa_word_game import GuessResult


class WorldGameTest(unittest.TestCase):

    def test_process_guess(self):
        matched, correct_but_wrong_place, wrong = GuessResult._process_guess("hello", "heyal")
        self.assertEqual("he---", matched)
        self.assertEqual("----l", correct_but_wrong_place)
        self.assertEqual("ya", wrong)

        matched, correct_but_wrong_place, wrong = GuessResult._process_guess("sweet", "toesn")
        self.assertEqual("--e--", matched)
        self.assertEqual("t--s-", correct_but_wrong_place)
        self.assertEqual("on", wrong)

        matched, correct_but_wrong_place, wrong = GuessResult._process_guess("sweet", "twees")
        self.assertEqual("-wee-", matched)
        self.assertEqual("t---s", correct_but_wrong_place)
        self.assertEqual("", wrong)
