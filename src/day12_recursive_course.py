houses = ["Eric's house", "Kenny's house", "Kyle's house"]


def deliver_presents_iteratively():
    for house in houses:
        print("Delivering presents to", house)


# Shift-Enter to run in Jupyter Interactive Terminal/REPL...
deliver_presents_iteratively()


def sum_recursive(current_number, accumulated_sum):
    """tutorial: maintaining state - thread the state;
    increment the number until number reaches 10"""
    # Note: The state that we have to maintain is
    #   (current number we are adding, accumulated sum till now)
    #  whether maintained as threaded or global
    # base case - return the final state
    if current_number == 11:
        return accumulated_sum
    # recursive case - thread the state through the recursive call
    else:
        return sum_recursive(current_number + 1, accumulated_sum + current_number)


""" global mutable state (not recommended!)"""
current_number = 1
accumulated_sum = 0


def sum_recursive():
    global current_number  # allows to access outside function's namespace
    global accumulated_sum
    # base case - return the final state
    if current_number == 11:
        return accumulated_sum
    # recursive case
    else:
        accumulated_sum += current_number
        current_number += 1
    return sum_recursive()


"""avoid slicing lists when recursive;
manipulate and pass the indexex instead of the list"""


def sum_lst(lst):
    print(lst)
    # base case
    if lst == []:
        return 0
    # recursive case
    else:
        # return sliced list to recursive case
        return lst[0] + sum_lst(lst[1:])


def sum_lst_noslice(lst):
    # recursive case
    print(lst)

    def helper(start_index):
        # note: lst is accessable from hekper();
        #   called 'enclosed' or 'nonlocal' scope
        #   more info about variable scope: LEGB Rule in Python
        #     Local > Enclosed > Global > Built-In
        #   [but mutable v immutable types get tricky?!]
        # base case
        if start_index == len(lst):
            return 0
        # recursive case
        else:
            print(lst, "  helper")
            return lst[start_index] + helper(start_index + 1)

    return helper(0)
