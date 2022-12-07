import unittest

from src.day02 import my_score


class DayO1Tests(unittest.TestCase):
    def test_my_score(self):  # Part 1
        self.assertEqual(
            15,
            my_score("data/day02_strategy_test.txt"),
        )
        self.assertEqual(15572, my_score("data/day02_strategy_bm.txt"))
        # self.assertEqual(2000, my_score("data/day02_strategy_tm.txt")))

    def test_my_score_2(self):  # Part 2
        self.assertEqual(
            12,
            my_score("data/day02_strategy_test.txt", 2),
        )
        self.assertEqual(16098, my_score("data/day02_strategy_bm.txt", 2))
        # self.assertEqual(2000, my_score("data/day02_strategy_tm.txt",2)))
