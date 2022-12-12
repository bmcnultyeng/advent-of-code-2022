import unittest

from src.day09 import Rope

# TODO restore previous version of this overwritten file from repository!


class DayTests(unittest.TestCase):
    def test_Rope(self):
        # test the basics of the Rope class
        rope_1 = Rope("data/day09_motions_test.txt")  # test with known data_lines
        self.assertEqual(8, len(rope_1.moves))
        self.assertEqual(("R", 4), rope_1.moves[0])

    #     self.assertEqual([1, True, True], forest_1.trees[0][0])
    #     self.assertEqual([5, False, False], forest_1.trees[1][1])
    #     # use data from test file
    #     forest_2 = Forest("data/day08_trees_test.txt")
    #     self.assertEqual(5, forest_2.extent)
    #     self.assertEqual([3, True, True], forest_2.trees[0][0])  # upper left corner
    #     self.assertEqual([2, True, True], forest_2.trees[2][4])  # center right edge
    #     self.assertEqual([5, False, False], forest_2.trees[1][1])  # before searching
    #     forest_3 = Forest("data/day08_trees_bm.txt")
    #     self.assertEqual(99, forest_3.extent)
    #     self.assertEqual([3, True, True], forest_3.trees[0][9])  # top row
    #     self.assertEqual([4, True, True], forest_3.trees[18][98])  # right edge
    #     self.assertEqual([8, False, False], forest_3.trees[22][50])  # interior

    # def test_is_visible(self):
    #     forest_1 = Forest("data/day08_trees_test.txt")
    #     self.assertEqual(True, forest_1.is_visible(1, 1))  # the top-left 5 visible
    #     self.assertEqual(True, forest_1.is_visible(1, 2))  # the top-middle 5 visible
    #     self.assertEqual(False, forest_1.is_visible(1, 3))  # the top-right 1 hidden
    #     self.assertEqual(False, forest_1.is_visible(2, 2))  # the center 3 hidden
    #     self.assertEqual(True, forest_1.is_visible(2, 3))  # the right-middle 3 visible
    #     self.assertEqual(True, forest_1.is_visible(3, 2))  # the low-middle 5 visible

    # def test_find_visible_trees(self):
    #     forest_1 = Forest()  # test with known data_lines
    #     forest_1.build_trees_structure(
    #         [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    #     )
    #     forest_1.find_visible_trees()
    #     self.assertEqual(9, forest_1.visible_count)  # before searching/tag
    #     forest_2 = Forest("data/day08_trees_test.txt")
    #     self.assertEqual(21, forest_2.find_visible_trees())  # before searching/tag
    #     # Parrt 1 solution
    #     forest_3 = Forest("data/day08_trees_bm.txt")
    #     self.assertEqual(1849, forest_3.find_visible_trees())  # before searching/tag

    # def test_calc_scenic_score(self):
    #     forest_1 = Forest("data/day08_trees_test.txt")
    #     self.assertEqual(4, forest_1.calc_scenic_score(1, 2))  # the middle 5 in 2nd row
    #     self.assertEqual(8, forest_1.calc_scenic_score(3, 2))  # the middle 5 in 4th row

    # def test_find_highest_scenic_score(self):
    #     forest_1 = Forest("data/day08_trees_test.txt")
    #     self.assertEqual(8, forest_1.find_highest_scenic_score())
    #     # Part 2 solution
    #     forest_2 = Forest("data/day08_trees_bm.txt")
    #     self.assertEqual(201600, forest_2.find_highest_scenic_score())
