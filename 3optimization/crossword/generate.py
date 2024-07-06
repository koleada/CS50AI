import sys
from collections import Counter
from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            self.domains[var] = [
                word for word in self.domains[var] if len(word) == var.length
            ]

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False
        ## ************** NOT 100% SURE THIS RETURNS AN INDEX - IF HAVING ISSUES TRY TO SUBTRACT 1 FROM EACH OF THE VARS ************************
        x_int, y_int = self.crossword.overlaps(x, y)

        if x_int == None:
            return False

        for v in self.domains[x]:
            char = v[x_int]
            found = False
            for v_y in self.domains[y]:
                if v_y[y_int] == char:
                    found = True
                    break
            if found == False:
                self.domains[x].remove(v)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        real_arcs = []
        if arcs is not None:
            # arcs = list of tuples
            real_arcs = arcs
        else:
            for var in self.crossword.variables:
                # get all neighbors
                neighbors = Crossword.neighbors(var)
                for neighbor in neighbors:
                    # create list of tuples
                    real_arcs.append((var, neighbor))
        while len(real_arcs) != 0:
            x, y = real_arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbors in Crossword.neighbors(x):
                    real_arcs.append(x, neighbor)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.crossword.variables) != len(assignment):
            return False
        for var in assignment:
            # not sure what will be stored here if there is no value - could be empty string or None
            if len(assignment[var]) == 0 or assignment[var] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # basically counts all appearances of the values in assignment dict
        counts = Counter(assignment.values())
        for count in counts:
            # if any  elem appears more then once return False
            if count > 1:
                return False

        # checks for proper length of key+value
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        # NEED TO IMPLEMENT CHECK FOR CONFLICTS BETWEEN NEIGHBORS - seems like this is going to be very similar to AC3/revise but not modify anything
        arcs = []
        for var in assignment:
            neighbors = Crossword.neighbors(var)
            for neighbor in neighbors:
                arcs.append((var, neighbor))
        for arc in arcs:
            # if revised return False
            if self.revise(arc):
                return False

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = Crossword.neighbors(var)
        # remove any neighbors that are already assigned
        for neighbor in neighbors:
            if (
                neighbor in assignment
                and assignment[neighbor] != None
                and len(assignment[neighbor]) != 0
            ):
                neighbors.remove(neighbor)

        sorted_values = {}
        for val in self.domains[var]:
            count = 0
            for neighbor in neighbors:
                x, y = self.crossword.overlaps(var, neighbor)
                val_char = val[x]
                for value in self.domains[neighbor]:
                    # checks for bad overlap
                    if value[y] != val_char:
                        count += 1
                    # checks for dups
                    elif val == value:
                        count += 1
            sorted_values[count] = val
        return dict(sorted(sorted_values.items()))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        max = 0
        min_var = None
        for var in self.crossword.variables:
            if (
                var in assignment
                and assignment[var] != None
                and len(assignment[var]) != 0
            ):
                pass
            else:

                if len(self.domains[var]) > max:
                    max = len(self.domains[var])
                    min_var = var
                elif len(self.domains[var]) == max:
                    if len(Crossword.neighbors(var)) > len(
                        Crossword.neighbors(min_var)
                    ):
                        min_var = var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
