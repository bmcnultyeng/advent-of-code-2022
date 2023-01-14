# Day #15: Proboscidea Volcanium
# Part 1: Work out the steps to release the most pressure in 30 minutes.
#           What is the most pressure you can release?
# Part 2: With you and an elephant working together for 26 minutes,
#           what is the most pressure you could release?

# Part 1 plan...
# 1) from input file, create a dict of all valves, flow rates
#      and connections to other valve rooms
# 2) convert the connections in the input dict to a similar dict of only the
#      valves with non-zero flow rates; add the shortest distance between the
#      n-z valves (will require DFS or BFS path optimizing?)
# 3) starting at valve AA, calc the total pressure release over 30 minutes for
#      every possible ordered combination of turning all valves on;
#      requires n-factorial interations! any way to shrten this?
#         TODO 'Hash' optimization (built into a dict in Python):
#               a) save the result (days remaining & pressure reduction)
#                  of every path simulated that starts at AA, of length >= 2
#               b) for each new pattern, find the longest path that
#                  has already been traversed, skip to the end of
#                  'hashed' path, and finish simulating the path
#               c) for Part 2, eventually most paths would have already been
#                  hashed by the other traveler (me or elephant)
#
# Part 2 plan...
# 3') test for the maximum result, using itertools.permutations to generate
#       non-zero valve routes for you and the elephant, unique from each other;
#       ?assume each route is 7 of 14 nz valves?

import itertools


