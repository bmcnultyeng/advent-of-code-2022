import unittest

from src.day12_recursive_incorrect import Grid


class DayTests(unittest.TestCase):
    def test_Grid(self):
        # test the basics of the class & initialized data lists
        grid_1 = Grid("data/day12_elevations_test.txt")  # test with known data_lines
        self.assertEqual(5, len(grid_1.elevations))
        self.assertEqual(1, grid_1.elevations[0][2])  # elevation 'b'
        self.assertEqual(25, grid_1.elevations[2][5])  # End location elevation 'z'
        self.assertEqual((0, 0), grid_1.start_loc)

    def test_explore_path(self):
        grid_1 = Grid("data/day12_elevations_test.txt")
        grid_1.explore_path(grid_1.start_loc)
        self.assertEqual(31, grid_1.best_step_count)

    # def test_blocked(self):
    #     grid_1 = Grid("data/day12_elevations_test.txt")
    #     self.assertEqual(
    #         "", grid_1.blocked((0, 0), (0, 1))
    #     )  # "" will evaluate as False
    #     if grid_1.blocked((0, 0), (0, 1)):  # "" will evaluate as False
    #         blocked_boolean = True
    #     else:
    #         blocked_boolean = False
    #     self.assertEqual(False, blocked_boolean)
    #     self.assertEqual("outside grid", grid_1.blocked((0, 0), (-1, 1)))
    #     self.assertEqual("too high", grid_1.blocked((0, 2), (0, 3)))
    #     if grid_1.blocked((0, 2), (0, 3)):  # "too high" will evaluate as True
    #         blocked_boolean = True
    #     else:
    #         blocked_boolean = False
    #     self.assertEqual(True, blocked_boolean)
