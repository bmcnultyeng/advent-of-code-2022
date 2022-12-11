import unittest

from src.day07 import update_path_sizes, process_commands


class DayTests(unittest.TestCase):
    def test_update_path_sizes(self):
        self.assertEqual(
            {("/",): 1250, ("/", "a"): 950, ("/", "a", "ab"): 300},
            update_path_sizes(
                ["/", "a"], {("/",): 1200, ("/", "a"): 900, ("/", "a", "ab"): 300}, 50
            ),
        )

    #     self.assertEqual(
    #         19,
    #         # find_unique_sequence("aabbabcd"),
    #         find_unique_sequence(
    #             "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    #             char=14,  # Part 2: 14 distinct characters
    #         ),
    #     )  # 1st line of test data

    def test_process_commands(self):
        # Part 1: total sizes <= 100,000
        self.assertEqual(
            95437,
            process_commands("data/day07_output_test.txt"),
        )
        self.assertEqual(
            1581595,
            process_commands("data/day07_output_bm.txt"),
        )
        # Part 2: min size for 30,000,000 unused space
        self.assertEqual(
            24933642,
            process_commands("data/day07_output_test.txt", part2=True),
        )
        self.assertEqual(
            1544176,
            process_commands("data/day07_output_bm.txt", part2=True),
        )
