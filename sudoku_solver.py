from z3 import Solver, Int, And, Or, Distinct, If, sat

# Takes the user input and calls the Sudoku Solver
def main():

    # Create the puzzle from the input
    puzzle = []
    print("Enter the rows in order when asked. ")

    for i in range(9):
        input_string = list(input("Enter a row: "))

        # Split the input string into individual characters
        chars_row = list(input_string)

        # Convert each character to an integer
        int_row = []
        for char in chars_row:
            # Convert " " to 0s, to facilitate the SAT solver.
            if char == ' ':
                int_row.append(0)
            else:
                int_row.append(int(char))
        
        # Add int row ro puzzle
        puzzle.append(int_row)

    # ----------- VERIFICATION -------------
    # print(puzzle)

    # Solve Sudoku
    solved_puzzle = sudoku_solver(puzzle)
    if solved_puzzle is not None:
        for row in solved_puzzle:
            print(row)
    # UNSAT
    else:
        print("UNSAT Sudoku.")


# Sudoku Solver
def sudoku_solver(puzzle):

    # Create a Z3 solver instance
    solver = Solver()

    # Create a 9x9 grid of integer variables
    grid = [[Int("cell_%s_%s" % (i, j)) for j in range(9)] for i in range(9)]

    # Add constraints for each cell
    for i in range(9):
        for j in range(9):
            # Cell must contain a number from 1 to 9
            solver.add(grid[i][j] >= 1, grid[i][j] <= 9)

            # Add constraint for row and column uniqueness
            for k in range(9):
                if k != j:
                    solver.add(grid[i][j] != grid[i][k])
                if k != i:
                    solver.add(grid[i][j] != grid[k][j])

            # Add constraint for sub-grid uniqueness
            sub_i = (i // 3) * 3
            sub_j = (j // 3) * 3
            for m in range(sub_i, sub_i + 3):
                for n in range(sub_j, sub_j + 3):
                    if m != i and n != j:
                        solver.add(grid[i][j] != grid[m][n])

    # Add constraints for the initial puzzle values
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                solver.add(grid[i][j] == puzzle[i][j])

    # Check if the puzzle is Satisfiable
    if solver.check() == sat:
        # Get the solved values for each cell
        model = solver.model()
        solution = [[model.evaluate(grid[i][j]).as_long() for j in range(9)] for i in range(9)]
        return solution
    else:
        # UNSAT
        return None
    

if __name__ == "__main__":
    main()

