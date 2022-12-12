# Day #9: Rope Bridge

# Part 1: simulate the movements of the tail of a rope;
#   how many positions does the tail visit at least once;
#   the tail knot follows the head knot, to maintain touching the head (within one 'Plank' distance unit)
# Part 2: there are 8 additional knots between the head and the tail,
#   following the previous knot in the same way

# read all lines of data (head movements) as a nested list of string-integer pairs (direction, steps)
# simulate the movements on a 2-D cartesian coordinate system
#   remember the positions visited by the tail as a set of x,y pairs)
#   create a single-use Rope calss to handle movements, positions and distances
#   create a method the calculate the 'Plank distance' & direction from tail to head
# the solutions to Parts 1 & 2 are a count of positions the tail visited at least once


class Rope:
    # handles movement and positions of the rope's head and tail
    def __init__(self, motions_file=""):
        # read & parse all lines of data file (movements of rope's head) as of tuples
        # initial positions at origin on xy grid (right +x, up +y)

        self.head_pos = [0, 0]
        # Part 1: only 2 knots, head & tail
        self.tail_pos = [0, 0]
        self.unique_tail_positions = {(0, 0)}
        # Part 2: positions of the head, 8 middle knots & tail
        self.knot_pos = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ]

        # parse & process each command line
        self.moves = []
        if len(motions_file) != 0:
            # read & parse all lines of input file
            with open(motions_file, "r") as mfile:
                for line in mfile:
                    if len(self.moves) == 0:
                        self.moves = [(line[0], int(line[2:]))]
                    else:
                        if len(line.strip()) != 0:
                            self.moves.append((line[0], int(line[2:])))
        else:  # for debug using dummy data_lines
            pass
        return

    def sign(self, number):
        if number == 0:
            return 0
        elif number < 0:
            return -1
        else:
            return 1

    def move_head(self, direction):
        # move head one unit
        match direction:
            case "R":
                self.head_pos[0] += 1  # move right +1 x
            case "L":
                self.head_pos[0] -= 1  # move left -1 x
            case "U":
                self.head_pos[1] += 1  # move up +1 y
            case "D":
                self.head_pos[1] -= 1  # move down -1 y
        return

    def adjust_tail(self):
        # move the tail one unit to restore the tail touching the head, if needed
        # 'touching' means adjacent (any direction incl diagonal) or overlapping
        x_distance = self.head_pos[0] - self.tail_pos[0]  # will be -2, -1, 0, +1 or +2
        y_distance = self.head_pos[1] - self.tail_pos[1]  # will be -2, -1, 0, +1 or +2
        if not (
            abs(x_distance) <= 1 and abs(y_distance) <= 1
        ):  # head & tail are touching
            if y_distance == 0:
                self.tail_pos[0] += self.sign(x_distance)  # move left or right
            elif x_distance == 0:
                self.tail_pos[1] += self.sign(y_distance)  # move up or down
            else:  # move diagonally
                self.tail_pos[0] += self.sign(x_distance)
                self.tail_pos[1] += self.sign(y_distance)
            self.unique_tail_positions.add((self.tail_pos[0], self.tail_pos[1]))
        return

    def adjust_knot(self, knot_num):
        # added for Part 2 to include 8 additional knots and the tail
        # adapted from adjust_tail(())
        x_distance = (
            self.knot_pos[knot_num - 1][0] - self.knot_pos[knot_num][0]
        )  # will be -2, -1, 0, +1 or +2
        y_distance = (
            self.knot_pos[knot_num - 1][1] - self.knot_pos[knot_num][1]
        )  # will be -2, -1, 0, +1 or +2
        if not (
            abs(x_distance) <= 1 and abs(y_distance) <= 1
        ):  # knots are touching, no move needed
            if y_distance == 0:
                self.knot_pos[knot_num][0] += self.sign(
                    x_distance
                )  # move left or right
            elif x_distance == 0:
                self.knot_pos[knot_num][1] += self.sign(y_distance)  # move up or down
            else:  # move diagonally
                self.knot_pos[knot_num][0] += self.sign(x_distance)
                self.knot_pos[knot_num][1] += self.sign(y_distance)
            if knot_num == 9:
                self.unique_tail_positions.add(
                    (self.knot_pos[knot_num][0], self.knot_pos[knot_num][1])
                )

        return

    def execute_moves(self, part2=False):
        # for each command line (direction, number-of-steps),
        #   move the head in direction given,
        #   adjusting the tail position after each step
        # refactored for Part 2 to handle 8 additional knots before tail
        if not part2:
            for command in self.moves:
                for step in range(command[1]):
                    self.move_head(command[0])
                    self.adjust_tail()
        else:
            for command in self.moves:
                for step in range(command[1]):
                    self.move_head(command[0])
                    self.knot_pos[0] = self.head_pos
                    for k in range(1, 10):  # 2nd knot[1] thru tail[9]; head is [0]
                        self.adjust_knot(k)

        return
