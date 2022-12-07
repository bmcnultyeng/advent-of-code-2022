# Day #6: Tuning Trouble

# Part 1: start-of-packet - find first 4-character sequence of non-repeated characters
# Part 2: start-of-message - find first 14-character sequence of non-repeated characters


def find_unique_sequence(
    buffer, char=4
):  # 4 distinct characters for Part 1; 14 for Part 2
    position = -1  # not found
    for i in range(len(buffer) - (char - 1)):
        if len(set(buffer[i : i + char])) == char:
            position = i + char
            break

    return position


def process_buffers(buffer_file, char=4):  # Part 1
    # read the buffer string
    # for each 4-character window (Part 1):
    #   test until finding 4 unique characters
    # return position of the end of the unique 4-character sequence
    # Part 2 wants 14 unique characters instead of 4
    positions = []  # process multiple lines from test data
    with open(buffer_file, "r") as bfile:
        for line in bfile:
            if len(line.strip()) > 0:  # skip blank line
                positions.append(find_unique_sequence(line.strip(), char))

    return positions
