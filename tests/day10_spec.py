import unittest

from src.day10 import Computer

# TODO this file was overwritten by day 10 tests; need to restore dsy09_spec.py from repository


class DayTests(unittest.TestCase):
    def test_Computer(self):
        # test the basics of the Computer class
        com_1 = Computer("data/day10_program_test1.txt")  # test with known data_lines
        self.assertEqual("noop", com_1.commands[0][0])
        self.assertEqual(("addx", 3), com_1.commands[1])
        self.assertEqual(("addx", -5), com_1.commands[2])
        com_1 = Computer("data/day10_program_test1.txt")  # test with known data_lines

    def test_execute_command(self):
        com_1 = Computer("data/day10_program_test1.txt")  # short sample command list
        com_1.execute_command(("addx", 5))
        self.assertEqual(6, com_1.reg_x)
        com_2 = Computer("data/day10_program_test1.txt")  # short sample command list
        com_2.execute_command(("addx", 5), part2=True)
        self.assertEqual("##", com_2.pixels[:5])  # 1st 2 cycles of a program

    def test_run_program(self):
        com_1 = Computer("data/day10_program_test2.txt")  # longer sample command list
        self.assertEqual(13140, com_1.run_program())
        # # Part #1 solution
        com_2 = Computer("data/day10_program_bm.txt")
        self.assertEqual(14360, com_2.run_program())

        # # Part 2 (these tests will fail)
        self.maxDiff = None  # to compare long debug errors
        com_1 = Computer("data/day10_program_test2.txt")  # longer sample command list
        self.assertEqual(
            "##..##..##..##..##..##..##..##..##..##..###...###...###...###...###...###...###.####....####....####....####....####....#####.....#####.....#####.....#####.....######......######......######......###########.......#######.......#######.....",
            com_1.run_program(part2=True),
        )
        # Part #2 solution
        #  view as 6 rows of 40 pixels to see 8 capital letters
        com_2 = Computer("data/day10_program_bm.txt")
        self.assertEqual("visual clue", com_2.run_program(part2=True))
        # result: BGKAEREZ ignoring the last column (2 characters per pixel)
        # -  ######      ####    ##    ##    ####    ########  ######    ########  ##########
        # -  ##    ##  ##    ##  ##  ##    ##    ##  ##        ##    ##  ##              ####
        # -  ######    ##        ####      ##    ##  ######    ##    ##  ######        ##  ##
        # -  ##    ##  ##  ####  ##  ##    ########  ##        ######    ##          ##    ##
        # -  ##    ##  ##    ##  ##  ##    ##    ##  ##        ##  ##    ##        ##      ##
        # -  ######      ######  ##    ##  ##    ##  ########  ##    ##  ########  ########
