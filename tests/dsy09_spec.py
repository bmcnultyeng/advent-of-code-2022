import unittest

from src.day09 import Rope


class DayTests(unittest.TestCase):
    def test_Rope(self):
        # test the basics of the Rope class
        rope_1 = Rope("data/day09_motions_test.txt")  # test with known data_lines
        self.assertEqual(8, len(rope_1.moves))
        self.assertEqual(("R", 4), rope_1.moves[0])

    def test_move_tail(self):
        rope_2 = Rope("data/day09_motions_test.txt")
        rope_2.move_head("R")
        self.assertEqual([1, 0], rope_2.head_pos)
        rope_2.move_head("R")
        rope_2.adjust_tail()
        self.assertEqual([2, 0], rope_2.head_pos)
        self.assertEqual([1, 0], rope_2.tail_pos)
        rope_2.move_head("U")
        rope_2.adjust_tail()
        rope_2.move_head("U")
        rope_2.adjust_tail()
        self.assertEqual([2, 2], rope_2.head_pos)
        self.assertEqual([2, 1], rope_2.tail_pos)
        self.assertEqual(3, len(rope_2.unique_tail_positions))

    def test_execute_commands(self):
        rope_1 = Rope("data/day09_motions_test.txt")
        rope_1.execute_moves()
        self.assertEqual(13, len(rope_1.unique_tail_positions))
        # Part #1 solution
        rope_2 = Rope("data/day09_motions_bm.txt")
        rope_2.execute_moves()
        self.assertEqual(6037, len(rope_2.unique_tail_positions))
        # test Part #2
        rope_3 = Rope("data/day09_motions_test.txt")
        rope_3.execute_moves(part2=True)
        self.assertEqual(1, len(rope_3.unique_tail_positions))
        rope_4 = Rope("data/day09_motions_test2.txt")  # larger example
        rope_4.execute_moves(part2=True)
        self.assertEqual(36, len(rope_4.unique_tail_positions))
        # Part #2 solution
        rope_5 = Rope("data/day09_motions_bm.txt")
        rope_5.execute_moves(part2=True)
        self.assertEqual(2485, len(rope_5.unique_tail_positions))
