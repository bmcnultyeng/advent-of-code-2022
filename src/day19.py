# Day 19: Not Enough Minerals
# Part 1: Determine the quality level of each blueprint
#   using the largest number of geodes it could produce
#   in 24 minutes. What do you get if you add up the
#   quality level of all of the blueprints in your list?

# Part 1 plan...
# 1) read & parse blueprints from input data into a dict.
# 2) for each blueprint, try all possible combinations
#    (iterative DFS paths?) of building one or none of
#    the robots over a time span of 24 min; track the
#    geode counts at the end of every 24-min trial.
#   a) the differences between bleueprints are the costs
#      of building an ore, clay, obsidian or geode robot.
#   b) the search parameters are: for each minute, choose
#      to build one or none of the robots, if affordable
#      from counts of ore, clay & obsidian at start of minute.
# 3) determine the max geode count and quality level
#    for each blueprint; solution = sum of quality levels.


class RobotFactory:
    """Build robots to process ore, clay, obsidian & geodes,
    according to the best blueprint"""

    def __init__(self, blueprints_file):
        """read & parse blueprints into a dict"""

        self.blueprints = dict()

        with open(blueprints_file, "r") as bfile:
            for line in bfile:
                if len(line.strip()) != 0:  # skip blank lines
                    # parse blueprint index (key) & costs of ore, clay,
                    # obsidian & geode robots; cost values are tuples,
                    # i.e (2,0,3) means cost is 2 ores + 3 obsidians
                    blueprint_index = int(line[line.find(":") - 2 : line.find(":")])
                    ln = line.split()
                    ore_cost = (int(ln[6]), 0, 0)
                    clay_cost = (int(ln[12]), 0, 0)
                    obs_cost = (int(ln[18]), int(ln[21]), 0)
                    geo_cost = (int(ln[27]), 0, int(ln[30]))

                    # dict value is a list of four 3-integer tuples
                    self.blueprints[blueprint_index] = [
                        ore_cost,
                        clay_cost,
                        obs_cost,
                        geo_cost,
                    ]
                _ = "debug breakpoint"

    def max_geode_count(self, blueprint_index, max_time=24):
        """try all combinations of building robots using DFS path search;
        over 24 minutes return the highest geode count of all trials"""
        # hit: heavy branch trimming/heuristics will drastically cut run time
        # TODO good hint/code at:
        #  https://github.com/mjpieters/adventofcode/blob/master/2022/Day%2019.ipynb
        #  https://github.com/mattbillenstein/aoc/blob/main/2022/19/p.py
        #  also: if predicted max total geodes is < a total geodes already found, abandon branch
        #  also: can stop if not possible to build any more geode robots in remaining time
        #         (at each time step?!)
        #  also: track geode inventory as totals-thru-24-min; don;t need to trak geode-robot-count
        #  https://github.com/deivi-drg/advent-of-code-2022/blob/main/Day19/day19.py

        #  https://nopaste.ml/#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
        # Instead of tracking current geodes and geode robots, just track a
        # single score (each time a geode robot is created, it is known how many
        # geodes it will contribute).  Instead of directly simulating wait states,
        # the choice to visit a neighbor computes the number of cycles needed to
        # reach the chosen bot, so each _visit() can branch at most 4 times.  To
        # further prune things, note that it is not worth choosing a bot that
        # would not produce useful resources, and line up the DFS search with
        # the later bots first so that states can short-circuit if they cannot
        # possibly score better than the current max.
        # - geode: need at least one obsR
        # - obs: need at least one clayR, avoid if obsR>=cost6
        # - clay: avoid if clayR>=cost4
        # - ore: avoid if oreR>=max(cost1,cost2,cost3,cost5)
        # - score cap: assuming infinite ore and obsidian supply, skip any visit
        #   that cannot produce more geodes in time remaining than current best

        # state of each node: an 8-integer tuple of remaining_time [0],
        #   then ore, clay & obsidian robot counts [1,2,3],
        #   then inventory counts of ore, clay, obsidian [4,5,6],
        #   then ultimate production of geodes [7].
        # when a geode robot is built, no need to track geode robot count
        #   or geode inventory since geodes can not purchase anything.

        # start with 1 ore robot at 24 minutes remaining (Part 1), no inventory;
        #  [time, ore_rob, clay_rob, obs_rob, ore_inv, clay_inv, obs_inv, geo_ult]
        start_node = (max_time, 1, 0, 0, 0, 0, 0, 0)
        queue = [start_node]

        best_geode_count = 0

        # iterative DFS search...

        # DFS summary: pop current node from FIFO queue; select & prioritze adjacent nodes;
        #   add selected adjacents to queue, in reverse priority order; repeat

        # cycle for one minute, until queue is empty...
        # -pop node from the FIFO queue; it will be the latest, highest-priority choice
        # -determine which robots are affordable, based on current inventory
        # -prioritize or eliminate robot choices, based on heuristic rules
        # -update inventory with collections by existing ore, clay & obs robots
        # -decrement time remaining
        # -create nodes for robot choices, if any, with cost deducted from inventory
        #    if choice is a geode robot, update the geo-ult value instead of robot count
        # -update best_geode_count if current geo-ult is higher
        # -append/extend nodes to queue, by reverse priority; next cycle will use highest-priority choice

        # while testing code & comparing heuristics, run for only 3 to 6 minutes
        self.nodes_popped_count = 0  # for testing/debug
        while len(queue) > 0:
            # last element in the FIFO queue is the newest and highest priority node.
            # mutable state during current cycle:
            #   [time, ore_rob, clay_rob, obs_rob, ore_inv, clay_inv, obs_inv, geo_ult]
            curr_node = list(queue.pop(-1))
            self.nodes_popped_count += 1  # for testing/debug
            # check again here; best_geode_count could have increased since adding to the queue
            if self.possible_to_exceed_best_geode_count(curr_node, best_geode_count):

                # TODO prioritize or eliminate robot choices, based on heuristic rules

                # if curr_node[0] > 1:
                #     # need at least 2 minutes to build a geode robot & increase ultimate geode count

                # # affordable robot indexes:
                # robot_choices = self.affordable_robots(curr_node, blueprint_index)

                # # update inventory with production by current non-geode robots
                # for i in range(3):
                #     curr_node[i + 4] += curr_node[i + 1]

                # # decrement time remaining
                # curr_node[0] -= 1

                # TODO JUMP TIME per hint... Instead of directly simulating wait (no-build) states,
                # jump to the next "built state": when each robot is affordable, then built,
                # using only the existing robots;
                # jump time = minimum production time + 1 min to build;
                # for obs & geo robots, one of two minerals will determine production time,
                # so there might be excessive-looking inventory of the non-limiting mineral;
                # except for building a geode robot, inventory increases by robot count * jump time,
                # less cost to build & robot count increases one for the built robot,
                #
                new_nodes = []
                for bot_index, bot_cost in enumerate(self.blueprints[blueprint_index]):
                    minerals_needed = [
                        cost - curr_node[i + 4] for i, cost in enumerate(bot_cost)
                    ]
                    # necessary robots available?
                    # none, one or two minerals may be needed
                    if all(
                        [
                            curr_node[i + 1] > 0
                            for i, need in enumerate(minerals_needed)
                            if need > 0
                        ]
                    ):

                        # time needed for existing robots to produce a needed mineral, if any,
                        # using integer division, rounded up
                        production_minutes = [0]
                        production_minutes.extend(
                            [
                                -(-need // curr_node[i + 1])
                                for i, need in enumerate(minerals_needed)
                                if need > 0
                            ]
                        )
                        # add one minute to build the robot, until it becomes productive
                        time_jump = 1 + max(production_minutes)

                        if time_jump < curr_node[0]:
                            # create a new node at the built time
                            new = curr_node.copy()
                            # decrement time
                            new[0] -= time_jump
                            # deduct robot cost from inventory
                            for i in range(3):
                                new[i + 4] -= self.blueprints[blueprint_index][
                                    bot_index
                                ][i]
                            # add production from existing non-geode robots
                            for i in range(3):
                                new[i + 4] += new[i + 1] * time_jump
                            if bot_index <= 2:
                                # build an ore, clay or obsidian robot
                                # add new robot to the count
                                new[bot_index + 1] += 1
                            else:
                                # build a geode robot
                                # add ultimate geode production
                                new[7] = new[0] - 1
                                # update best_geode_count if current geo-ult is higher
                                best_geode_count = max(best_geode_count, new[7])
                            if self.possible_to_exceed_best_geode_count(
                                new, best_geode_count
                            ):
                                new_nodes.append(tuple(new))

                # ......refactoring above..............................................
                #     # use existing robots only
                #     if curr_node[bot_index] > 0:

                #         new = curr_node.copy()
                #         new[0] = curr_node[0] + time_jump
                #         if bot_index <= 2:
                #             new[bot_index + 1] += 1

                # # add 'no-build' node to queue as lowest priority [? only if no choice to build a robot]
                # if self.possible_to_exceed_best_geode_count(curr_node, best_geode_count):
                #     queue.append(tuple(curr_node))
                # new_nodes = []
                # for r in robot_choices:
                #     new = curr_node.copy()
                #     if r <= 2:
                #         new[r + 1] += 1  # add to robot count
                #         for i in range(3):
                #             new[i + 4] -= self.blueprints[blueprint_index][r][
                #                 i
                #             ]  # spend inventory
                #     else:
                #         new[7] = new[0] - 1  # ultimate geode count
                #         # update best_geode_count if current geo-ult is higher
                #         best_geode_count = max(best_geode_count, new[7])
                #     if self.possible_to_exceed_best_geode_count(new, best_geode_count):
                #         new_nodes.append(tuple(new))

                # append 'build' nodes to queue, by reverse priority
                # TODO order new_nodes by lower-to-higher priority
                #   -already ordered by newly built robot type
                queue.extend(new_nodes)

        return best_geode_count

    def possible_to_exceed_best_geode_count(self, node, best_geode_count):
        #   -do not add this node, if impossible to exceed best_geode_count with
        #     unlimited resources & Time Remaining: addl geodes = (TR-1) * (TR/2)
        max_additional_geodes = (node[0] - 1) * (node[0] / 2)
        return max_additional_geodes + node[7] > best_geode_count

    def quality_level(self, max_time=24):
        q_level = 0
        for i in range(1, len(self.blueprints + 1)):
            q_level += i * self.max_geode_count(i, max_time)
        return q_level

    def affordable_robots(self, node, blueprint_index):
        """determine which robots can be built, using current inventory"""
        # [ore_rob, clay_rob, obs_rob, geo_rob]
        robots = []
        for r in range(4):
            if (
                node[4] >= self.blueprints[blueprint_index][r][0]
                and node[5] >= self.blueprints[blueprint_index][r][1]
                and node[6] >= self.blueprints[blueprint_index][r][2]
            ):
                robots.append(r)
        return robots


# robot_choices = [node[i+4] >= self.blueprints[blueprint_index][i] for i in range(4)]
