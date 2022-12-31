import unittest

from src.day13 import (
    solve_part1_compare,
    solve_part2_compare,
    solve_part1_flatten,
    solve_part2_flatten,
)


class DayTests(unittest.TestCase):
    def test_part1_compare(self):
        self.assertEqual(13, solve_part1_compare("data/day13_signals_test.txt"))
        self.assertEqual(5843, solve_part1_compare("data/day13_signals_bm.txt"))

    def test_part2_compare(self):
        self.assertEqual(140, solve_part2_compare("data/day13_signals_test.txt"))
        self.assertEqual(26289, solve_part2_compare("data/day13_signals_bm.txt"))

    def test_part1_flatten(self):
        self.assertEqual(13, solve_part1_flatten("data/day13_signals_test.txt"))
        self.assertEqual(5843, solve_part1_flatten("data/day13_signals_bm.txt"))

    def test_part2_flatten(self):
        self.assertEqual(140, solve_part2_flatten("data/day13_signals_test.txt"))
        self.assertEqual(26289, solve_part2_flatten("data/day13_signals_bm.txt"))
