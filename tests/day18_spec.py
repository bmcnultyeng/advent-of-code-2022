import unittest

from src.day18 import (
    LavaDroplet,
)


class DayTests(unittest.TestCase):
    def test_LavaDroplet_init(self):

        ld_1 = LavaDroplet("data/day18_lava_test.txt")
        self.assertEqual(13, len(ld_1.cubes))
        self.assertTrue((2, 3, 2) in ld_1.adjacencies[(2, 2, 2)])
        self.assertFalse((2, 1, 5) in ld_1.adjacencies[(2, 3, 5)])
        self.assertEqual(64, ld_1.total_surface_area)

        ld_2 = LavaDroplet("data/day18_lava_bm.txt")
        self.assertEqual(2834, len(ld_2.cubes))
        # Part 1 solution
        self.assertEqual(4310, ld_2.total_surface_area)

    def test_external_surface_area(self):

        ld_1 = LavaDroplet("data/day18_lava_test.txt")
        ld_1.external_surface_area(1, 6)  # example data min=1, max=6
        # volume of air envelope 8x8x8=512 cubes,
        #   less 13 solid cubes = 499 air cubes
        self.assertEqual(499, len(ld_1.air_cubes))
        self.assertEqual(58, ld_1.external_surface_area())
        # Part 2 solution
        ld_2 = LavaDroplet("data/day18_lava_bm.txt")
        self.assertEqual(2466, ld_2.external_surface_area())
