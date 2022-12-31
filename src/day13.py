# Day #13: Distress Signal
# Part 1: How many pairs of packets are in the right order?
# Part 2: Insert the divider packets [2] & [6];
#   sort all packets; soln is product of the divider indeces
# I got lost in the logic here, so I copied a couple of solutions from reddit
#   as a learning experience; some modifications were made to fit our TDD structure

# __________ reddit solution #1: recursive solution by aaegic ___________

# Part #1...

from itertools import zip_longest


def compare_part1(l, r) -> bool:

    for ll, rr in zip_longest(l, r, fillvalue=None):
        if ll == None:  # left ran out of items (a base case)
            return True
        if rr == None:  # right ran out of items (a base case)
            return False

        if isinstance(ll, int) and isinstance(rr, int):
            if ll > rr:
                return False
            if ll < rr:  # the lower integer should come first (base cases)
                return True
            # integers are equal; loop to the next item
        else:
            # elevate single integers to a list, then compare the sublists (recursive case)
            if isinstance(rr, int):
                rr = [rr]
            if isinstance(ll, int):
                ll = [ll]

            ret = compare_part1(ll, rr)
            if ret in [True, False]:
                return ret
            # otherwise, integers in sublists are equal; loop to the next item


def solve_part1_compare(signals_file):
    itxt = open(signals_file, mode="r").read().split("\n\n")
    itxt = [i.splitlines() for i in itxt]
    # eval() will parse the string, then complile and evaluate it as an expression (typical Python overkill?)
    pkts = [eval(j) for i in itxt for j in i]
    # nest the lines into a list of pairs
    pkts = [[list(pl), list(pr)] for pl, pr in zip(pkts[0::2], pkts[1::2])]

    # feed each pair of lists into the compare function; start enumerate index at 1
    out = [i for i, p in enumerate(pkts, 1) if compare_part1(*p) == True]
    # Part 1 solution: sum of 1-based pair indeces
    return sum(out)


# Part #2...

# from itertools import zip_longest


def compare_part2(l, r) -> bool:
    for ll, rr in zip_longest(l, r, fillvalue=None):
        if ll == None:
            return True
        if rr == None:
            return False

        if isinstance(ll, int) and isinstance(rr, int):
            if ll > rr:
                return False
            if ll < rr:
                return True
        else:
            if isinstance(rr, int):
                rr = [rr]
            if isinstance(ll, int):
                ll = [ll]

            ret = compare_part2(ll, rr)
            if ret in [True, False]:
                return ret


def solve_part2_compare(signals_file):
    itxt = open(signals_file, mode="r").read().split("\n\n")
    itxt = [i.splitlines() for i in itxt]
    pkts = [eval(j) for i in itxt for j in i] + [[[2]], [[6]]]

    while True:  # .oO(...)
        for i in range(len(pkts) - 1):
            if compare_part2(pkts[i], pkts[i + 1]) == False:
                pkts[i], pkts[i + 1] = pkts[i + 1], pkts[i]
                done = False

        if done == True:
            break
        done = True

    ret = (pkts.index([[2]]) + 1) * (pkts.index([[6]]) + 1)
    return ret


# __________ reddit solution #2: flatten/sort solution by OilAppropriate2827 ___________
# To be original, I wanted to rely on standard sorting, do I decided to flatten the lists...

maxval, maxdepth = 100, 100
# maxval used to simplify flatten nested lists by elevating the values recursively
# maxdepth used to fill empty list with a big negative number


def flatten(l):
    # base case: item is a single integer or empty list
    if isinstance(l, int):
        return [l]
    if len(l) == 0:
        return [-maxdepth]
    # recursive case: item is a sublist
    return [
        l2 + (l2 < 0, maxval + maxdepth)[i > 0]
        for l1 in l
        for i, l2 in enumerate(flatten(l1))
    ]


def get_data(signals_file):
    # had to recreate this myself
    # itxt = open(signals_file, mode="r").read().split("\n\n")
    return open(signals_file, mode="r").read()  # don't split yet


def solve_part1_flatten(signals_file):
    data = [flatten(eval(p)) for p in get_data(signals_file).split("\n") if len(p)]

    ret = sum((data[i * 2] <= data[i * 2 + 1]) * (i + 1) for i in range(len(data) // 2))
    return ret


def solve_part2_flatten(signals_file):
    data = [flatten(eval(p)) for p in get_data(signals_file).split("\n") if len(p)]
    data += [[2], [6]]
    data.sort()

    ret = (data.index([2]) + 1) * (data.index([6]) + 1)
    return ret