class ValveGroup:
    """maximumize pressure relief by opening the optimal valves within 30 minutes"""

    def __init__(self, valves_file, part_2=False):
        """create dict of all valves from input data"""

        self.part2 = part_2

        # key: valve name; values: flow rate, adjacent valves (all distances = 1)
        self.valves_input = dict()  # from input file; includes zero-rate valves

        # 1) from input file, create a dict of all valves, flow rates
        #      and connections to other valve rooms
        with open(valves_file, "r") as vfile:
            for line in vfile:
                if len(line.strip()) != 0:  # skip blank lines
                    # example: "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
                    valve_name = line[6:8]
                    flow_rate = int(line[line.find("=") + 1 : line.find(";")])
                    if len(line) <= 52:  # only one connection
                        # TODO ??make connections a set, for BFS code
                        connections = [line[-3:-1]]
                    else:
                        connections = line[line.find("valves") + 7 : -1].split(", ")
                    self.valves_input[valve_name] = [flow_rate, connections]

        # 2) convert the connections in the input dict to a similar dict of only the
        #      valves with non-zero flow rates and "AA" starting node;
        #      include the shortest distances to each
        #      n-z valve (will require DFS or BFS path optimizing?)

        # map of distances from "AA" & nz valves to all other nz valves
        # key: non-zero valve; values: flow rate, dict of other n-z valves & distances
        self.valves_nz = dict()
        nz_list = [k for k, v in self.valves_input.items() if v[0] != 0]
        for node in ["AA"] + nz_list:
            self.valves_nz[node] = [
                self.valves_input[node][0],
                self.distances_to_other_nz_nodes(node),
            ]
            # self.valves_nz[node] = [self.valves_input[node][0], dict()]
            # for nz in nz_list:
            #     if nz != node:
            #         # distances determined by BFS searches
            #         self.valves_nz[node][1][nz] = 0
        _ = "breakpoint for debug"

        # for each non-zero flow rate valve, find shortest paths to the other n-z valves
        # potential Part 1 plan ...
        #       - use BFS algorithm to find the shortest distances from each node
        #         to all other nodes
        #       - build a connections dict that includes these distances,
        #         using only the n-z nodes as a key or value
        #       - use the generator function itertools.permutations() to
        #         test all paths, starting at valve AA and
        #         visiting all other n-z valves; track the max 30-min pressure relief
        #         and the associated path

    def distances_to_other_nz_nodes(self, start):
        """find the shortest distance from a node to all other
        valves with non-zero rates, loosely based on BFS (breadth first search)"""
        # woks for a small number of nodes

        current_nodes = {start}
        next_nodes = set()
        visited = {start}
        distance = 0  # 'level' of the search; distance from start
        nz_distances = dict()

        while current_nodes:
            distance += 1
            for cur in current_nodes:
                next_nodes.update(self.valves_input[cur][1])
            for nex in next_nodes:
                if nex not in visited and self.valves_input[nex][0] != 0:
                    nz_distances[nex] = distance
            current_nodes = next_nodes.copy() - visited
            visited.update(next_nodes)
            next_nodes.clear()
        return nz_distances

    def pressure_relief(self, valve_list, time_limit=30):
        """calculate the pressure relieved in 30 minutes by
        opening valves in the order listed"""
        from_node = "AA"
        time_remaining = time_limit  # Part 1: 30 minutes; Part 2: 26 min
        pressure_reduction = 0  # total pressure released over 30 min
        last_valve_opened = valve_list[-1]
        for to_node in valve_list:
            # minutes remaining after moving to and opening valve
            time_remaining -= 1 + self.valves_nz[from_node][1][to_node]
            if time_remaining < 0:
                # return f"Time remaining: {time_remaining}  to_node {to_node} of {valve_list}"
                return pressure_reduction, from_node  # last valve opened
            # pressure reduction contributed by this valve (flow-rate * minutes-remaining)
            pressure_reduction += time_remaining * self.valves_nz[to_node][0]
            from_node = to_node
        return pressure_reduction, valve_list[-1]

    def solve_part1(self, max_valves=6):
        """compare all permutations of valve openings; ?maximum pressure relief"""
        max_pressure_reduction = 0
        best_valve_order = tuple()
        nz_valves = [x for x in self.valves_nz.keys() if x != "AA"]
        # visited = set()
        # for valve_order in itertools.permutations(nz_valves):
        for valve_order in itertools.permutations(nz_valves, max_valves):
            # ??more efficient way of comparing shorter visited tuples to valve_orser
            # ?? try limiting length of itertools.permutations to 6 or 8?
            # already_visited = False
            # for vis in visited:
            #     if vis == valve_order[:len(vis)]:
            #         # a shorter valve list has already been tested
            #         already_visited = True
            #         break
            # if not already_visited:
            current_reduction, last_valve_opened = self.pressure_relief(valve_order)
            if current_reduction > max_pressure_reduction:
                max_pressure_reduction = current_reduction
                best_valve_order = valve_order[
                    : valve_order.index(last_valve_opened) + 1
                ]
            # visited.update(valve_order[: valve_order.index(last_valve_opened) + 1])
        return max_pressure_reduction, best_valve_order

    def solve_part2(self, split_valves=3):
        """compare all permutations of valve openings; ?maximum pressure relief;
        Part 2: give half of each permutation to me & the elephant;
        use split_valves=3 for test data; use split_valves=7 for actual data"""
        # this could take a long time to execute on the actual data!
        # assume all valves can be opened within 26 minutes by me & elephant
        max_pressure_reduction = 0
        best_valve_order = tuple()
        nz_valves = [x for x in self.valves_nz.keys() if x != "AA"]
        # visited = set()

        for valve_order in itertools.permutations(nz_valves):
            current_reduction_1, last_valve_opened = self.pressure_relief(
                valve_order[:split_valves], time_limit=26
            )
            current_reduction_2, last_valve_opened = self.pressure_relief(
                valve_order[split_valves:], time_limit=26
            )
            if current_reduction_1 + current_reduction_2 > max_pressure_reduction:
                max_pressure_reduction = current_reduction_1 + current_reduction_2
                best_valve_order = valve_order

        return max_pressure_reduction, best_valve_order

        # # based on "Depth-First Search and Breadth-First Search in Python"
        # # by Edd Mann  on 05 Mar 2014
        # # at https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

        # # an iterative approach to BFS, modified to remember all n-z node distances...
        # visited = set()
        # queue = [start]
        # connections = dict()
        # distance = 0

        # while queue:
        #     distance += 1
        #     vertex = queue.pop(0)
        #     if vertex not in visited:
        #         visited.add(vertex)
        #         # set object overloads subtraction operator
        #         queue.extend(self.valves_input[vertex] - visited)
