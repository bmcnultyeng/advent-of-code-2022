import unittest

from src.day19 import (
    RobotFactory,
)


class DayTests(unittest.TestCase):
    def test_RobotFactory_init(self):
        rf_1 = RobotFactory("data/day19_blueprints_test.txt")
        self.assertEqual(2, len(rf_1.blueprints))
        self.assertEqual((4, 0, 0), rf_1.blueprints[1][0])
        self.assertEqual((3, 0, 12), rf_1.blueprints[2][3])

    def test_max_geode_count(self):
        rf_1 = RobotFactory("data/day19_blueprints_test.txt")
        # TODO debug with more max_time
        self.assertEqual(0, rf_1.max_geode_count(blueprint_index=1, max_time=15))
        # self.assertEqual(9, rf_1.max_geode_count(blueprint_index=1, max_time=24))
        # self.assertEqual(12, rf_1.max_geode_count(blueprint_index=2, max_time=24))

    def test_affordable_robots(self):
        rf_1 = RobotFactory("data/day19_blueprints_test.txt")
        # [time, ore_rob, clay_rob, obs_rob, ore_inv, clay_inv, obs_inv, geo_ult]
        node = (24, 1, 0, 0, 6, 0, 0, 0)
        # [ore_rob, clay_rob, obs_rob, geo_rob]
        self.assertEqual(
            [True, True, False, False],
            rf_1.affordable_robots(node, blueprint_index=1),
        )
        node = (24, 1, 0, 0, 8, 14, 10, 0)
        self.assertEqual(
            [True, True, True, True],
            rf_1.affordable_robots(node, blueprint_index=1),
        )
        node = (24, 1, 0, 0, 4, 10, 0, 0)
        self.assertEqual(
            [True, True, True, False],
            rf_1.affordable_robots(node, blueprint_index=2),
        )

    def test_quality_level(self):
        rf_1 = RobotFactory("data/day19_blueprints_test.txt")
        self.assertEqual(33, rf_1.quality_level(max_time=24))
