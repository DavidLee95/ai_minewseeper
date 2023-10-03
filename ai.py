# Class to store the safes, mines, and checked cells
class Known_cells:
    def __init__(self):
        # Contains (x, y) coordinates of known mines
        self.mines = set()
        # Contains (x, y) coordinates of known safe cells   
        self.safes = set()
        # Contains (x, y) coordinates of checked cells    
        self.checked = set()  
    # Add cells to the mines set
    def add_mine(self, cell):
        self.mines.add(cell)
    # Add cells to the safe set
    def add_safe(self, cell):
        self.safes.add(cell)
    # Add cells to the checked set
    def add_checked(self, cell):
        self.checked.add(cell)

# Class to create a new knowledge everytime that a cell is selected by the AI        
class KnowledgeBase:
    def __init__(self, adjacent_cells, count):
        self.adjacent_cells = set(adjacent_cells)
        self.count = count
    # Remove cells from the adjacent_cells set
    def remove_cell(self, cell):
        if cell in self.adjacent_cells:
            self.adjacent_cells.remove(cell)
    # Reduce the count by one
    def reduce_count(self):
        if self.count > 0:
            self.count -= 1
