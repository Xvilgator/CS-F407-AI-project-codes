import random

# Check if a value can be placed in a cell without violating the Sudoku rules
def is_valid(grid, row, col, value):
    # Check if the value already appears in the same row or column
    for i in range(9):
        if grid[row][i] == value:
            return False
        if grid[i][col] == value:
            return False
    # Check if the value already appears in the same 3x3 sub-grid
    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if grid[i][j] == value:
                return False
    return True

# Generate a valid Sudoku grid with the given number of hints
def generate_grid(num_hints):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(num_hints):
        # Choose a random cell
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        # Choose a random value for the cell that is consistent with the Sudoku rules
        value = random.randint(1, 9)
        while not is_valid(grid, row, col, value):
            value = random.randint(1, 9)
        # Set the value in the grid
        grid[row][col] = value
    return grid
    

box = generate_grid(45)
print(box)

# Count the number of conflicts in the Sudoku grid
def count_conflicts(grid, row=None, col=None, value=None):
    conflicts = 0
    if row is not None and col is not None and value is not None:
        # Count the conflicts for the given cell and value
        for i in range(9):
            if grid[row][i] == value:
                conflicts += 1
            if grid[i][col] == value:
                conflicts += 1
        subgrid_row = (row // 3) * 3
        subgrid_col = (col // 3) * 3
        for i in range(subgrid_row, subgrid_row + 3):
            for j in range(subgrid_col, subgrid_col + 3):
                if grid[i][j] == value:
                    conflicts += 1
    else:
        # Count the conflicts for the entire grid
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    continue
                conflicts += count_conflicts(grid, row, col, grid[row][col]) - 3
    return conflicts

# Get the best value to place in a given cell to reduce the number of conflicts
def get_best_value(grid, row, col):
    best_value = grid[row][col]
    best_conflicts = count_conflicts(grid)
    for value in range(1, 10):
        grid[row][col] = value
        conflicts = count_conflicts(grid)
        if conflicts < best_conflicts:
            best_value = value
            best_conflicts = conflicts
    grid[row][col] = best_value
    return best_value

# Hill Climbing Local Search algorithm to solve a Sudoku puzzle
def hill_climbing(grid):
    # Keep track of the best grid and its number of conflicts seen so far
    best_grid = [row[:] for row in grid]
    best_conflicts = count_conflicts(grid)
    
    # Continue until the solution is found or a maximum number of iterations is reached
    max_iterations = 1000
    num_iterations = 0
    while True:
        # Choose a random cell to modify
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        # Get the best value to place in the cell to reduce the number of conflicts
        value = get_best_value(grid, row, col)
        # If the best value is already in the cell, skip this iteration
        if value == grid[row][col]:
            continue
        # Update the grid with the best value
        grid[row][col] = value
        # Count the number of conflicts in the new grid
        conflicts = count_conflicts(grid)
        # If the new grid has fewer conflicts than the previous best grid, update the best grid
        if conflicts < best_conflicts:
            best_grid = [row[:] for row in grid]
            best_conflicts = conflicts
        # If the number of iterations exceeds the maximum, stop and return the best grid found so far
        num_iterations += 1
        if num_iterations >= max_iterations:
            return best_grid

hill_climbing(box)
print(box)
