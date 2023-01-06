import unittest

from src.day15 import (
    SensorGroup,
)


class DayTests(unittest.TestCase):
    def test_SensorGroup_init(self):
        sg_1 = SensorGroup("data/day15_sensors_test.txt", line_y=10)
        self.assertEqual(
            (-2, 15), sg_1.sensors[(2, 18)][0]
        )  # first beacon x,y position
        self.assertEqual(7, sg_1.sensors[(2, 18)][1])  # m_distance to beacon
        self.assertEqual((15, 3), sg_1.sensors[(20, 1)][0])  # last beacon x,y position

    def test_overlap_x_range(self):
        sg_1 = SensorGroup("data/day15_sensors_test.txt", line_y=10)
        self.assertIsNone(sg_1.overlap_x_range((2, 18)))
        self.assertEqual((2, 14), sg_1.overlap_x_range((8, 7)))

    def test_merge_intervals(self):
        sg_1 = SensorGroup("data/day15_sensors_test.txt", line_y=10)
        self.assertEqual(
            [[2, 10], [15, 18]],
            sg_1.merge_intervals([[3, 9], [2, 6], [8, 10], [15, 18]]),
        )
        self.assertEqual(
            [[-2, 24]],
            sg_1.merge_intervals(
                [[12, 12], [2, 14], [2, 2], [-2, 2], [16, 24], [14, 18]]
            ),
        )

    def test_solve_part1(self):
        sg_1 = SensorGroup("data/day15_sensors_test.txt", line_y=10)
        self.assertEqual(26, sg_1.solve_part1())
        # Part 1 solution
        sg_2 = SensorGroup("data/day15_sensors_bm.txt", line_y=2000000)
        self.assertEqual(5112034, sg_2.solve_part1())

    def test_solve_part2(self):
        sg_1 = SensorGroup("data/day15_sensors_test.txt")
        self.assertEqual((14, 11, 56000011), sg_1.solve_part2(max_xy=20))
        # Part 2 solution: x 3_293_021, y 3_230_812, tf 13_172_087_230_812)
        sg_2 = SensorGroup(
            "data/day15_sensors_bm.txt",
        )
        self.assertEqual(
            (3293021, 3230812, 13172087230812), sg_2.solve_part2(max_xy=4_000_000)
        )
