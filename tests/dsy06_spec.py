import unittest

from src.day06 import find_unique_sequence, process_buffers


class DayTests(unittest.TestCase):
    def test_find_unique_sequence(self):
        self.assertEqual(
            7,
            # find_unique_sequence("aabbabcd"),
            find_unique_sequence(
                "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
                char=4,  # Part 1: 4 distinct characters
            ),
        )  # 1st line of test data
        self.assertEqual(
            19,
            # find_unique_sequence("aabbabcd"),
            find_unique_sequence(
                "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
                char=14,  # Part 2: 14 distinct characters
            ),
        )  # 1st line of test data

    def test_process_buffers(self):
        # Part 1: 4 distinct characters
        self.assertEqual(
            [7, 5, 6, 10, 11],
            process_buffers("data/day06_buffer_test.txt"),
        )
        self.assertEqual(
            [1480],
            process_buffers("data/day06_buffer_bm.txt"),
        )
        # Part 2: 14 distinct characters
        self.assertEqual(
            [19, 23, 23, 29, 26],
            process_buffers("data/day06_buffer_test.txt", char=14),
        )
        self.assertEqual(
            [2746],
            process_buffers("data/day06_buffer_bm.txt", char=14),
        )
