import unittest

from src.day04 import (
    has_contained_range,
    count_contained,
    has_overlap_range,
    count_overlap,
)


class DayTests(unittest.TestCase):
    def test_has_contained_range(self):  # Part 1
        self.assertEqual(False, has_contained_range("2-4,6-8"))  # 1st line of test data
        self.assertEqual(
            True, has_contained_range("2-8,3-7\n")
        )  # 4th line of test data
        self.assertEqual(
            True, has_contained_range("23-37,23-45\n")
        )  # try parsing double-digits

    def test_count_contained(self):
        self.assertEqual(2, count_contained("data/day04_assignments_test.txt"))
        self.assertEqual(536, count_contained("data/day04_assignments_bm.txt"))

    def test_has_overlap_range(self):  # Part 2
        self.assertEqual(False, has_overlap_range("2-4,6-8"))  # 1st line of test data
        self.assertEqual(True, has_overlap_range("6-6,4-6\n"))  # 5th line of test data
        self.assertEqual(True, has_overlap_range("10-33,30-40\n"))  # double-digits

    def test_count_overlap(self):
        self.assertEqual(4, count_overlap("data/day04_assignments_test.txt"))
        self.assertEqual(845, count_overlap("data/day04_assignments_bm.txt"))

