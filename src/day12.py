# Day 12: Hill CLimbing Algorithm

# Part #1: find the shortest path on a grid from S to E, obeying the following rules:
#  elevation increases from 'a to 'z'; start location 'S' at 'a'; end location 'E' at 'z'
#  each step moves one position to left, right, up or down
#  can not move off the edge of the grid
#  can move to any elevation at most 1 level higher; i.e. can move to any lower, same or 1 higher
#  optimally, you should not revisit any location
# plan...
#   generate an adjacency-list representation of the graph, using the height matrix data
#   use the a-star (A*) path search algorithm to find the shortest distance between Start and End positions
# solution to Part #1: fewest steps required to move from Start to End
# Part #2: find the shortest path from any square at elevation a to the square marked E.
#   Part 2 solution: shortest of all possible paths, starting at any a elevation?
#   there are 6 occurances of a in the test data;
#   1862 in my input file ==> works, but takes ~4 seconds to run A* on all occurances

import sys


class Grid:
    """creates adjacencies from height data; uses A8 to find shortest path"""

    def __init__(self, elevations_file=""):
        """read & parse all lines of data file (elevation letters) into an adjacency-list dictionary"""

        # nested list of integers of row/col of the height grid (a -> 0, z -> 25)
        self.elevations = []

        # nested list (matrix) of known distances from Start node;
        # initially infinity for all except Start =0
        self.distances = []

        # keys represent each location on the grid
        # values are adjacent locations with legal moves (not exceeding one higher)
        self.adjacencies = {}

        # table of visited status for each location
        self.visited = []
        self.start_loc = ()
        self.end_loc = ()

        if len(elevations_file) != 0:
            # read input file and initialize data
            with open(elevations_file, "r") as efile:
                # create elevations & visited matrixes
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

                        # visited status table; initialize as False for unvisited
                        self.visited.append(
                            [
                                False,
                            ]
                            * len(row)
                        )

                        # initialize the distances matrix with float("inf")
                        #   distances from the Start node; set =0 at Start
                        self.distances.append(
                            [
                                float("inf"),
                            ]
                            * len(row)
                        )

                self.distances[self.start_loc[0]][self.start_loc[1]] = 0

                # optimized using a priority queue, aka open set or fringe
                # initialize dict as only the start node
                self.fringe = {
                    self.start_loc: self.heuristic((self.start_loc), (self.end_loc))
                }
                # Wikipedia description... At each step of the algorithm, the node with the
                # lowest f(x) value is removed from the queue, the f and g values of its neighbors
                # are updated accordingly, and these neighbors are added to the queue.
                # The algorithm continues until a removed node (thus the node with the
                # lowest f value out of all fringe nodes) is a goal node.
                #   f(n)=g(n)+h(n)  for node n, f is total cost of the path,
                #     g is known cost from Start, and h is estimated (heuristic) cost to End

                # generate a directed adjacencies-list representation of the graph by comparing elevations
                for i, row in enumerate(self.elevations):
                    for j, height in enumerate(row):
                        neighbors = []
                        for direction in [
                            [0, 1],
                            [0, -1],
                            [1, 0],
                            [-1, 0],
                        ]:  # right,left,up,down
                            if 0 <= i + direction[0] < len(
                                self.elevations
                            ) and 0 <= j + direction[1] < len(
                                row
                            ):  # within grid
                                if (
                                    height
                                    >= self.elevations[i + direction[0]][
                                        j + direction[1]
                                    ]
                                    - 1
                                ):  # at most one higher
                                    neighbors.append(
                                        (i + direction[0], j + direction[1])
                                    )
                            pass
                        self.adjacencies[(i, j)] = neighbors

        else:  # for debug using dummy data_lines
            pass
        return

    def heuristic(self, point_1, point_2, method="straight_line"):
        """shortest distance between two x,y points;
        for A*, this estimate should always be shorter than actually possible;
        input: two tuples of x,y or row/column coordinates
        & optional method string"""
        if method == "straight_line":
            # straight-line- usually best for A*
            straight_line_distance = (
                (point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2
            ) ** 0.5
            return straight_line_distance
        elif method == "manhattan":
            # manhattan distance (move 4 directions NSEW or UDLR) can sometimes be more efficient
            manhattan_distance = abs(point_1[0] - point_2[0]) + abs(
                point_1[1] - point_2[1]
            )
            return manhattan_distance
        else:
            return 0

    def a_star(self, max_count=100):
        """use the A* algorithm to find the shortest path from Start to End,
        optimized by a priority queue (fringe); all costs (distance between nodes) = 1"""
        # 0) repeat until exiting in step 1) or 2); use 'repeat while True' or a max count
        for _ in range(max_count):
            # 1) find a node with the lowest current priority; no path found if queue is empty
            if len(self.fringe) == 0:
                msg = "No path found."
                # return msg
                return float("inf")

            lowest_cost = min(self.fringe.values())
            best_nodes = [
                node for node in self.fringe if self.fringe[node] == lowest_cost
            ]
            current_node = best_nodes[0]  # a random choice, for now

            if current_node == self.end_loc:
                # 2) if it is the End node, return it's priority as the best distance solution
                # return f"Shortest path is {lowest_cost} steps."  # TODO verify this is correct!
                return lowest_cost

            # 3) add all unvisited neighboring nodes to the queue with updated priorities;
            for neighbor in self.adjacencies[current_node]:
                if not self.visited[neighbor[0]][neighbor[1]]:
                    self.distances[neighbor[0]][neighbor[1]] = (
                        self.distances[current_node[0]][current_node[1]] + 1
                    )
                    self.fringe[neighbor] = self.distances[neighbor[0]][
                        neighbor[1]
                    ] + self.heuristic(neighbor, self.end_loc)

            # 4) remove the current node from the queue; mark as visited
            del self.fringe[current_node]
            self.visited[current_node[0]][current_node[1]] = True

        msg = f"Limit of {max_count} A-star steps exceeded."
        return msg

    def restart_grid(self, new_start_node):
        """reset the start_loc, fringe dict, directions matrix & visited matrix"""

        for i in range(len(self.visited)):
            self.visited[i] = [
                False,
            ] * len(self.visited[0])

        for i in range(len(self.distances)):
            self.distances[i] = [
                float("inf"),
            ] * len(self.distances[0])
        self.distances[new_start_node[0]][new_start_node[1]] = 0

        self.fringe = {new_start_node: self.heuristic((new_start_node), (self.end_loc))}

        self.start_loc = new_start_node


def part2_solution(elevations_file):
    """create a Grid instance starting at each 'a' node;
    find the closest start node to the End node"""

    grid = Grid(elevations_file)

    # initialize a dictionary of all possible Start nodes with 'a' elevation (height=0)
    start_nodes_part2 = {}
    for i, row in enumerate(grid.elevations):
        for j, height in enumerate(row):
            if height == 0:
                start_nodes_part2[(i, j)] = float("inf")

    # find the shortest path from each possible Start to the End node
    for new_start_node in start_nodes_part2:
        grid.restart_grid(new_start_node)
        start_nodes_part2[new_start_node] = grid.a_star(10000)

    # solution to Part #2
    shortest_distance = min([val for val in start_nodes_part2.values()])
    return shortest_distance
