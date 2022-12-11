# Day #8: Treetop Tree House

# Part 1: find number of trees visible from left, right, above or below;
#   blocked by height greater than or equal
# Part 2: find tree w highest scenic-score, the
#   product of unblocked viewing distances in all 4 directions

# read all lines of data file (rows of trees) as nested list of integers & create Forest instance
#   use a list of [height,visible] tuples to represent the searchable forest
# for each line (while result of current tree is visible (either LR or AB are True):
#   if a top or bottom row, all are always visible
#   first (leftmost) & last (rightmost) are always visible
#   compare the height of the current tree to the other trees in the same row: visible = True
#   if not visible, compare the current tree to the other trees in the same column: visible = True


class Forest:
    # a nested list of list represents the trees in the forest
    #   each tree: [tree-height, visible-from-one-edge, scenic-score]
    def __init__(self, trees_file="") -> None:
        # read all lines of data file (rows of trees) as nested list of integers & create Forest instance
        self.trees = []
        self.extent = 0
        self.visible_count = 0
        highest_scenic_score = 0

        if len(trees_file) != 0:
            with open(trees_file, "r") as tfile:
                all_lines = []
                for line in tfile:
                    if len(all_lines) == 0:
                        all_lines = [line.strip()]
                    else:
                        if len(line.strip()) != 0:
                            all_lines.append(line.strip())
                self.build_trees_structure(all_lines)

        else:  # for debug using dummy data_lines
            pass

        return

    def build_trees_structure(self, data_lines):
        self.extent = len(
            data_lines[0]
        )  # original size of forest; assume square data grid

        # top row always visible
        # initial scenic-score=0; will remain 0 on edges
        row = [[int(x), True, 0] for x in data_lines[0]]
        self.trees = [row]

        # build remaining rows
        for r in range(1, self.extent - 1):
            # leftmost & rightmost columns always visible
            row = (
                [[int(data_lines[r][0]), True, 0]]
                + [[int(x), False, 0] for x in data_lines[r][1:-1]]
                + [[int(data_lines[r][-1]), True, 0]]
            )
            self.trees.append(row)

        # bottom row always visible
        row = [[int(x), True, 0] for x in data_lines[-1]]
        self.trees.append(row)
        return

    def is_visible(self, row, colm):
        # True if tree at position (row,colm) is higher than
        #   trees to left, right, above or below
        visible = False  # visible from left, right, above or below
        height = self.trees[row][colm][0]

        # search for same or higher trees to the left in same row
        if len([tree[0] for tree in self.trees[row][:colm] if tree[0] >= height]) == 0:
            visible = True
        else:
            # search for same or higher trees to the right
            if (
                len(
                    [
                        tree[0]
                        for tree in self.trees[row][colm + 1 :]
                        if tree[0] >= height
                    ]
                )
            ) == 0:
                visible = True

        # search for same or higher trees above in same column
        if not visible:
            if len([r[colm][0] for r in self.trees[:row] if r[colm][0] >= height]) == 0:
                visible = True
            else:
                # search for same or higher trees below
                if (
                    len(
                        [
                            r[colm][0]
                            for r in self.trees[row + 1 :]
                            if r[colm][0] >= height
                        ]
                    )
                    == 0
                ):
                    visible = True

        return visible

    def find_visible_trees(self):
        # all trees in first/last row/column are always fully visible
        # update the visible status of all trees not in first/last row/column
        # for rows 2nd from top to 2nd from bottom:
        for r in range(1, self.extent - 1):
            #   for cols 2nd from left to 2nd from right:
            for i in range(1, self.extent - 1):
                self.trees[r][i][1] = self.is_visible(r, i)
        self.visible_count = sum(
            1 for row in self.trees for tree in row if tree[1]
        )  # TODO could have a running total in tag_visible_trees() instead; incl. edges
        return self.visible_count

    def calc_scenic_score(self, row, colm):
        # count the viewing_distance : stop if you reach an edge or
        #   at the first tree that is the same height or taller
        # scenic-score is the product of viewing_distance in all 4 directons

        height = self.trees[row][colm][0]

        # search left from current tree until edge, same height or taller
        viewing_distance = 0
        for i in range(colm - 1, -1, -1):
            viewing_distance += 1  # can see this tree
            if self.trees[row][i][0] >= height:
                break  # next tree is blocked
        scenic_score = viewing_distance

        # search right...
        viewing_distance = 0
        for i in range(colm + 1, self.extent):
            viewing_distance += 1  # can see this tree
            if self.trees[row][i][0] >= height:
                break  # next tree is blocked
        scenic_score *= viewing_distance

        # search up from current tree until edge, same height or taller
        viewing_distance = 0  # can always see 1st tree
        for i in range(row - 1, -1, -1):
            viewing_distance += 1  # can see this tree
            if self.trees[i][colm][0] >= height:
                break  # next tree is blocked
        scenic_score *= viewing_distance

        # search down...
        viewing_distance = 0
        for i in range(row + 1, self.extent):
            viewing_distance += 1  # can see this tree
            if self.trees[i][colm][0] >= height:
                break  # next tree is blocked
        scenic_score *= viewing_distance

        return scenic_score

    def find_highest_scenic_score(self):
        # update the scenic-score of all trees not in first/last row/column
        # for rows 2nd from top to 2nd from bottom:
        for r in range(1, self.extent - 1):
            #   for cols 2nd from left to 2nd from right:
            for i in range(1, self.extent - 1):
                self.trees[r][i][2] = self.calc_scenic_score(r, i)
        self.highest_scenic_score = max(
            tree[2] for row in self.trees for tree in row if tree[2]
        )  # TODO could have a running max in calc_scenic_score() instead; incl. edges
        return self.highest_scenic_score
