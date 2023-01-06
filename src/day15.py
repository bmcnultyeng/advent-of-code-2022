# Day #15: Beacon Exclusion Zone
# Part 1: In the row where y=2000000, how many positions cannot contain a beacon?
# Part 2: Find the only possible position for the distress beacon.
#           What is its tuning frequency (x-coord * 4_000_000)?

# Part 1 plan...
# 1) from input file, create a dict of all beacons, closest sensor &
#       calculated Manhatten distance; also a dict of beacons as key?
# 2) for each sensor, calc begin & end positions covered on the target row (y=10 or 2000000)
# 3) count the unique covered positions on the target line,
#       excluding beacons on the line;
#       avoid lists/comprehensions of all possible x-values;
#       use comparisons between min/max
# Part 2 plan...
# 1) find the single uncovered position within xy_range of
#       0 thru 20 (test data), 0 thru 4_000_000 (actual data);
#       by checking for gaps in the intervals on each y-line?
#         find line with merged intervals != [[0, 4_000_000]]
#         but would need to check 4 million lines!
#       or by analyzing the overlapping distances from each sensor?
# 2) return the tuning frequency = 4_000_000 *
#       x-coordinate of uncovered position + y-coordinate


class SensorGroup:
    """tracks the closest beacon to each sensor among the tunnels"""

    def __init__(self, sensor_file, line_y=10, part_2=False):
        """create dict of all sensors from input data;
        calc the manhattan distance from each sensor to the nearest beacon"""

        self.line_y = line_y
        self.part2 = part_2
        self.covered_ranges = []

        # key: x,y sensor; values: x,y nearest beacon & distance to beacon
        self.sensors = dict()

        # 1) from input file, create a dict of all beacons, closest sensor &
        #       calculated Manhatten distance
        with open(sensor_file, "r") as sfile:
            for line in sfile:
                if len(line.strip()) != 0:  # skip blank lines
                    s_spec, b_spec = line.split(":")
                    s_x = int(s_spec[s_spec.find("x=") + 2 : s_spec.find(", y=")])
                    s_y = int(s_spec[s_spec.find(", y=") + 4 :])
                    b_x = int(b_spec[b_spec.find("x=") + 2 : b_spec.find(", y=")])
                    b_y = int(b_spec[b_spec.find(", y=") + 4 :])
                    m_distance = abs(s_x - b_x) + abs(s_y - b_y)
                    self.sensors[(s_x, s_y)] = [(b_x, b_y), m_distance]
                    # TODO need a beacons dict also?

    def overlap_x_range(self, sensor_pos):
        """find min & max x-coord covered by a sensor on a line at y position"""

        if sensor_pos not in self.sensors:
            return None

        y_overlap = 1 + self.sensors[sensor_pos][1] - abs(self.line_y - sensor_pos[1])
        if y_overlap > 0:
            min_x = sensor_pos[0] - (y_overlap) + 1
            max_x = sensor_pos[0] + (y_overlap) - 1
            return [min_x, max_x]

        return None  # no overlap

    def merge_intervals(self, intervals):
        """merge overlapping min/max intervals, given a list of lists"""
        # per https://stackoverflow.com/questions/49071081/merging-overlapping-intervals-in-python
        #   answered by Uvar 3/2/18
        # xx not working for inclusive & overlapping intervals- see my corrections

        def recursive_merge(inter, start_index=0):
            for i in range(start_index, len(inter) - 1):
                # if inter[i][1] > inter[i + 1][0]:
                if inter[i][1] >= inter[i + 1][0]:  # me chg > to >=
                    new_start = inter[i][0]
                    new_end = inter[i + 1][1]
                    if inter[i][1] > new_end:  # added me
                        new_end = inter[i][1]  # added me
                    inter[i] = [new_start, new_end]
                    del inter[i + 1]
                    return recursive_merge(inter.copy(), start_index=i)
            return inter

        sorted_on_start = sorted(intervals)
        merged = recursive_merge(sorted_on_start.copy())
        # print(merged) #[[2, 10], [15, 18]]
        return merged

    # TODO create an ascii visualization on a print frame

    def solve_part1(self):
        """combine overlap ranges on the target line;
        count unique covered positions on the line, excluding known beacons"""

        # 2) for each sensor, calc begin & end positions covered on the target row (y=10 or 2000000)
        line_ranges = []
        for sensor_pos in self.sensors:
            interval = self.overlap_x_range(sensor_pos)
            if interval is not None:
                line_ranges.append(interval)

        # 3) count the unique covered positions on the target line,
        #       excluding beacons on the line;
        #       avoid lists/comprehensions of all possible x-values;
        #       use comparisons between min/max

        # handle overlapping x-ranges
        line_ranges = self.merge_intervals(line_ranges)

        # handle beacons on the line
        beacons_on_line = {
            val[0] for val in self.sensors.values() if val[0][1] == self.line_y
        }
        beacons_in_intervals = 0
        for beacon in beacons_on_line:
            for interval in line_ranges:
                if interval[0] <= beacon[0] <= interval[1]:
                    beacons_in_intervals += 1
        covered_positions_count = 0
        for interval in line_ranges:
            covered_positions_count += (
                interval[1] - interval[0] + 1
            )  # inclusive of interval end
        covered_positions_count -= beacons_in_intervals
        return covered_positions_count

    def solve_part2(self, max_xy=20):
        """find a y-line which has a gap in the interval 0 thru ymax;
        return the tuning frequence = gap x-coord * 4_000_000 + gap_y"""

        # TODO faster solution: follow the positions one unit outside the
        #      perimeter of each covered diamond, within 0-max_xy square
        #      alt 2: search within one unit of all intersections of
        #      line segments (diamonds & max_xy square)

        # find the merged intervals for each y-line
        #   for x == 0 thru max_xy
        for y in range(0, max_xy + 1):
            # same start as part 1 except disregard existing beacons
            self.line_y = y
            line_ranges = []
            for sensor_pos in self.sensors:
                interval = self.overlap_x_range(sensor_pos)
                intervals_to_delete = []
                if interval is not None:
                    # Part 2: limit x from 0 thru max_xy
                    if interval[0] < 0:
                        if interval[1] < 0:
                            intervals_to_delete.add(interval)
                        else:
                            interval[0] = 0
                    if interval[1] > max_xy:
                        if interval[0] > max_xy:
                            intervals_to_delete.add(interval)
                        else:
                            interval[1] = max_xy
                    line_ranges.append(interval)
            for interval in intervals_to_delete:
                line_ranges.remove(interval)

            # handle overlapping x-ranges
            line_ranges = self.merge_intervals(line_ranges)

            if line_ranges[0][0] != 0 or line_ranges[0][1] != max_xy:
                # find coordinates for gap
                gap_y = self.line_y
                # should be one or two merged intervals
                if line_ranges[0][0] != 0:
                    gap_x = 0
                else:
                    gap_x = line_ranges[0][1] + 1
                break  # for line_y; found the gap

        return (gap_x, gap_y, gap_x * 4_000_000 + gap_y)  # the tuning frequency
