# Day #14: Regolith Reservoir
# Part 1: How many units of sand will stack up in the cave until
#   falling over the edge into the abyss?
# part 2: How manu units of sand can stack to the top opening
#   if there is an infinite floor 2 units below the deepest rock?


# Part 1 plan...
# 1) create a list of all rock x,y coordinates (x=right, y=down) from input data
# 2) create an adjacencies list for all possible moves through air
#      from the sand source (500,0) to the abyss (y = max rock y + 1)
#      as a dict of ordered lists [down,down-left,down-right]
# 3) simulate each falling sand unit from source until it runs out of moves or goes into abyss
#      delete the stopped sand position from the air adjacencies dict (value and it's key if empty)
#      count how many sand units dropped overall
#      this should be a recursive function (end at rock or abyss; recurse at air position, return final position)
# ?) Is there a quicker way to do this?  by tracing reverse paths from rocks to souce?

# Part 2 plan...
# - change the abyss_y from 1 to 2 below the deepest rock; use as the floor
# - modify the end condition from falling into the abyss to filling to the top
# - add a part2 flag parameter


class Cave:
    """creates map of cave cross section; simulates falling sand units"""

    def __init__(self, rocks_file, part_2=False):
        """create list of all rock positions from input data;
        create dict of all air positions and legal moves to adjacent air positions"""

        self.part2 = part_2
        self.rock_positions = set()

        # 1) create a list of all rock x,y coordinates (x=right, y=down) from input data
        with open(rocks_file, "r") as rfile:
            for line in rfile:
                if len(line.strip()) != 0:  # skip blank lines
                    corners = [eval(corner) for corner in line.split("->")]
                    self.rock_positions.update(corners)  # add corners to the set
                    for i in range(len(corners) - 1):  # add the rocks between corners
                        # handle negative direction in range between corners
                        c1, c2 = min(corners[i], corners[i + 1]), max(
                            corners[i], corners[i + 1]
                        )
                        if c1[0] == c2[0]:  # x coordinates same
                            self.rock_positions.update(
                                [(c1[0], y) for y in range(c1[1] + 1, c2[1])]
                            )
                        elif c1[1] == c2[1]:  # y coordinates same
                            self.rock_positions.update(
                                [(x, c1[1]) for x in range(c1[0] + 1, c2[0])]
                            )

        # 2) create an adjacencies list for all possible moves through air
        #      from the sand source (500,0) to the abyss (y = max rock y + 1)
        #      as a dict of ordered lists [down,down-left,down-right]
        if not self.part2:
            self.abyss_y = 1 + max(
                [y for (x, y) in self.rock_positions]
            )  # sand is spilling over edges
        else:
            self.abyss_y = 2 + max(
                [y for (x, y) in self.rock_positions]
            )  # use abyss as an infinite floor

        self.start_pos = (500, 0)  # source of sand at top of cave per problem statement
        self.air_adjacencies = (
            dict()
        )  # graph of legal moves from all air positions between start_pos and abyss_y
        # cascade of adjacent positions for all possible sand positions which are not rocks
        if not self.part2:
            y_limit = self.abyss_y  # deepest rock + 1
        else:
            y_limit = self.abyss_y + 1  # deepest rock + 2
        for i, y in enumerate(range(self.start_pos[1], y_limit)):
            # priorities of path: down, down-left, down-right
            new_air = {
                (x, y): [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
                for x in range(self.start_pos[0] - i, self.start_pos[0] + i + 1)
                if (x, y) not in self.rock_positions
            }
            # remove paths into rocks  TODO a better way, list comprehension?
            new_air_not_rocks = dict()
            for key in new_air:
                not_rocks = []
                for xy in new_air[key]:
                    if xy not in self.rock_positions:
                        not_rocks.append(xy)
                new_air_not_rocks[key] = not_rocks

            self.air_adjacencies.update(new_air_not_rocks)

        abyss_moves = [
            moves
            for key, moves in self.air_adjacencies.items()
            # if key[1] == self.abyss_y - 1
            if key[1] == y_limit - 1  # handles Part 2 floor
        ]
        # flatten a list: [element for innerList in lis for element in innerList]
        # add blocks at abyss with no moves
        self.air_adjacencies.update({pos: [] for moves in abyss_moves for pos in moves})

    def drop_sand(self, current_position):
        """follow path of one sand unit from source to resting place or into abyss"""

        if len(self.air_adjacencies[current_position]) == 0:
            # end case: sand came to rest (Part 1 & 2) or fell off edge into abyss (Part 1)
            return current_position
        # recurse case: take highest priority move
        return self.drop_sand(self.air_adjacencies[current_position][0])

    def solve_part12(self, max_drops=2000):
        """drop sand units until they fall off edge into abyss"""
        self.sand_count = 0
        sand_positions = []
        # 3) simulate each falling sand unit from source until it runs out of moves or goes into abyss
        for _ in range(max_drops):  # prevent runaway
            final_pos = self.drop_sand(self.start_pos)
            if not self.part2:
                if final_pos[1] >= self.abyss_y:
                    # Part 1 - sand fell off edge into abyss
                    return self.sand_count  # same as _ loop index
            else:
                if final_pos == self.start_pos:
                    # Part 2 - sand pile reached the top
                    self.sand_count += 1  # fill the source block with sand
                    return self.sand_count  # same as _ loop index - 1

            # sand came to rest
            self.sand_count += 1
            # save resting positions, if needed
            sand_positions.append(final_pos)
            # remove resting position from air blocks and previous paths
            del self.air_adjacencies[final_pos]
            previous_keys = [
                (final_pos[0] - 1, final_pos[1] - 1),
                (final_pos[0], final_pos[1] - 1),
                (final_pos[0] + 1, final_pos[1] - 1),
            ]
            for key in previous_keys:
                if (
                    key in self.air_adjacencies
                    and final_pos in self.air_adjacencies[key]
                ):
                    self.air_adjacencies[key].remove(final_pos)
        return f"Exceeded {max_drops}."
