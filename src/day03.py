# Day #3: Rucksack Reorganization


def calc_priority(rucksack):  # Part 1
    #   split line into 2 strings
    #   find the common item type as intersection of sets
    #   calc the priority of the resulting item type

    common_item = "".join(
        set(rucksack[(len(rucksack) // 2) :]).intersection(
            set(rucksack[: (len(rucksack) // 2)])
        )
    )
    if common_item.isupper():
        return ord(common_item) - 38
    else:
        return ord(common_item) - 96


def priorities(rucksacks_file):  # Part 1
    # for each rucksack/line:
    # return the sum of priorities for all rucksacks/lines
    total_priorities = 0
    with open(rucksacks_file, "r") as rfile:
        for line in rfile:
            if len(line.strip()) > 0:  # skip blank line
                total_priorities += calc_priority(line.strip())

    return total_priorities  # Part 1


def calc_group_priority(three_sacks):
    #   find the item type common to 3 rucksacks in a group
    common_item = "".join(
        set(three_sacks[0]).intersection(set(three_sacks[1]), set(three_sacks[2]))
    )
    #   calculate the priority for the common item
    if common_item.isupper():
        return ord(common_item) - 38
    else:
        return ord(common_item) - 96


def group_priorities(rucksacks_file):  # Part 2
    # for each group of 3 rucksacks/lines
    # return the sum of priorities for all groups of 3
    total_priorities = 0
    with open(rucksacks_file, "r") as rfile:
        all_lines = rfile.readlines()
        for i in range(0, len(all_lines), 3):
            if len(all_lines[i].strip()) > 0:  # skip blank line
                three_sacks = (
                    all_lines[i].strip(),
                    all_lines[i + 1].strip(),
                    all_lines[i + 2].strip(),
                )
                total_priorities += calc_group_priority(three_sacks)
    return total_priorities
