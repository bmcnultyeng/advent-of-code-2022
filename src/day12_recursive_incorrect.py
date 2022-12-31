# Day 12: Hill CLimbing Algorithm
# XXX This recursive version was abandoned in favor of the A-star algorithm

# Part #1: find the shortest path on a grid from S to E, obeying the following rules:
#  elevation increases from 'a to 'z'; start location 'S' at 'a'; end location 'E' at 'z'
#  each step moves one position to left, right, up or down
#  can not move off the edge of the grid
#  can move to any elevation at most 1 level higher; i.e. can move to any lower, same or 1 higher
#  optimally, you should not revisit any location
# plan...
#  read grid of elevations, start location and end location from input file
#    store the grid as a list of elevation-letter rows (grid[0][0] at upper left)
#    create a similar nested list of visited-flag, all initially False
#  trace each possible path (recursively?):
#    stop tracing the path when any of the following are true:
#      no unvisited location adjacent
#      no legal elevation adjacent
#      step count >= minimum count of previous paths
#      reached End
# solution to Part #1: fewest steps required to move from Start to End

import sys


class Grid:
    """loads initial data from input file"""

    def __init__(self, elevations_file=""):
        # read & parse all lines of data file (elevation letters) as a nested list

        # indexes represent each location on the grid
        self.elevations = []  # nested list of integers (a -> 0, z -> 25)
        # table of visited status for each location
        #   >0 on a path to End;
        #   0 target never visited (initial value);
        #  -1: on a condemned path or busy (looped back to current path)
        self.visited = []
        self.start_loc = ()
        self.end_loc = ()
        # self.step_count = 0

        if len(elevations_file) != 0:
            # read input file and initialize data
            with open(elevations_file, "r") as efile:
                for line in efile:
                    if len(line.strip()) != 0:  # skip blank lines
                        row = []
                        row = [ord(char) - 97 for char in line.strip()]
                        if line.find("S") >= 0:
                            self.start_loc = (len(self.elevations), line.find("S"))
                            row[line.find("S")] = 0  # Start has elevation 'a'
                        if line.find("E") >= 0:
                            self.end_loc = (len(self.elevations), line.find("E"))
                            row[line.find("E")] = 25  # End has elevation 'z'
                        self.elevations.append(row)
                        # visited status table; initialize to 0 for never visited
                        self.visited.append(
                            [
                                0,
                            ]
                            * len(row)
                        )
                # initialize best_step_count as higher than possible count
                self.best_step_count = len(self.visited) * len(self.visited[0])

        else:  # for debug using dummy data_lines
            pass
        return

    def blocked_test(self, cur_loc, targ_loc, steps):
        """test if move complies with rules, exists or on a proven path to End;
        returns -1 (blocked or busy) or >0 (step count to End; 1 if target loc is End)"""
        # an empty return string can be tested as False;
        # can return True or False to optimize?

        # 1) target location (row,colm) exists on grid
        if not (
            (0 <= targ_loc[0] < len(self.elevations))
            and (0 <= targ_loc[1] < len(self.elevations[0]))
        ):
            return -1  # outside grid

        # 2) height of target location is higher, same, or one lower
        if (
            self.elevations[cur_loc[0]][cur_loc[1]]
            < self.elevations[targ_loc[0]][targ_loc[1]] - 1
        ):
            return -1  # too high

        # 3) current steps count is higher than a previous count that reached End
        if steps > self.best_step_count:
            return -1  # best successful steps count exceeded

        # # 4) target is the End location TODO move this into explore_path
        # if targ_loc == self.end_loc:
        #     return 1  # found End location one step away

        # >0 on a path to End; 0 target never visited; -1: on a condemned path or busy (looped back to current path)
        return self.visited[targ_loc[0]][targ_loc[1]]

    def explore_path(
        self,
        cur_loc,
        prev_loc=(-1, -1),
        # explored_status=-1,
        steps=0,
        # direction_list=["up", "down", "left", "right"],
    ):  # initialized the previous location outside grid
        """recursively attempt every possible path;
        stop an excursion when target location is blocked or reached End"""

        if steps > 100:  # temporarily, avoid runaway recursion
            sys.exit("Number of steps exceeded (temporary limit).")

        # directions = direction_list

        # TODO apply concepts from TalkP recursive course...
        #   - what state are we maintaining? thread the state through the recursive call
        #       state: current location, previous location, step count [ignore visited list]
        #   - identify base case & recursive case
        #       base case: reached end of path (targ_loc is blocked or End); if End update best count
        #       recursive case: for all 4 directions (except prev_loc), move to next unblocked location (cached?)

        # for loop for each direction; not the contents of a directions list (avoid list slicing or popping in recursives)

        # set visited status = -1 for current location to show "busy", in case search path loops back on itself
        self.visited[cur_loc[0]][cur_loc[1]] = -1
        results_gt_zero = (
            []
        )  # accumulate results >0 from testing all 3 directions; use best before reuturn

        for targ_loc in [
            (cur_loc[0], cur_loc[1] - 1),
            (cur_loc[0], cur_loc[1] + 1),
            (cur_loc[0] - 1, cur_loc[1]),
            (cur_loc[0] + 1, cur_loc[1]),
        ]:  # left, right, up, down

            # recursive case: move to target location if not blocked/ End or is the previous location or is busy on a working path
            if targ_loc != prev_loc:
                blocked_status = self.blocked_test(
                    cur_loc, targ_loc, steps
                )  # will be -1, 0 or >0
                if blocked_status > 0:
                    # target already on a successful path to End
                    # compare to best count current & overall
                    # update best steps
                    # TODO some logic is bad here ??
                    # TODO ?save results from each direction, then keep best, after testing all 3 directions?
                    results_gt_zero.append(blocked_status)

                    # if steps + blocked_status < self.best_step_count:
                    #     # found a shorter path to End
                    #     self.best_step_count = steps + blocked_status
                    #     self.visited[cur_loc[0]][cur_loc[1]] = blocked_status + 1
                    # elif self.visited[cur_loc[0]][cur_loc[1]] > blocked_status + 1:
                    #     # this location on a longer path to the End location
                    #     self.visited[cur_loc[0]][cur_loc[1]] = blocked_status + 1
                    # # otherwise, this location already on a shorter path to the End location

                elif blocked_status == 0:
                    if targ_loc == self.end_loc:
                        # 0: target is the End location => end case
                        # path to End is one step away; End location will never be visited
                        self.visited[cur_loc[0]][cur_loc[1]] = 1
                        # update current visited status if a better path found to End
                        if steps + 1 < self.best_step_count:
                            # found a shorter path to End
                            self.best_step_count = steps + 1
                        return 1  # found End location one step away; no need to search other directions

                    # 0: target never visited & End not reached => recursive case
                    steps += 1
                    # move to target location and explore from there
                    explored_status = self.explore_path(targ_loc, cur_loc, steps)

                    results_gt_zero.append(blocked_status)

                    # # update current visited status if a better path found to End
                    # if explored_status > 0:  # otherwise would be -1 but no longer 0;
                    #     if steps + explored_status < self.best_step_count:
                    #         # found a shorter path to End
                    #         self.best_step_count = steps + explored_status
                    #     self.visited[cur_loc[0]][cur_loc[1]] = explored_status + 1

                # otherwise will be -1: skip this direction;
                #   on a condemned path or busy path (looped back to current path);
                #   no need to modify visited status of current location for this direction

        # after testing in 3 new directions, recur to previous location's search
        # return visible status of current loc thru explored_status of upstream location
        if len(results_gt_zero) > 0:
            self.visited[cur_loc[0]][cur_loc[1]] = min(
                results_gt_zero
            )  # otherwise remains -1
        return self.visited[cur_loc[0]][cur_loc[1]]


