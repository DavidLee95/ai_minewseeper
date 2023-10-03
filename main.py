import pygame
import sys
import random
import functions as fn
import ai
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_SIZE = 10
CELL_SIZE = (SCREEN_WIDTH - 160) // (GRID_SIZE)
MINE_COUNT = 10
MINE_IMAGE = pygame.transform.scale(pygame.image.load('images/mine.png'), (50,50))
FLAG_IMAGE = pygame.transform.scale(pygame.image.load('images/flag.png'), (50,50))

# Colors
BG_COLOR = (51, 255, 153)
GRID_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 255, 255)
MINE_COLOR = (255, 0, 0)
BUTTON_COLOR = (255, 255, 255)
BUTTON_TEXT_COLOR = (0, 0, 0)
TITLE_TEXT_COLOR = (0, 0, 0)
TITLE_TEXT_BG = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")

# Function to create a nested array to represent the game board
def create_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to place mines randomly on the grid
def place_mines(grid, count):
    mines_placed = 0
    while mines_placed < count:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == 0:
            grid[x][y] = 100    
            mines_placed += 1

# Funciton to write title on the top middle
def write_title(text):
    # Create a background rectangle
    title_background = pygame.Rect(
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT * 0.06,
        )
    pygame.draw.rect(screen, TITLE_TEXT_BG, title_background)
    font = pygame.font.Font(None, 50)
    text = font.render(text, True, TITLE_TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 675))
    screen.blit(text, text_rect)

# Function to draw the button to play the game on the bottom middle 
def draw_buton(text):
    # Create a background rectangle
    button_rect = pygame.Rect(
        SCREEN_WIDTH * 0.25,
        SCREEN_HEIGHT * 0.91,
        SCREEN_WIDTH * 0.5,
        SCREEN_HEIGHT * 0.07,
    )

    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 36)
    button_text = font.render(text, True, BUTTON_TEXT_COLOR)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)  

