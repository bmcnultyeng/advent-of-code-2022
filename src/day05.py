# Day #5: Supply Stacks

# Part 1: crates move one at a time
# Part 2: multiple crates can be moved at one time


def parse_stacks(input_lists):
    layers = []
    for line in input_lists:
        if line[1] == "1":
            stack_count = int(line.split()[-1])
            break  # end of layers input lines
        # show crates above top of stack as " " placeholder
        layers.insert(0, [line[i] for i in range(1, len(line), 4)])

    # assemble stacks by layer
    stacks = list(zip(*layers))
    stacks = [[crate for crate in stack if crate != " "] for stack in stacks]

    return stacks, len(layers) + 1


def move_crates(stacks, move_command, move_multiple_crates=False):
    # for each move, like "move 2 from 2 to 1":
    #   pop & push crates between spcified stacks
    move_command = move_command.split()
    if move_multiple_crates:
        stacks[int(move_command[5]) - 1] = stacks[int(move_command[5]) - 1] + (
            stacks[int(move_command[3]) - 1][-int(move_command[1]) :]
        )
        stacks[int(move_command[3]) - 1] = stacks[int(move_command[3]) - 1][
            : -int(move_command[1])
        ]

    else:
        for i in range(int(move_command[1])):  # number of crates to be moved
            stacks[int(move_command[5]) - 1].append(
                stacks[int(move_command[3]) - 1].pop()
            )
    return stacks


def organize_stacks(crates_file, move_multiple_crates=False):
    # crates are moved singly (Part 1) or together (Part 2) per the optional parameter move_multiple_crates
    top_crates = ""
    # read all lines of input file
    with open(crates_file, "r") as cfile:
        all_lines = cfile.readlines()
    # parse stacks & moves into nested lists
    stacks, last_line_number = parse_stacks(all_lines)
    # skip blank line between layers lines & moves lines
    for line in all_lines[last_line_number:]:
        if len(line.strip()) > 0:  # skip blank lines (separator or EOF)
            move_crates(stacks, line, move_multiple_crates)
    # return the labels for the crates on top
    for stack in stacks:
        top_crates += stack[-1]
    return top_crates
