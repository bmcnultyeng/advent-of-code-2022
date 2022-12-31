import unittest

from src.day12 import Grid, part2_solution


class DayTests(unittest.TestCase):
    def test_Grid(self):
        # test the basics of the class & initialized data lists
        grid_1 = Grid("data/day12_elevations_test.txt")  # test with known data_lines
        self.assertEqual(5, len(grid_1.elevations))
        self.assertEqual(1, grid_1.elevations[0][2])  # elevation 'b'
        self.assertEqual(25, grid_1.elevations[2][5])  # End location elevation 'z'
        self.assertEqual((0, 0), grid_1.start_loc)
        self.assertEqual([(0, 1), (1, 0)], grid_1.adjacencies[(0, 0)])
        self.assertEqual([(0, 4), (0, 2), (1, 3)], grid_1.adjacencies[(0, 3)])

    def test_heuristic(self):
        grid_1 = Grid("data/day12_elevations_test.txt")  # test with known data_lines
        # straight-line distance, default
        self.assertEqual(5.0, grid_1.heuristic((0, 0), (3, 4)))
        # manhattan distance
        self.assertEqual(7, grid_1.heuristic((0, 0), (3, 4), "manhattan"))

    def test_a_star(self):
        grid_1 = Grid("data/day12_elevations_test.txt")  # test with known data_lines
        self.assertEqual(31, grid_1.a_star())  # 39 iterations
        # Part 1 solution
        grid_1 = Grid("data/day12_elevations_bm.txt")
        self.assertEqual(504, grid_1.a_star(10000))  # 6437 iterations

    def test_no_path(self):
        grid_1 = Grid("data/day12_elevations_test_nopath.txt")  # all paths blocked from
        self.assertEqual(float("inf"), grid_1.a_star())  # 12 iterations

    def test_part2_solution(self):
        self.assertEqual(29, part2_solution("data/day12_elevations_test.txt"))
        self.assertEqual(
            500, part2_solution("data/day12_elevations_bm.txt")
        )  # estimate 12 million iterations ~ 6 seconds
