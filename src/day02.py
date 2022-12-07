# Day 2: Rock Paper Scissors

# translate each round from the strategy guide into scores


def my_score(rounds_file, part=1):
    if part == 1:
        scores = {
            "A X": 4,
            "A Y": 8,
            "A Z": 3,
            "B X": 1,
            "B Y": 5,
            "B Z": 9,
            "C X": 7,
            "C Y": 2,
            "C Z": 6,
        }  # Part 1
    else:
        scores = {
            "A X": 3,
            "A Y": 4,
            "A Z": 8,
            "B X": 1,
            "B Y": 5,
            "B Z": 9,
            "C X": 2,
            "C Y": 6,
            "C Z": 7,
        }  # Part 2
    total_score = 0

    with open(rounds_file, "r") as rfile:
        for line in rfile:
            if line.strip() in scores:  # skip blank line
                total_score += scores[line.strip()]

    return total_score
