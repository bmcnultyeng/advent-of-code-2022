# Day #10: Cathode-Ray Tube

# Part 1: track the effect of noop & addx commands on register X;
#  solution: value (signal strenth) in register X at specific cycles
# Part 2: register-X is the position of (the center of) a 3-pixel sprite
#     on a 240-pixel (40 wide by 6 high) screen
#  the CRT draws one pixel (lit or dark) st each cycle
#  a pixel is drawn as lit if within the 3-pixel sprite, otherwise drawn as dark
#  solution: what eight capital letters appear on the CRT screen after one 240-cycle scan?

# read all lines of data (CPU commands) as a nested list of string-integer pairs (command, value-V)
# track the effect on register x's value at the end of each cycle
#  'noop' command consumes one cycle and has no effect on register X
#  'addx V' command increases X-value by V (can be <0);
#     the changes to the X-value take effect at the end of the two cycles
#     X-value = 1 at start of & during the 1st cycle;
#       X-value reflects the  effect of the 1st command at end of 1st cycle
# Part 1 solution: sum of signal-strength DURING 20th & every 40 cycles after
#  signal-strength = X-values times cycle-number
# create a simple Computer class with register-X, command list & execute-command function


class Computer:
    # handles register-X value, command list & execute-command function
    def __init__(self, program_file=""):
        # read & parse all lines of data file (cpu commands) list as of tuples

        self.reg_x = 1  # current X-value in register X
        # self.reg_x_log = [1]  # for debug
        self.cycle_num = 0
        self.signal_strengths_part1 = {
            20: 0,
            60: 0,
            100: 0,
            140: 0,
            180: 0,
            220: 0,
        }  # during 20th, 60th, 100th, 140th, 180th & 220th cycles

        self.pixels = ""  # 240 char string: "#" (lit) or "." (dark)

        self.commands = []
        if len(program_file) != 0:
            # read & parse all lines of input file
            with open(program_file, "r") as pfile:
                for line in pfile:
                    cmd = line[:4]
                    val = line[5:]
                    if len(self.commands) == 0:
                        if cmd == "noop":
                            self.commands = [("noop", 0)]  # 0 value ignored
                        elif cmd == "addx":  # skip empty lines
                            self.commands = [("addx", int(val))]
                    else:
                        if cmd == "noop":
                            self.commands.append(("noop", 0))
                        elif cmd == "addx":  # skip empty lines
                            self.commands.append(("addx", int(val)))
        else:  # for debug using dummy data_lines
            pass
        return

    def update_signal_strengths(self):  # Part 1
        if self.cycle_num in self.signal_strengths_part1:
            self.signal_strengths_part1[self.cycle_num] = self.cycle_num * self.reg_x
        return

    def draw_pixel(self):  # Part 2
        # the 3-wide sprite  covers all vertical rows; use modulo/remainder
        if (self.cycle_num % 40) - 1 in [self.reg_x - 1, self.reg_x, self.reg_x + 1]:
            self.pixels += "##"  # draw a lit pixel "#" if 3-pixel sprite is visible; "##" for readability
        else:
            self.pixels += "  "  # draw a dark pixel "."; "  " for readability
        if self.cycle_num % 40 == 0:
            self.pixels += "\n"  # for readability 6 rows x 40 pixels
        return

    def execute_command(self, cmd, part2=False):
        # increment cycles & adjust X-value based on the current command
        # update signal-strength list when needed

        # 1st cycle of "noop" or "addx V" command
        self.cycle_num += 1
        if not part2:  # Part 1
            self.update_signal_strengths()
        else:  # Part 2
            self.draw_pixel()
        # self.reg_x_log.append(self.reg_x)  # for debug

        if cmd[0] == "addx":  # 2nd cycle for "addx V" command
            self.cycle_num += 1
            if not part2:  # Part 1
                self.update_signal_strengths()
            else:  # Part 2
                self.draw_pixel()
            self.reg_x += cmd[1]  # update X-value after both cycles
            # self.reg_x_log.append(self.reg_x)  # for debug

        return

    def run_program(self, part2=False):
        # execute all commands from the program input file

        if not part2:  # Part #1
            for cmd in self.commands:
                self.execute_command(cmd)
            # Part #1 answer
            return sum([v for v in self.signal_strengths_part1.values()])

        else:  # Part #2
            for cmd in self.commands:
                self.execute_command(cmd, part2=True)
            # Part #2 answer: must view pixels in 6 rows of 40
            return self.pixels
