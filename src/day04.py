# Day #4: Camp Cleanup

# for each pair of assignments (line in text file):
#   parse the start & end of each range of assigned sections
#   compare the two ranges
#   increment count if one range fully contains the other
# return count of contained pairs


def has_contained_range(assignment):  # Part 1
    if len(assignment.strip()) == 0:  # skip blank line
        return False
    #   parse the start & end of each range of assigned sections, as integers
    limits = assignment.strip().replace(",", "-").split("-")
    limits = [int(x) for x in limits]
    #   compare the two ranges
    if (limits[0] <= limits[2]) and (limits[1] >= limits[3]):  # 1st contains 2nd
        return True
    if (limits[0] >= limits[2]) and (limits[1] <= limits[3]):  # 2nd contains 1st
        return True
    return False


def count_contained(assignments_file):  # Part 1
    # for each pair of assignments (line in text file):
    #   increment count if one range fully contains the other
    # return count of contained pairs
    total_contained = 0
    with open(assignments_file, "r") as afile:
        for line in afile:
            if len(line.strip()) > 0:  # skip blank line
                if has_contained_range((line.strip())):
                    total_contained += 1

    return total_contained  # Part 1


def has_overlap_range(assignment):  # Part 2
    if len(assignment.strip()) == 0:  # skip blank line
        return False
    #   parse the start & end of each range of assigned sections, as integers
    limits = assignment.strip().replace(",", "-").split("-")
    limits = [int(x) for x in limits]
    #   compare the two ranges, as sets of the section numbers
    range1 = {x for x in range(limits[0], limits[1] + 1)}
    range2 = {x for x in range(limits[2], limits[3] + 1)}

    if range1.intersection(range2):  # if length >0
        return True
    return False


def count_overlap(assignments_file):  # Part 1
    # for each pair of assignments (line in text file):
    #   increment count if one range partly contains the other
    # return count of overlapping pairs
    total_overlap = 0
    with open(assignments_file, "r") as afile:
        for line in afile:
            if len(line.strip()) > 0:  # skip blank line
                if has_overlap_range((line.strip())):
                    total_overlap += 1

    return total_overlap  # Part 1
