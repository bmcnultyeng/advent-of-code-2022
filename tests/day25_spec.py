import unittest

from src.day25 import (
    SnafuNumber,
    get_input,
    sum_part1,
    day25,
    day25_deconstructed,
)


class DayTests(unittest.TestCase):
    def test_add(self):
        sn_1 = SnafuNumber("1")
        self.assertEqual("2", sn_1 + "1")
        self.assertEqual("-", sn_1 + "=")
        sn_2 = SnafuNumber("2")
        self.assertEqual("1-", sn_2 + "2")
        self.assertEqual("0", sn_2 + "=")
        sn_11 = SnafuNumber("11")
        self.assertEqual("22", sn_11 + "11")
        self.assertEqual("21", sn_11 + "10")
        sn_212 = SnafuNumber("212")
        self.assertEqual("10--", sn_212 + "222")
        self.assertEqual("1=-2", sn_212 + "1=0")
        # debug/refactor to handle a second carry
        sn_big = SnafuNumber("1-12-11012=-1--2-")
        self.assertEqual("1-2=01-0---211-22", sn_big + "110=-222=0201=")

    def test_get_input(self):
        s_list_1 = get_input("data/day25_snafu_test.txt")
        self.assertEqual(13, len(s_list_1))
        self.assertEqual("122", s_list_1[12])
        s_list_2 = get_input("data/day25_snafu_bm.txt")
        self.assertEqual(114, len(s_list_2))
        self.assertEqual("1=20101-==1", s_list_2[113])

    def test_sum_part1(self):
        s_list_1 = ["212", "222", "1=0"]
        self.assertEqual("102-", sum_part1(s_list_1))
        s_list_2 = get_input("data/day25_snafu_test.txt")
        self.assertEqual("2=-1=0", sum_part1(s_list_2))
        # an incorrect Part 1 solution !
        s_list_3 = get_input("data/day25_snafu_bm.txt")
        self.assertEqual("2=01201==-2-=2-00022", sum_part1(s_list_3))

    def test_day25_by_hugues_hoppe(self):
        with open("data/day25_snafu_test.txt", "r") as s_file:
            s = s_file.read()
        self.assertEqual("2=-1=0", day25(s))
        # the correct Part 1 solution !
        with open("data/day25_snafu_bm.txt", "r") as s_file:
            s = s_file.read()
        self.assertEqual("2-0=11=-0-2-1==1=-22", day25(s))

    def test_day25_deconstructed(self):
        total_1 = day25_deconstructed("data/day25_snafu_test.txt")
        self.assertEqual("2=-1=0", total_1)
        # correct part 1 solution
        total_2 = day25_deconstructed("data/day25_snafu_bm.txt")
        self.assertEqual("2-0=11=-0-2-1==1=-22", total_2)

    def test_compare_day25_solutions(self):
        snafu_filename = "data/day25_snafu_bm.txt"
        s_list = get_input(snafu_filename)
        my_solution = sum_part1(s_list)
        hh_solution = day25_deconstructed(snafu_filename)
        self.assertEqual(my_solution, hh_solution)
