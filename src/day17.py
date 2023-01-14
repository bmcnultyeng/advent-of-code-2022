# Day 17: Pyroclastic Flow

# plan for Part 1 & 2...
# 1) create a basic simulation for Part 1 and solve for the actual input
#      create a True/False 7-wide grid for the map of the tall narrow chamber
#      create functions for the jet directions and rock shapes (lists of xy coordinates)
# 2) create the pattern dict lookup; test on the known Part 1 solution
#      pattern is a combo of rock index, jet index & map of the top 20+ rows with rocks
# 3) apply the modified code to Part 2 (just an increased number of drops)

# description of a cycle:
#   place the next rock at the starting position, [check for an existing pattern,]
#   push rock with gas jet (checking for a collision with tower or walls),
#   drop down one position, end cycle if a tower collision (rock comes to rest),
#   repeat jet & drop moves until rock comes to rest on tower or floor


class PyroFlow:
    """How tall do falling rocks stack in a narrow chamber?"""

    def __init__(self, jets_file, rock_count_limit=2022, max_top_levels=20):
        """get jet-flow string from input data;
        initialize rock shapes & tower of rocks"""

        with open(jets_file, "r") as jfile:
            for line in jfile:
                # only one long line
                if len(line.strip()) != 0:  # skip blank lines
                    # self.jets = line.strip()
                    self.jets = list(line.strip())  # faster as a list of char?

        self.rock_count_limit = rock_count_limit
        self.max_top_levels = max_top_levels

        # initialize the tower as a solid floor
        # top 20 (default) levels of rocks, for patterns;
        # had to increase to 100 for actual data
        self.tower_top = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}
        self.tower_height = 0  # height of all rocks from floor to top occupied level
        self.rock_count = 0
        self.rock_index = -1
        self.jet_index = -1

        # rock shapes: a list of sublists of x,y (+right,+up) coordinates;
        # origin at the lower right corner;
        # in the order as dropped:   -  +  L  |  =
        # values ordered as: min-x, max-x, ..., max-y
        self.rock_shapes = [
            [(0, 0), (3, 0), (1, 0), (2, 0)],
            [(0, 1), (2, 1), (1, 0), (1, 1), (1, 2)],
            [(0, 0), (2, 0), (1, 0), (2, 1), (2, 2)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
        ]

    def adjust_tower_top_origin(self):
        """shift origin to top of rocks; remove rocks more than 20 (default) deep"""
        # y_adjust = max([y for x, y in self.tower_top])
        y_adjust = self.rock[-1][1]  # max y in last xy pair
        if y_adjust > 0:
            self.tower_top = {
                (x, y - y_adjust)
                for x, y in self.tower_top
                if y > -self.max_top_levels + y_adjust
            }
            self.tower_height += y_adjust
        return

    def rock_xys(self, rock_index, x_offset=2, y_offset=4):
        """returns the true x,y coordinates, offset on the level provided"""
        # start at 2 from left wall & 4 above top of rocks or floor
        position = []
        for xy in self.rock_shapes[rock_index]:
            position.append((xy[0] + x_offset, xy[1] + y_offset))
        return position

    def drop_rocks(self):
        """drop rocks; check for previous states; move rock; check for collisions"""

        # dictionary of hashes at start of the cycle, before rock starts moving
        self.previous_states = dict()
        self.jumped_ahead = False

        while self.rock_count < self.rock_count_limit:  # drop a new rock
            if self.rock_index < 4:
                self.rock_index += 1
            else:
                self.rock_index = 0
            self.rock = self.rock_xys(self.rock_index)  # at starting position

            self.rock_count += 1

            if not self.jumped_ahead:
                self.pattern_jump()

            while True:  # continue moving this rock
                # self.make_ascii_map(False)  # monitor self.ascii_map in debug pane
                if self.jet_index < len(self.jets) - 1:
                    self.jet_index += 1
                else:
                    self.jet_index = 0
                self.move_left_right()

                if not self.move_down():  # came to rest on tower
                    self.tower_top.update(self.rock)
                    self.adjust_tower_top_origin()
                    break  # end of cycle for this rock
                # else continue with movements
        return

    def pattern_jump(self):
        # before any moves, check for a previously executed state;
        #   a) if none, save hash of starting state, rock count & overall height; or
        #   b) if a match, advance rock count & overall height as near as possible
        #      to max rock count; then revert to single drop cycles without pattern checks

        #    the hashable key is a tuple of:
        #       rock-index, jet-index, list(self.tower_top).sorted()
        #    the values are:
        #    [0] rock count at start of this cycle
        #    [1] overall height of tower at start of this cycle.
        if self.tower_height >= self.max_top_levels:
            starting_hash = hash(
                (
                    self.rock_index,
                    self.jet_index,
                    tuple(sorted(list(self.tower_top))),
                )
            )

            if starting_hash not in self.previous_states:
                # save current state
                self.previous_states[starting_hash] = [
                    self.rock_count,
                    self.tower_height,
                ]
            else:
                # advance rock count & tower height as close as possible to rock_count_limit
                rock_count_delta = (
                    self.rock_count - self.previous_states[starting_hash][0]
                )
                tower_height_delta = (
                    self.tower_height - self.previous_states[starting_hash][1]
                )
                number_of_jumps = (
                    self.rock_count_limit - self.rock_count
                ) // rock_count_delta
                self.rock_count += number_of_jumps * rock_count_delta
                self.tower_height += number_of_jumps * tower_height_delta
                # need a flag to do this only once
                self.jumped_ahead = True

    def move_left_right(self):
        """jet moves rock unless it collides with wall"""
        if self.jets[self.jet_index] == ">":  # move 1 right
            next_pos = [(x + 1, y) for x, y in self.rock]
        else:  # move 1 left
            next_pos = [(x - 1, y) for x, y in self.rock]
        if self.rocks_collide(next_pos) or self.side_collide(next_pos):
            return
        self.rock = next_pos.copy()  # no collisions

    def move_down(self):
        """rock drops one unit unless it collides with tower of existing rocks"""
        next_pos = [(x, y - 1) for x, y in self.rock]
        if self.rocks_collide(next_pos):
            return False  # rock can no longer move down
        self.rock = next_pos.copy()  # no collisions
        return True

    def rocks_collide(self, rock_pos):
        """if any rock coordinates overlap with the resting tower of rocks"""
        # top of tower at y=0
        for xy in rock_pos:
            if xy in self.tower_top:
                return True
        return False

    def side_collide(self, rock_pos):
        """if any rock coordinates overlap with the sides of the 7-wide chamber"""
        # walls at x=-1 and x=7
        # for xy in rock_pos:
        #     if xy[0] == -1 or xy[0] == 7:
        #         return True

        # 1st xy value has min-x; 2nd has max-x
        if rock_pos[0][0] == -1 or rock_pos[1][0] == 7:
            return True
        return False

    def make_ascii_map(self, print_it=False):
        """simple text visualization of tower_top"""
        max_print_depth = 20  # change this to look deeper into tower of rocks
        # watch for indexes out of range
        width = 7
        height = 8 + max_print_depth
        # normalize with origin at row 9 from top
        text_map = [["." for x in range(width)] for row in range(height)]
        for (x, y) in self.tower_top:
            if y > -max_print_depth:
                text_map[y + max_print_depth - 1][x] = "#"
        if self.rock:
            for (x, y) in self.rock:
                if y > -max_print_depth:
                    text_map[y + max_print_depth - 1][x] = "@"
        text_block = ""
        self.ascii_map = []
        for row in reversed(text_map):
            self.ascii_map.append("".join(row))
            text_block = text_block + "".join(row) + "\n"
        if print_it:
            print(self.text_block)


# best hint from reddit ...
# https://www.reddit.com/r/adventofcode/comments/znykq2/2022_day_17_solutions/
# spartanrickk     17 days ago     C++
# Lagging a few days behind, but I thought let's post anyway. Both part 1
# and part 2 are solved in a single script. This code runs in about 5ms
# when built in Release mode. Getting part 1 right took quite some time,
# I had a lot of nasty off-by-one errors. What helped eventually was to
# print out the "debug messages" that were also shown in the example
# (e.g. "jet pushes rock to the left, but nothing happens").
# I left the these messages in the script, uncomment if you want to
# see them. I didn't use fancy bitwise operations for moving the blocks
# left/right, or for collision detection, I might update that in the future.

# For part 2, I eventually settled for "hashing" the game state
# (current wind direction + current shape + top 20 rows), and looking
# if this combination was encountered before. Then from that the height
# of the stack after 1 trillion blocks have dropped is calculated.
# This works for my input, but I can imagine some pathological inputs
# where 20 rows is not sufficient. In that case, bump the number to
# 100, 1000, 10.000, whatever. I am sure there are smarter solutions,
# or at least better hashing functions, but this works good enough :)
#
