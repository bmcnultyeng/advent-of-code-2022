# Day #11: Monkey in the Middle

# Part 1: track the effect of monkey actions on item worry levels
#  solution: monkey-business = product of the total inspections
#  by 2 most active monkeys after 20 rounds
# Part 2: worry level is no longer reduced by 3 after each inspection
#  items (worry level values) become very large numbers
#    ? reduce value if all divisors are factors
#
#  solution: monkey_business after 10_000 rounds


class Monkees:
    # loads initial data; simulates monkey actions; tracks item worry levels
    def __init__(self, monkey_file=""):
        # read & parse all lines of data file (monkey rules & starting items) as list as of lists

        # index is monkey number in each list
        self.rules = []  # operation-on-old, test-divisor, true-throw, false-throw
        self.items = []  # item-worry-levels for each monkey
        # product of all test divisors, to reduce items (Part 2)
        #   only need LCM (least common multiple) but assume all are unique primes
        self.divisors_combined = 1
        self.inspections = []  # total inpection count for each monkey

        if len(monkey_file) != 0:
            # read & parse all lines of input file
            with open(monkey_file, "r") as mfile:
                for line in mfile:
                    if len(line.strip()) != 0:  # skip blank lines
                        match line.split()[0]:
                            case "Monkey":
                                self.inspections.append(0)
                            case "Starting":  # add a list of items for this monkey
                                worry_list = []
                                for num_comma in line.split()[2:]:
                                    worry_list.append(int(num_comma.strip(",")))
                                self.items.append(worry_list)  # used in Part 1
                            case "Operation:":  # start a list of rules for this monkey
                                # will exec() the statement
                                self.rules.append([line[19:].strip()])
                            case "Test:":  # add a divisor for this monkey's test rule
                                divisor = int(line.split()[-1])
                                self.rules[-1].append(divisor)
                                self.divisors_combined *= divisor
                            case "If":  # add 2 throw-to rules for this monkey
                                match line.split()[1]:
                                    case "true:":
                                        self.rules[-1].append(int(line.split()[-1]))
                                    case "false:":
                                        self.rules[-1].append(int(line.split()[-1]))
        else:  # for debug using dummy data_lines
            pass
        return

    def monkey_turn(self, monk_num, part2=False):
        """update inspection counts, worry levels & throws"""
        for i, old in enumerate(self.items[monk_num]):

            # inspect
            self.inspections[monk_num] += 1

            # apply opeeraation; adjust worry level
            if not part2:
                # Part 1: apply operation (example: 'old + 2') and int-divide by 3
                self.items[monk_num][i] = eval(self.rules[monk_num][0]) // 3
            else:
                # Part 2: do not divide by 3; to prevent overrun,
                #   after operation, reduce to modulo of LCM of all test divisors
                self.items[monk_num][i] = eval(self.rules[monk_num][0])
                self.items[monk_num][i] %= self.divisors_combined

            # apply test & throw to another monkey
            if (
                self.items[monk_num][i] % self.rules[monk_num][1]
            ) == 0:  # divisible by test-value?
                self.items[self.rules[monk_num][2]].append(self.items[monk_num][i])
            else:
                self.items[self.rules[monk_num][3]].append(self.items[monk_num][i])

        self.items[monk_num] = []  # monkey threw all items during it's turn
        return

    def do_rounds(self, round_count=20, part2=False):
        """simulate rounds of turns for each monkey;
        determine two most active monkeys;
        20 rounds for Part 1; 10_000 rounds for Part 2"""
        for round in range(round_count):
            for monkey_num in range(len(self.inspections)):
                self.monkey_turn(monkey_num, part2)

        monkey_business = sorted(self.inspections)[-2] * sorted(self.inspections)[-1]
        return monkey_business
