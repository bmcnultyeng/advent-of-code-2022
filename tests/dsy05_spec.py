import unittest

from src.day05 import parse_stacks, move_crates, organize_stacks


class DayTests(unittest.TestCase):
    def test_parse_stacks(self):  # Part 1
        # self.assertEqual(
        #     3,
        #     len(
        #         parse_stacks(
        #             ["    [D]    \r", "[N] [C]    \r", "[Z] [M] [P]\r", " 1   2   3 \r"]
        #         ),
        #     ),
        # )  # 1st 4 lines of test data
        self.assertEqual(
            ([["Z", "N"], ["M", "C", "D"], ["P"]], 4),
            parse_stacks(
                ["    [D]    \r", "[N] [C]    \r", "[Z] [M] [P]\r", " 1   2   3 \r"]
            ),
        )  # 1st 4 lines of test data

    def test_move_crates(self):
        self.assertEqual(
            ([[1, 2, 3, 12], [10, 11], [20, 21, 22]]),
            move_crates([[1, 2, 3], [10, 11, 12], [20, 21, 22]], "move 1 from 2 to 1"),
        )
        self.assertEqual(
            [[1], [10, 11, 12], [20, 21, 22, 3, 2]],
            move_crates([[1, 2, 3], [10, 11, 12], [20, 21, 22]], "move 2 from 1 to 3"),
        )
        self.assertEqual(
            [[1], [10, 11, 12], [20, 21, 22, 2, 3]],
            move_crates(
                [[1, 2, 3], [10, 11, 12], [20, 21, 22]],
                "move 2 from 1 to 3",
                move_multiple_crates=True,
            ),
        )  # Part 2

    def test_organize_stacks(self):
        # Part 1
        self.assertEqual("CMZ", organize_stacks("data/day05_crates_test.txt"))
        self.assertEqual("VQZNJMWTR", organize_stacks("data/day05_crates_bm.txt"))
        # Part 2
        self.assertEqual(
            "MCD",
            organize_stacks("data/day05_crates_test.txt", move_multiple_crates=True),
        )
        self.assertEqual(
            "NLCDCLVMQ",
            organize_stacks("data/day05_crates_bm.txt", move_multiple_crates=True),
        )
