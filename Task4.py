def get_ship_positions(board_size, ship, cell, misses):
    feasible_positions = []
    x, y = cell

    # Check both original and rotated positions
    for shape in ship["shapes"]:
        ship_positions = [(x + dx, y + dy) for dx, dy in shape]
        if all(0 <= i < board_size and 0 <= j < board_size for i, j in ship_positions):
            # If the ship's position intersects with misses, discard this position
            if not set(ship_positions) & misses:
                feasible_positions.extend(ship_positions)

    return feasible_positions


def get_ship_configuration_count(board_size, ships, misses):
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    for ship in ships:
        for i in range(board_size):
            for j in range(board_size):
                positions = get_ship_positions(board_size, ship, (i, j), misses)
                for pos in positions:
                    # Increment the count for this cell
                    board[pos[0]][pos[1]] += 1

    return board


import random


# Function to get the cell with the highest configuration count
def get_highest_config_cell(board):
    max_config = max(max(row) for row in board)
    highest_config_cells = [(i, j) for i in range(len(board)) for j in range(len(board[i])) if
                            board[i][j] == max_config]

    # Sort the cells by their coordinates (first by row index, then by column index) and return the first cell
    highest_config_cells.sort()
    return highest_config_cells[0]  # Return the top leftmost cell


# Function to get the adjacent cells of a given cell
def get_adjacent_cells(cell):
    x, y = cell
    return [(nx, ny) for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
            0 <= nx < board_size and 0 <= ny < board_size]


# StrategyII-Hunt function
def StrategyII_Hunt(board):
    # Find and return the cell with the highest configuration count
    return get_highest_config_cell(board)


# StrategyII-Target function
def StrategyII_Target(board, h):
    # Get the list of adjacent cells
    adjacent_cells = get_adjacent_cells(h)
    # Select the adjacent cell with the highest configuration count
    max_config = max(board[i][j] for i, j in adjacent_cells)
    highest_config_adj_cells = [(i, j) for i, j in adjacent_cells if board[i][j] == max_config]
    return random.choice(
        highest_config_adj_cells)  # Return a random cell if there are multiple cells with the highest count


board_size = 6
misses = {(0, 0), (3, 2), (0, 5), (5, 5)}  # Misses on the board
hits = [(5, 0), (5, 1)]

# Define the ships and their shapes in both horizontal and vertical (rotated) orientations
ships = [
    {"name": "KoKo", "shapes": [[(0, 0), (1, 0)], [(0, 0), (0, 1)]]},  # A 2x1 ship
    {"name": "Cruiser", "shapes": [[(0, 0), (0, 1), (1, 0), (1, 1)]]},  # A 2x2 ship
    {"name": "Unicorn", "shapes": [[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]]}  # A '+' shaped ship
]

board = get_ship_configuration_count(board_size, ships,
                                     misses)  # Get the ship configuration count for the current state of the board

# Use the hunt mode if there are no hits, otherwise use the target mode
if not hits:
    guess = StrategyII_Hunt(board)
else:
    guess = StrategyII_Target(board, hits[-1])  # Use the most recent hit as the target

print("Task 4")

print("Next guess:", guess)

# Print the board
print("\nBoard with ship configuration count for each cell (row indices increasing from bottom to top):")
for row in reversed(board):
    print(row)
