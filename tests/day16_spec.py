import unittest

from src.day16 import (
    ValveGroup,
)


class DayTests(unittest.TestCase):
    def test_ValveGroup_init(self):
        vg_1 = ValveGroup("data/day16_valves_test.txt")
        self.assertEqual([0, ["DD", "II", "BB"]], vg_1.valves_input["AA"])
        self.assertEqual([21, ["II"]], vg_1.valves_input["JJ"])
        self.assertEqual(
            [0, {"BB": 1, "CC": 2, "DD": 1, "EE": 2, "HH": 5, "JJ": 2}],
            vg_1.valves_nz["AA"],
        )
        self.assertEqual(
            [21, {"BB": 3, "CC": 4, "DD": 3, "EE": 4, "HH": 7}], vg_1.valves_nz["JJ"]
        )

    def test_distances_to_other_nz_nodes(self):
        vg_1 = ValveGroup("data/day16_valves_test.txt")
        self.assertEqual(
            {"BB": 1, "CC": 2, "DD": 1, "EE": 2, "HH": 5, "JJ": 2},
            vg_1.distances_to_other_nz_nodes("AA"),
        )
        self.assertEqual(
            {"BB": 2, "CC": 1, "EE": 1, "HH": 4, "JJ": 3},
            vg_1.distances_to_other_nz_nodes("DD"),
        )

    def test_pressure_relief(self):
        vg_1 = ValveGroup("data/day16_valves_test.txt")
        # DD valve; distance 1; flow rate 20; 20 * (30-1-1) = 560
        self.assertEqual(560, vg_1.pressure_relief(["DD"]))
        # open HH then BB; 22 * (30-5-1) + 13 * (30-5-1-6-1) = 528 + 221 = 749
        self.assertEqual(749, vg_1.pressure_relief(["HH", "BB"]))
        # valve order solution per A0C instructions
        self.assertEqual(
            1651, vg_1.pressure_relief(["DD", "BB", "JJ", "HH", "EE", "CC"])
        )

    def test_solve_part1(self):
        vg_1 = ValveGroup("data/day16_valves_test.txt")
        self.assertEqual(
            (1651, ("DD", "BB", "JJ", "HH", "EE", "CC")), vg_1.solve_part1()
        )
        # Part 1 solution
        vg_2 = ValveGroup("data/day16_valves_bm.txt")
        # limited length of permutations to 8 of 14 nz valves, by trial-and-error
        self.assertEqual(
            (1775, ("EA", "QN", "GW", "KB", "NA", "XX", "UD", "YD")),
            vg_2.solve_part1(max_valves=8),
        )

    def test_solve_part2(self):
        vg_1 = ValveGroup("data/day16_valves_test.txt")
        self.assertEqual(
            (1707, ("DD", "HH", "EE", "JJ", "BB", "CC")),
            vg_1.solve_part2(split_valves=3),
        )
        vg_2 = ValveGroup("data/day16_valves_bm.txt")
        self.assertEqual(
            (888, ("yy", "zz")),
            vg_2.solve_part2(split_valves=7),
        )
