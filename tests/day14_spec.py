import unittest

from src.day14 import (
    Cave,
)


class DayTests(unittest.TestCase):
    def test_cave_init(self):
        cave_1 = Cave("data/day14_rocks_test.txt")
        self.assertEqual(True, (498, 4) in cave_1.rock_positions)
        self.assertEqual(True, (498, 5) in cave_1.rock_positions)
        self.assertEqual(True, (502, 9) in cave_1.rock_positions)
        self.assertEqual(True, (499, 9) in cave_1.rock_positions)
        self.assertEqual(
            True, (501, 6) in cave_1.air_adjacencies[(501, 5)]
        )  # path into air
        self.assertEqual(
            False, (501, 8) in cave_1.air_adjacencies[(501, 5)]
        )  # path into rock
        # Part 1 abyss block
        self.assertEqual([], cave_1.air_adjacencies[(503, 10)])
        # Part 2 floor block
        cave_2 = Cave("data/day14_rocks_test.txt", part_2=True)
        self.assertEqual([], cave_2.air_adjacencies[(503, 11)])

    def test_drop_sand(self):
        cave_1 = Cave("data/day14_rocks_test.txt")
        self.assertEqual((500, 8), cave_1.drop_sand((500, 0)))

    def test_solve_part12(self):
        # cave_1 = Cave("data/day14_rocks_test.txt")
        # self.assertEqual(24, cave_1.solve_part12())
        # # Part 1 solution
        # cave_2 = Cave("data/day14_rocks_bm.txt")
        # self.assertEqual(763, cave_2.solve_part12())

        # Part 2
        cave_3 = Cave("data/day14_rocks_test.txt", part_2=True)
        self.assertEqual(93, cave_3.solve_part12())
        # Part 2 solution
        # cave_4 = Cave("data/day14_rocks_bm.txt")
        # self.assertEqual(999, cave_4.solve_part12(part2=True))
