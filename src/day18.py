# Day 18: Boiling Boulders

# plan for Part 1...
#   make an adjacencies dict, like a path search map
#   subtract the count of adjacent faces from total
#     of 6 faces per cube = surface area
# plan for Part 2...
#   an internal cubic space will be adjacent to 6 cubes or
#     other internal spaces
#   1) find a 3-D path from each non-lava point within the drop to a
#      known outside point; my previous A* algo should work well;
#      if no path, that point is an internal air cube;
#      note that min & max x,y&z are 0 & 21 for the actual data, so the
#      search area can be limited to enclosing 22-unit cube;
#      any point with a negative coord would be external;
#      the search can be accelerated by caching the result of air cubes
#      along fully-explored paths (connected to or fully blocked from outside)
#   2) count the adjacencies of each trapped air cube with faces of solid cubes;
#      subtract this internal surface area total s.a. to get external s.a.


class LavaDroplet:
    """Cooling lava forms obsidian; find cubic surface area"""

    def __init__(self, lava_file):
        """get cubic coordinates; set adjacencies dict"""

        self.cubes = set()

        with open(lava_file, "r") as lfile:
            for line in lfile:
                if len(line.strip()) != 0:  # skip blank lines
                    # read (x,y,z) coordinates of cube centroids in the droplet
                    self.cubes.add(tuple(int(x) for x in line.strip().split(",")))

        self.adjacencies = dict()

        for cube in self.cubes:
            # note: didn't need adjacencies for solids for part 1,
            #   thought it might be needed it in part 2
            self.adjacencies[cube] = set()
            for other in (x for x in self.cubes if x != cube):  # generator object
                if (other[0], other[1]) == (cube[0], cube[1]) and abs(
                    other[2] - cube[2]
                ) == 1:
                    self.adjacencies[cube].add(other)
                if (other[0], other[2]) == (cube[0], cube[2]) and abs(
                    other[1] - cube[1]
                ) == 1:
                    self.adjacencies[cube].add(other)
                if (other[1], other[2]) == (cube[1], cube[2]) and abs(
                    other[0] - cube[0]
                ) == 1:
                    self.adjacencies[cube].add(other)
            self.total_surface_area = self.surface_area()

    def surface_area(self):
        """find total surface area, i.e. number of solid cube faces
        that are not located adjacent to faces of other cubes"""
        adjacent_faces = sum([1 for val in self.adjacencies.values() for cube in val])
        surface_area = 6 * len(self.cubes) - adjacent_faces
        return surface_area

    def external_surface_area(self, min_coord=0, max_coord=21):
        """faces of solid cubes that have an open path to the outside of the lava drop"""
        # points/cubes within min/max_coord that are not solid cubes;
        # includes an air envelope that is one cube thick on all sides of
        #   min-coord & max-coord, to allow flood-fill from outside
        self.air_cubes = dict()
        for x in range(min_coord - 1, max_coord + 2):
            for y in range(min_coord - 1, max_coord + 2):
                for z in range(min_coord - 1, max_coord + 2):
                    if (x, y, z) not in self.cubes:
                        # initialize the 'connected' value = False
                        # the flood-fill algo will flip 'connected' values
                        #   to True if connected to outside air cubes
                        self.air_cubes[(x, y, z)] = False

        # flood-fill algo starting in a corner of the outside air envelope
        self.flood_fill((min_coord - 1, min_coord - 1, min_coord - 1))

        # count solid faces that are adjacent to trapped air cubes
        trapped_solid_faces = 0
        for trapped_air_cube in (xyz for xyz, val in self.air_cubes.items() if not val):
            # test whether each adjacent face abuts a solid cube
            trapped_solid_faces += self.adjacent_solids(trapped_air_cube)
        exposed_solid_faces = self.total_surface_area - trapped_solid_faces
        return exposed_solid_faces  # solution for example data = 58

    def flood_fill(self, start_pos):
        """iterative DFS algo to flip the 'connected' value to True
        for any air cube connected to the outside air envelope;
        the 'connected' value is equivalent to the algo's 'visited' flag"""

        # use depth-first-search DFS to follow all possible paths;
        # use iterative with a queue, not recursive, since a large map;
        # start the flood-fill in an 1-unit 3-D envelope of air cubes
        #   outside the drop bounds, initailized as connected=False;
        #   flood-fill along all possible paths with connected=True;

        # no need to verify start_pos within bounds or not visited, here

        # initialize a FIFO queue with the current position
        queue = [start_pos]
        # mark the current position as visited/connected
        self.air_cubes[start_pos] = True

        # DFS: pop current from queue; mark current as visited in map;
        #   add unvisited adjacents to queue; repeat
        while len(queue) > 0:
            cur_pos = queue.pop(0)

            next_pos = (cur_pos[0] + 1, cur_pos[1], cur_pos[2])
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)
            next_pos = (cur_pos[0] - 1, cur_pos[1], cur_pos[2])
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)
            next_pos = (cur_pos[0], cur_pos[1] + 1, cur_pos[2])
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)
            next_pos = (cur_pos[0], cur_pos[1] - 1, cur_pos[2])
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)
            next_pos = (cur_pos[0], cur_pos[1], cur_pos[2] + 1)
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)
            next_pos = (cur_pos[0], cur_pos[1], cur_pos[2] - 1)
            if next_pos in self.air_cubes and not self.air_cubes[next_pos]:
                self.air_cubes[next_pos] = True
                queue.append(next_pos)

    def adjacent_solids(self, air):
        """count solid cubes adjacent to any face of the air cube"""
        adjacent_count = 0
        if (air[0] + 1, air[1], air[2]) in self.cubes:
            adjacent_count += 1
        if (air[0] - 1, air[1], air[2]) in self.cubes:
            adjacent_count += 1
        if (air[0], air[1] + 1, air[2]) in self.cubes:
            adjacent_count += 1
        if (air[0], air[1] - 1, air[2]) in self.cubes:
            adjacent_count += 1
        if (air[0], air[1], air[2] + 1) in self.cubes:
            adjacent_count += 1
        if (air[0], air[1], air[2] - 1) in self.cubes:
            adjacent_count += 1
        return adjacent_count


# thanks for the best DFS / flood-fill examples (iterative & recursive) at
# https://playandlearntocode.com/article/flood-fill-algorithm-in-python
# by Goran Trlin
