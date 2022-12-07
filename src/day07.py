# Day #7: No Space Left On Device

# Part 1: find paths(directories incl subdirectories) with at most 100,000 size
# Part 2: delete the smallest possible to create at least 30,000,000 unused space
#   for the update, out of total 70,000,000 total disk space

# read all lines of terminal output
# for each line:
#   if a command, $ prompt:
#     if command is "cd":
#       move in or out of directory structure (nested dict, not needed for Part 1?)
#       update current path (list)
#     if command is "ls":
#       no action needed; listing output should follow
#   if part of a listing, no $ prompt:
#     update directory structure (nested dict?) for the current dir
#     update PATH size totals (dict) for all PATHS (tuple keys) in current path
# note: no need to track the directory structure, assuming:
#   - all cd commands are legitimate
#   - ls commands are executed only once for each dir
# hint: all dir names are unique (NOT! so use PATH sizes!)


# def update_dir_sizes(current_path, dir_sizes, file_size):
#     # not used; replaced by update_path_sizes()
#     for dir in current_path:
#         if dir in dir_sizes:
#             dir_sizes[dir] += file_size
#         else:
#             dir_sizes[dir] = file_size
#     return dir_sizes


def update_path_sizes(current_path, path_sizes, file_size):
    # replaces update_dir_sizes()
    for i in range(len(current_path)):
        path = tuple(current_path[0 : i + 1])
        if path in path_sizes:
            path_sizes[path] += file_size
        else:
            path_sizes[path] = file_size
    return path_sizes


def calc_path_sizes(all_lines):
    # TODO refactor as a Path_Size class?
    # TODO refactor using match/case?
    current_path = []
    # dir_sizes = {}
    path_sizes = {}
    for line in all_lines:
        if len(line.strip()) > 0:  # skip blank lines (EOF)
            output = line.strip().split()
            if output[0] == "$":
                if output[1] == "cd":
                    # move in or out of directory structure (nested dict, not needed for Part 1?)
                    # update current path (list)
                    if output[2] == "..":
                        current_path.pop()
                    else:
                        current_path.append(output[2])
            else:  # a listing line
                # if output[0] != "dir":
                #     dir_sizes = update_dir_sizes(
                #         current_path, dir_sizes, int(output[0])
                #     )
                if output[0] != "dir":
                    path_sizes = update_path_sizes(
                        current_path, path_sizes, int(output[0])
                    )
    return path_sizes


def process_commands(output_file, part2=False):
    # read all lines of input file
    total_size = 0
    with open(output_file, "r") as ofile:
        all_lines = ofile.readlines()
        # parse & process each command line

        path_sizes = calc_path_sizes(all_lines)

        # for dir in dir_sizes:
        #     if dir_sizes[dir] <= 100000:
        #         total_sizes += dir_sizes[dir]

        if not part2:
            # Part 1
            for path in path_sizes:
                if path_sizes[path] <= 100000:  # Part 1
                    total_size += path_sizes[path]
        else:
            # Part 2
            space_needed = 30000000 - (70000000 - path_sizes[("/",)])
            # make list of path sizes sufficiently large
            total_size = min([y for x, y in path_sizes.items() if y >= space_needed])
    return total_size
