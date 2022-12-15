import unittest

from src.day11 import Monkees


class DayTests(unittest.TestCase):
    def test_Monkees(self):
        # test the basics of the class & initialized data lists
        monk_1 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        self.assertEqual([0, 0, 0, 0], monk_1.inspections)
        self.assertEqual([[79, 98], [54, 65, 75, 74], [79, 60, 97], [74]], monk_1.items)
        self.assertEqual(
            [
                ["old * 19", 23, 2, 3],
                ["old + 6", 19, 2, 0],
                ["old * old", 13, 1, 3],
                ["old + 3", 17, 0, 1],
            ],
            monk_1.rules,
        )

    def test_monkey_turn(self):
        monk_1 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        monk_1.monkey_turn(0)  # 1st turn of 1st monkey
        self.assertEqual([2, 0, 0, 0], monk_1.inspections)
        self.assertEqual(
            [[], [54, 65, 75, 74], [79, 60, 97], [74, 500, 620]], monk_1.items
        )

    def test_do_rounds(self):
        monk_1 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        self.assertEqual(10605, monk_1.do_rounds())  # default 20 rounds
        self.assertEqual(
            [[10, 12, 14, 26, 34], [245, 93, 53, 199, 115], [], []], monk_1.items
        )
        monk_2 = Monkees("data/day11_monkey_bm.txt")
        # Part #1 solution
        self.assertEqual(113_232, monk_2.do_rounds())  # default 20 rounds

        # Part #2
        monk_3 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        self.assertEqual(10197, monk_3.do_rounds(20, part2=True))
        monk_4 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        self.assertEqual(27019168, monk_4.do_rounds(1000, part2=True))
        monk_5 = Monkees("data/day11_monkey_test.txt")  # test with known data_lines
        self.assertEqual(2713310158, monk_5.do_rounds(10000, part2=True))
        # Part #2 solution
        monk_6 = Monkees("data/day11_monkey_bm.txt")
        self.assertEqual(29703395016, monk_6.do_rounds(10000, part2=True))
