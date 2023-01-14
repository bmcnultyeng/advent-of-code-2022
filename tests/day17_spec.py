import unittest

from src.day17 import (
    PyroFlow,
)


class DayTests(unittest.TestCase):
    def test_PyroFlow_init(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        self.assertEqual(40, len(pf_1.jets))
        pf_2 = PyroFlow("data/day17_jets_bm.txt")
        self.assertEqual(10091, len(pf_2.jets))

    def test_rock_xys(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        # put the plus shape at 3 from left side & level 30
        self.assertEqual([(4, 30), (3, 31), (4, 31), (5, 31)], pf_1.rock_xys(1, 3, 30))

    # def test_tower_xys(self):
    #     pf_1 = PyroFlow("data/day17_jets_test.txt")
    #     # # floor level, as initialized
    #     # self.assertEqual(
    #     #     {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}, pf_1.tower_xys()
    #     # )
    #     # initialize as only a floor level
    #     self.assertEqual(
    #         {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}, pf_1.tower()
    #     )

    def test_rocks_collide(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        # floor level with plus block 3 levels above
        self.assertEqual(
            False,
            pf_1.rocks_collide(pf_1.rock_xys(1, 3, 2), pf_1.tower_top),
        )
        # plus block overlapping floor level
        self.assertEqual(
            True,
            pf_1.rocks_collide(pf_1.rock_xys(1, 2, 0), pf_1.tower_top),
        )
        # plus block next level above floor level
        self.assertEqual(
            False,
            pf_1.rocks_collide(pf_1.rock_xys(1, 2, 1), pf_1.tower_top),
        )

    def test_side_collide(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        # plus block 2 from left side & 4 levels above floor (starting position)
        self.assertEqual(
            False,
            pf_1.side_collide(pf_1.rock_xys(1, 2, 4)),
        )
        # plus block overlapping left side & 3 levels above
        self.assertEqual(
            True,
            pf_1.side_collide(pf_1.rock_xys(1, -1, 3)),
        )
        # plus block overlapping right side & 3 levels above
        self.assertEqual(
            True,
            pf_1.side_collide(pf_1.rock_xys(1, 5, 3)),
        )

    def test_move_left_right(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        # plus block 2 from left side & 4 levels above floor (starting position)
        pf_1.rock = pf_1.rock_xys(1, 2, 4)
        pf_1.jet_index = 0  # test data jets[0] is ">" right
        pf_1.move_left_right()
        self.assertEqual(
            pf_1.rock_xys(1, 3, 4),
            pf_1.rock,
        )
        # plus block against left side & 3 levels above
        pf_1.rock = pf_1.rock_xys(1, 0, 3)
        pf_1.jet_index = 4  # test data jets[4] is "<" left
        pf_1.move_left_right()
        # should not move
        self.assertEqual(
            pf_1.rock_xys(1, 0, 3),
            pf_1.rock,
        )
        # add rocks along left side of tower at 5 levels
        pf_1.tower_top.update({(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)})
        # plus block against rocks on left side & 3 levels above
        pf_1.rock = pf_1.rock_xys(1, 1, 3)
        pf_1.jet_index = 4  # test data jets[4] is "<" left
        pf_1.move_left_right()
        # should not move
        self.assertEqual(
            pf_1.rock_xys(1, 1, 3),
            pf_1.rock,
        )

    def test_drop_cycle(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")
        # first block (minus shape) comes to rest on floor
        #   against right wall after 3 right jets & 3 moves down
        next_tower_top = pf_1.tower_top.union({(3, 1), (4, 1), (5, 1), (6, 1)})
        pf_1.drop_cycle()
        self.assertEqual(
            next_tower_top,
            pf_1.tower_top,
        )

    def test_adjust_tower_top_origin(self):
        pf_1 = PyroFlow("data/day17_jets_test.txt")

        # add some rocks above floor
        pf_1.tower_top.update({(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)})
        # origin should be adjusted 5 units higher
        new_tower_top = {
            (0, -5),
            (1, -5),
            (2, -5),
            (3, -5),
            (4, -5),
            (5, -5),
            (6, -5),
            (1, -4),
            (2, -3),
            (3, -2),
            (4, -1),
            (5, 0),
        }
        pf_1.adjust_tower_top_origin()
        self.assertEqual(new_tower_top, pf_1.tower_top)

        # # add some rocks over 15 above top
        pf_1.tower_top.update({(2, 13), (3, 14), (4, 15), (5, 16), (6, 17)})
        # # origin should be adjusted 17 units higher & floor should not be included
        new_tower_top = {
            # (1, -21),
            # (2, -20),
            (3, -19),
            (4, -18),
            (5, -17),
            (2, -4),
            (3, -3),
            (4, -2),
            (5, -1),
            (6, 0),
        }
        pf_1.adjust_tower_top_origin()
        self.assertEqual(new_tower_top, pf_1.tower_top)

    def test_drop_rocks(self):

        # Part 1 solution to example data
        # pf_2 = PyroFlow("data/day17_jets_test.txt", rock_count_limit=2022)
        # pf_2.drop_rocks()
        # self.assertEqual(3068, pf_2.tower_height)

        # Part 1 solution to actual data
        # TODO why much slower when rock_count_limit > 58 ??
        #      because tower_top is leakey in x=0 column!
        pf_3 = PyroFlow(
            "data/day17_jets_bm.txt", rock_count_limit=2022, max_top_levels=100
        )
        pf_3.drop_rocks()
        self.assertEqual(3186, pf_3.tower_height)

        # # note: used print_ascii() to visualize & test/debug
        # pf_1 = PyroFlow("data/day17_jets_test.txt")
        # pf_1.rock_count_limit = 1  # change this value to test/debug
        # # pf_1.rock_count_limit = 10  # change this value to test/debug
        # pf_1.drop_rocks()
        # # after one rock; minus shape resting on floor
        # new_tower_top = {
        #     (0, -1),
        #     (1, -1),
        #     (2, -1),
        #     (3, -1),
        #     (4, -1),
        #     (5, -1),
        #     (6, -1),
        #     (2, 0),
        #     (3, 0),
        #     (4, 0),
        #     (5, 0),
        # }
        # self.assertEqual(new_tower_top, pf_1.tower_top)
