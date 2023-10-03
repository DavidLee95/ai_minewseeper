import random

# Function to count the number of adjacent mines
def adjacent_mines(board, GRID_SIZE, x, y):
    # Create a variable to keep track of the mine_count
    mine_count = 0
    # Create a list to store the adjacent_cells
    adjacent_cells = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # Only check mines that are not the checked mine, and are within 0 to 9 in both x and y
            if (x,y) != (x + i,y + j) and 0 <= x + i < GRID_SIZE and 0 <= y + j < GRID_SIZE:
                # Append to the adjacent_cells list every surrounding cell
                adjacent_cells.append((x + i, y + j))
                # If a cell is a known (represented by 300) or unknwon (represented by 100) mine, increase the mine count by 1
                if board[x + i][y + j] == 100 or board[x + i][y + j] == 300:
                    mine_count += 1
    return adjacent_cells, mine_count

# Function to pick a random cell from the board that has not been picked yet and that is not a known mine
def pick_random(board):
    while True:
        x = random.randint(0,9)
        y = random.randint(0,9)
        if board[x][y] == 0 or board[x][y] == 100:
            return((x,y))

# Function to pick a safe cell that has not been picked yet
def pick_safe(safes, checked):
    for cell in safes:
        if cell not in checked:
            # Remove the cell from the safes list
            safes.remove(cell)
            return(cell, safes)
    