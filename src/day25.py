# Day 25: Full of Hot Air
# Part 1: You need the sum of a list of fuel requirements for the
#   hot air balloons, to be processed through the fuel heating machine.
#   Instead of using digits four through zero,
#   the digits are 2, 1, 0, minus (written -), and double-minus
#   (written =). Minus is worth -1, and double-minus is worth -2.
#   A balanced quinary numeral system.
#   What total number (in SNAFU format) do you supply to Bob's console?
# Part 1 plan...
# 1) read SNAFU (base 5) numbers from console file
# 2) implement a special __add__ method in the snafu number system;
#      conversion to/from decimal system not needed;
#      had to handle up to two carry digits!
# 3) calc the total of the snafu values from the input files

# see also an alternate solution, using only iteration;
#   a good demo of itertools.accumulate(), itertools.zip_longest(),
#   divmod() & lambda

# Part 2: a free star, if you have earned all previous stars


class SnafuNumber:
    def __init__(self, snafu_string: str) -> None:
        self.s_string = snafu_string
        # lookup table for addition of snafu digits: tuple of (carry,sum)
        # snafu digits are:  = (-2),  - (-1),  0,  1,  2
        self.add_table = {
            "=": {
                "=": ("-", "1"),
                "-": ("-", "2"),
                "0": ("0", "="),
                "1": ("0", "-"),
                "2": ("0", "0"),
            },
            "-": {
                "=": ("-", "2"),
                "-": ("0", "="),
                "0": ("0", "-"),
                "1": ("0", "0"),
                "2": ("0", "1"),
            },
            "0": {
                "=": ("0", "="),
                "-": ("0", "-"),
                "0": ("0", "0"),
                "1": ("0", "1"),
                "2": ("0", "2"),
            },
            "1": {
                "=": ("0", "-"),
                "-": ("0", "0"),
                "0": ("0", "1"),
                "1": ("0", "2"),
                "2": ("1", "="),
            },
            "2": {
                "=": ("0", "0"),
                "-": ("0", "1"),
                "0": ("0", "2"),
                "1": ("1", "="),
                "2": ("1", "-"),
            },
        }

    def __add__(self, other: str) -> str:
        """sum of two snafu strings, as a snafu string"""
        # no conversion to decimals needed !
        sss = self.s_string[::-1]
        ooo = other[::-1]
        pad_length = max(len(sss), len(ooo)) + 1
        # append zeros for equal length and extra carry digit

        sss += "0" * (pad_length - len(sss))
        ooo += "0" * (pad_length - len(ooo))
        total = ""
        carry = "0"

        for i, sd1 in enumerate(sss):
            carry, place_total = self._add_position(sd1, ooo[i], carry)
            total = place_total + total

        if total[0] == "0":  # strip leading zero
            total = total[1:]
        return total

    def _add_position(self, sd1: str, sd2: str, carry_previous):
        """add two snafu digits & a carry digit"""
        carry_next, subtotal = self.add_table[sd1][sd2]
        carry_extra, total = self.add_table[subtotal][carry_previous]
        if carry_extra != "0":
            carry_never, carry_next = self.add_table[carry_extra][
                carry_next
            ]  # never a third carry here ?
        return (carry_next, total)


def sum_part1(snafu_list) -> str:
    """sum of a list of snafu strings, in snafu format"""
    total = snafu_list[0]
    for sn in snafu_list[1:]:
        total = SnafuNumber(total) + sn
    return total


def get_input(snafu_file):
    """read & parse fuel requirements into a SnafuNumber list"""
    snafu_input = []
    with open(snafu_file, "r") as sfile:
        for line in sfile:
            if len(line.strip()) != 0:  # skip blank lines
                # read file as a list of strings
                snafu_input.append(line.strip())
    return snafu_input


# a much better solution from reddit by hugues_hoppe
#   "Addition in the SNAFU algebra, using only Python iterators"

# the asterisk is used here to unpack the generator function; the
#   list is unpacked into separate positional arguments.
# see my deconstruction of the day25 function into more verbose functions below...
import itertools


def day25(s):
    it = itertools.accumulate(
        itertools.zip_longest(
            *(line[::-1] for line in s.splitlines()), "0" * 20, fillvalue="0"
        ),
        lambda state, t: divmod(
            state[0] + sum("=-012".index(ch) - 2 for ch in t) + 2, 5
        ),
        initial=(0, 0),
    )

    # return "".join("=-012"[mod] for _, mod in it)[:0:-1].lstrip("0")
    result = "".join("=-012"[mod] for _, mod in it)[:0:-1].lstrip("0")
    return result


# ****** my deconstruction of the day25 function into more verbose functions below... ******


def day25_deconstructed(snafu_file_name):
    # read file into a single string
    with open(snafu_file_name, "r") as s_file:
        s = s_file.read()

    # parse each line in reverse order, filled to length 20 with zeros
    # s_zipped generates 20 lists of the snafu digits, one list for each position
    s_zipped = itertools.zip_longest(
        *(line[::-1] for line in s.splitlines()), "0" * 20, fillvalue="0"
    )

    # the first argument of itertools.accumulate() is an iterable such as a list or *(generator).
    # the optional second 'func' argument of itertools.accumulate() is a running function that
    #   operates on the iterable;  'func' can be simple, like max, or a lambda function;
    #   'func' should accept two arguments, the current and previous values from the interable.

    # divmod(a,b) of two integers returns tuple(a/b, a%b) integer quotient and integer remainder;
    #   if either is float, returns whole decimal quotient and decimal remainder

    # lambda state, t: divmod(state[0] + sum("=-012".index(ch) - 2 for ch in t) + 2, 5)
    #   input: a tuple of two ints (the previous 'state') & a sequence of integers;
    #      'state' is the tuble pair result from the previous divmod calculation
    #      't' is generated by the iterable in the first argument of iter.accum()
    #   calculations:  divmod by 5 of (the previous quotient + total of digits in this position)
    #   output: quotient and remainder from divmod, as a tuple of two ints (the current 'state');
    #       the quotient is the carry for the next higher digit position and the
    #       remainder is the base-5 unbalanced value of the digit for the current position
    lambda_func = lambda state, t: divmod(
        state[0] + sum("=-012".index(ch) - 2 for ch in t) + 2, 5
    )

    # initial=(0,0)  # initial output value of itertools.accumulate(), before applying 'func';
    #   also used as initial input value 'state' into 'func'

    it = itertools.accumulate(
        s_zipped,
        lambda_func,
        initial=(0, 0),
    )
    # 'it' represents a sequence of 'state' tuple pairs for each (reversed) digit position,
    #   like [(0, 0), (2, 2), (3, 0), (0, 3), (1, 1), (1, 0), (0, 4), ...]
    #

    # convert the divmod remainder values 'mod' from unbalanced base-5 integers
    #   into digits in snafu format, using an index lookup
    result = "".join("=-012"[mod] for _, mod in it)[:0:-1].lstrip("0")
    return result
