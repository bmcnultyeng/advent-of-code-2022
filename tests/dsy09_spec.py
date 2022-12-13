import unittest

from src.day10 import Computer


class DayTests(unittest.TestCase):
    def test_Computer(self):
        # test the basics of the Computer class
        puter_1 = Computer("data/day10_program_test1.txt")  # test with known data_lines
        self.assertEqual("noop", puter_1.commands[0][0])
        self.assertEqual(("addx", 3), puter_1.commands[1])
        self.assertEqual(("addx", -5), puter_1.commands[2])
        puter_1 = Computer("data/day10_program_test1.txt")  # test with known data_lines

    def test_execute_command(self):
        puter_1 = Computer("data/day10_program_test1.txt")  # short sample command list
        puter_1.execute_command(("addx", 5))
        self.assertEqual(6, puter_1.reg_x)

    def test_run_program(self):
        puter_1 = Computer("data/day10_program_test2.txt")  # longer sample command list
        self.assertEqual(13140, puter_1.run_program())

    # def test_move_tail(self):
    #     rope_2 = Rope("data/day09_motions_test.txt")
    #     rope_2.move_head("R")
    #     self.assertEqual([1, 0], rope_2.head_pos)
    #     rope_2.move_head("R")
    #     rope_2.adjust_tail()
    #     self.assertEqual([2, 0], rope_2.head_pos)
    #     self.assertEqual([1, 0], rope_2.tail_pos)
    #     rope_2.move_head("U")
    #     rope_2.adjust_tail()
    #     rope_2.move_head("U")
    #     rope_2.adjust_tail()
    #     self.assertEqual([2, 2], rope_2.head_pos)
    #     self.assertEqual([2, 1], rope_2.tail_pos)
    #     self.assertEqual(3, len(rope_2.unique_tail_positions))

    # def test_execute_commands(self):
    #     rope_1 = Rope("data/day09_motions_test.txt")
    #     rope_1.execute_moves()
    #     self.assertEqual(13, len(rope_1.unique_tail_positions))
    #     # Part #1 solution
    #     rope_2 = Rope("data/day09_motions_bm.txt")
    #     rope_2.execute_moves()
    #     self.assertEqual(6037, len(rope_2.unique_tail_positions))
    #     # test Part #2
    #     rope_3 = Rope("data/day09_motions_test.txt")
    #     rope_3.execute_moves(part2=True)
    #     self.assertEqual(1, len(rope_3.unique_tail_positions))
    #     rope_4 = Rope("data/day09_motions_test2.txt")  # larger example
    #     rope_4.execute_moves(part2=True)
    #     self.assertEqual(36, len(rope_4.unique_tail_positions))
    #     # Part #2 solution
    #     rope_5 = Rope("data/day09_motions_bm.txt")
    #     rope_5.execute_moves(part2=True)
    #     self.assertEqual(2485, len(rope_5.unique_tail_positions))
