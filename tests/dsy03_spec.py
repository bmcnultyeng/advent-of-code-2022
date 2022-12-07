import unittest

from src.day03 import calc_priority, priorities, calc_group_priority, group_priorities


class DayTests(unittest.TestCase):
    def test_calc_priority(self):  # Part 1
        self.assertEqual(
            16, calc_priority("vJrwpWtwJgWrhcsFMMfFFhFp")  # first line of test data
        )

    def test_priorities(self):  # Part 1
        self.assertEqual(157, priorities("data/day03_rucksack_test.txt"))
        self.assertEqual(8109, priorities("data/day03_rucksack_bm.txt"))

    def test_calc_group_priority(self):  # Part 2
        self.assertEqual(
            18,
            calc_group_priority(
                [
                    "vJrwpWtwJgWrhcsFMMfFFhFp",
                    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                    "PmmdzqPrVvPwwTWBwg",
                ]
            ),  # first 3 lines of test data
        )

    def test_group_priorities(self):  # Part 2
        self.assertEqual(70, group_priorities("data/day03_rucksack_test.txt"))
        self.assertEqual(2738, group_priorities("data/day03_rucksack_bm.txt"))

    # def test_my_score_2(self):  # Part 2
    #     self.assertEqual(
    #         12,
    #         my_score("data/day02_strategy_test.txt", 2),
    #     )
    #     self.assertEqual(16098, my_score("data/day02_strategy_bm.txt", 2))
    #     # self.assertEqual(2000, my_score("data/day02_strategy_tm.txt",2)))