# Function to draw the game board
def draw_board(board):
    for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(
                    x * CELL_SIZE + 80,
                    y * CELL_SIZE + 70,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1,
                )
                # Show a black color on the cell that has not been clicked yet by the AI
                if board[x][y] == 0 or board[x][y] == 100:
                    pygame.draw.rect(screen, GRID_COLOR, rect)
                # Show a white color on the cell that has been clicked by the AI and is not a mine
                elif 0 < board[x][y] < 100:
                    pygame.draw.rect(screen, SELECTED_COLOR, rect)
                    font = pygame.font.Font(None, 36)
                    # If the cell has 0 surrounding mines show 0.
                    if board[x][y] == 10:
                        text = font.render(str(0), True, (0, 0, 0))
                    # If the cell has any surrounding mines show the count.
                    else:
                        text = font.render(str(board[x][y]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                # Show a mine on the cell that has been clicked by the AI and is a mine
                elif board[x][y] == 200:
                    pygame.draw.rect(screen, MINE_COLOR, rect)
                    screen.blit(MINE_IMAGE, (x * CELL_SIZE + 80, y * CELL_SIZE + 70))
                # Show a found mine by the AI and that has not been clicked yet
                elif board[x][y] == 300:
                    pygame.draw.rect(screen, SELECTED_COLOR, rect)
                    screen.blit(FLAG_IMAGE, (x * CELL_SIZE + 80, y * CELL_SIZE + 70))



# Check the knowledgebase to see if any mines or safes can be found
def check_knowledgebase(knowledgebase):
    mines = []
    safes = []
    for knowledge in knowledgebase:
        # Check for any known mines
        if len(knowledge.adjacent_cells) == knowledge.count:
            for cells in knowledge.adjacent_cells:
                mines.append(cells)
        # Check for any known safes
        elif knowledge.count == 0:
            for cells in knowledge.adjacent_cells:
                safes.append(cells)
    return(mines,safes)

# Remove safe cells from the knowledgebase
def remove_cell(knowledgebase, safe):
    for knowledge in knowledgebase:
        knowledge.remove_cell(safe)
    return knowledgebase

# Remove mines from the knowledgebase
def remove_mines(knowledgebase, mine):
    for knowledge in knowledgebase:
        # Reduce the knowledge cound by 1
        if mine in knowledge.adjacent_cells:
            knowledge.reduce_count()
        knowledge.remove_cell(mine)
    return knowledgebase

# Remove safes, checked, mines from the new knowledge before appending it to the knowledgebase
def update_knowledge(knowledge, safes, mines, checked):
    for item in knowledge.adjacent_cells.copy():
        if item in safes:
            knowledge.remove_cell(item)
        if item in checked:
            knowledge.remove_cell(item)
        if item in mines:
            knowledge.reduce_count()
            knowledge.remove_cell(item)

    return knowledge

# Main game loop
def main():

    #Initialize board and place mines
    board = create_board()
    place_mines(board, MINE_COUNT)

    # Initialize a variable to make known that the game has not yet begun
    game_on = False

    # Create an instance of the Categories class
    cell_categories = ai.Known_cells()

    # Create a list of the knowledge that will be used by the AI
    knowledgebase = []

    while True:

        # Main logic of the game
        if game_on:

            # Function to pick a safe cell that has not been picked yet
            if len(cell_categories.safes) > 0:
                cell, cell_categories.safes = fn.pick_safe(cell_categories.safes, cell_categories.checked)

            # Function to pick a random cell from the board that has not been picked yet and is not a known mine
            else:
                cell = fn.pick_random(board)
                
            # If the chosen cell is not a mine
            if board[cell[0]][cell[1]] == 0:
                # Check how many mines are surrounding the cell
                adjacent_cells,mines_count = fn.adjacent_mines(board, GRID_SIZE, cell[0], cell[1])

                # If the cell has 0 mines surrounding it mark it as a 10 on the board
                if mines_count == 0:
                    board[cell[0]][cell[1]] = 10
                # If the cell has mines surrounding it mark the number on the board
                else:
                    board[cell[0]][cell[1]] = mines_count
                
                # Add the cell to the checked set in cell_categories
                cell_categories.add_checked(cell)

                # Create a new knowledge with the adjacent cells and the mine count
                new_knowledge = ai.KnowledgeBase(adjacent_cells, mines_count)
                # Reduce the new knowledgebase by removing any known safes, mines, and checked cells
                new_knowledge = update_knowledge(new_knowledge, cell_categories.safes, cell_categories.mines, cell_categories.checked)
                # Add to the knowledgebase
                knowledgebase.append(new_knowledge)

                # Since the cell itself is safe, remove it from all the knowledgebase
                knowledgebase = remove_cell(knowledgebase, cell)
                
                # Check for any mines and safes that can be deduced in the knowledgebase with the updated knowledgebase
                found_mines, found_safes = check_knowledgebase(knowledgebase)

                # Remove any mines from the knowledgebase, reduce the count, and add the cell to the mines list
                if len(found_mines) > 0:
                    for item in found_mines:
                        knowledgebase = remove_mines(knowledgebase, item)
                        cell_categories.add_mine(item)
                        # Mark in the board as a deduced mine
                        board[item[0]][item[1]] = 300
                # Remove any safes from the knowledgebase and add the cell to the safes list
                if len(found_safes) > 0:
                    for item in found_safes:
                        knowledgebase = remove_cell(knowledgebase, item)
                        cell_categories.add_safe(item)
            
            # If the cell is a mine, mark is as 200 to represent that the cell is a mine and has been selected
            else:
                board[cell[0]][cell[1]] = 200
                game_on = False     
            
            # Give a delay of 0.2s to visualize the AI solving the puzzle
            time.sleep(0.2)
        
        # Quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Detect the user's mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get coordinate values
            x_coord = event.pos[0]
            y_coord = event.pos[1]
            # Initialize the game when the button is pressed
            if 175 < x_coord < 525 and 637 < y_coord < 686 and game_on == False:
                #Initialize board and place mines
                board = create_board()
                place_mines(board, MINE_COUNT)

                # Initialize a variable to make known that the game has not yet begun
                game_on = True

                # Create an instance of the Categories class
                cell_categories = ai.Known_cells()

                # Create a list of the knowledge that will be used by the AI
                knowledgebase = []


        # Clear the screen
        screen.fill(BG_COLOR)

        # Draw the grid
        draw_board(board)

        # Draw button before the game starts
        if not game_on and sum(row.count(100) for row in board) == 10:
            draw_buton("Solve the Puzzle With AI")
        # Write text after the AI loses
        if not game_on and sum(row.count(100) for row in board) < 10:
            draw_buton("Play again")

        # Title when the AI wins
        if sum(row.count(0) for row in board) == 0:
            write_title("THE AI WON!!!")
            game_on = False
        # Title when the AI loses
        elif sum(row.count(100) for row in board) + sum(row.count(300) for row in board) < 10:
            write_title("THE AI LOST :(")
        # Title when the game starts
        elif sum(row.count(100) for row in board) + sum(row.count(300) for row in board) == 10:
            write_title("AI MINESWEEPER")

        pygame.display.flip()

if __name__ == "__main__":
    main()