# ................................................................
# if target_status > 0:
#     # found a successful path to End
#     if steps + target_status < self.best_step_count:
#         # found a shorter path to End
#         self.best_step_count
#         return target_status + 1  # one step back up best path
#     else:
#         # not a shorter path to end
#         return -1
# else:

#     # 0: target never visited; -1: on a condemned path or busy (looped back to current path)

# blocked or busy on current path
#  if not blocked (including End), continue exploring from target location
# steps += 1
# self.explore_path(targ_loc, (cur_loc[0], cur_loc[1]), steps)

# if directions:
#     match directions.pop():
#         case "up":
#             targ_loc = (cur_loc[0], cur_loc[1] - 1)
#         case "down":
#             targ_loc = (cur_loc[0], cur_loc[1] + 1)
#         case "left":
#             targ_loc = (cur_loc[0] - 1, cur_loc[1])
#         case "right":
#             targ_loc = (cur_loc[0] + 1, cur_loc[1])

#     # test if target is blocked
#     if not self.blocked(cur_loc, targ_loc, steps):
#         #  if not blocked (including End), continue exploring from target location
#         self.explore_path(targ_loc, steps, ["up", "down", "left", "right"])
#     #  if blocked, return to previous location's search
#     else:
#         self.explore_path(cur_loc, steps)

# else:  # empty list;
#     # return to previous location after attempting all 4 directions
#     return
