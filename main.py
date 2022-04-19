import os
import time
import random

THRESHOLD = 0.7 # percentage of dead cells in initial state of the board

def dead_state(height, width):
    board = [[0]*width for h in range(height)]
    return board

def random_board(height, width):
    board = []
    for i in range(height):
        row = [1 if random.random() > THRESHOLD else 0 for _ in range(width)]
        board.append(row)
    return board

def render_board(board):
    board_str = ""
    for row in board:
        board_str += "".join(['#' if cell else ' ' for cell in row])
        board_str += '\n'
    print(board_str)

def next_board_state(board):
    next_state = []
    for r, row in enumerate(board):
        new_row = []
        for c, cell in enumerate(row):
            count = alive_neighbor_count(board, (r, c))
            if cell == 1:
                new_cell = 0 if count not in [2, 3] else 1
                new_row.append(new_cell)
            else:
                new_cell = 1 if count == 3 else 0
                new_row.append(new_cell)
        next_state.append(new_row)
    return next_state

def alive_neighbor_count(board, index):
    rows, cols = len(board), len(board[0])
    r, c = index

    neighbors = [
        (r-1, c-1),
        (r-1, c),
        (r-1, c+1),
        (r, c-1),
        (r, c+1),
        (r+1, c-1),
        (r+1, c),
        (r+1, c+1)
    ]

    # filter out invalid neighbors
    neighbors = filter(
        lambda n: 0 <= n[0] < rows and 0 <= n[1] < cols,
        neighbors
    )

    neighbor_cells = []
    for nr, nc in neighbors:
        neighbor_cells.append(board[nr][nc])
    
    return sum(neighbor_cells)


if __name__ == "__main__":
    board = random_board(20, 60)

    clear_cmd = 'cls' if os.name == 'nt' else 'clear'

    while True:
        os.system(clear_cmd) # clear terminal
        render_board(board)
        time.sleep(0.3)
        board = next_board_state(board)
