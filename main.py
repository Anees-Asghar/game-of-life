import os
import time
import random


THRESHOLD = 0.7 # percentage of dead cells in initial state of the board


def random_board(height, width):
    """
        Return a board of size height x width where each cell is either 0 (dead) or 1 
        (living). The ratio of dead to living cells is defined by THRESHOLD constant.
    """
    board = []
    for _ in range(height):
        row = [1 if random.random() > THRESHOLD else 0 for _ in range(width)]
        board.append(row)
    return board


def render_board(board):
    """
        Print board on the terminal.
    """
    board_str = ""
    for row in board:
        board_str += "".join(['#' if cell else ' ' for cell in row])
        board_str += '\n'
    print(board_str)


def next_board_state(board):
    """
        Return the next board state under the rules of the game, given the current
        board state.
    """
    next_state = []
    for r, row in enumerate(board):
        new_row = []
        for c, cell in enumerate(row):
            count = living_neighbor_count(board, (r, c))
            if cell == 1: # if living cell
                # acording to the rules of game of life, the only case when a living cell 
                # doesn't die off is when it has the right numbers of neighbors, i.e, 2 or 3
                new_cell = 0 if count not in [2, 3] else 1
                new_row.append(new_cell)
            else: # if dead cell
                # dead cell becomes alive if the neighbor count is exactly 3
                new_cell = 1 if count == 3 else 0
                new_row.append(new_cell)
        next_state.append(new_row)
    return next_state


def living_neighbor_count(board, cell_index):
    """
        Return the count of living neighbors of a cell, provided the index 
        of that cell.
    """
    r, c = cell_index
    height, width = len(board), len(board[0])

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
        lambda n: 0 <= n[0] < height and 0 <= n[1] < width,
        neighbors
    )

    # create a list of the states of the neighboring cells (dead or alive)
    neighbor_cells = []
    for nr, nc in neighbors:
        neighbor_cells.append(board[nr][nc])

    living_count = sum(neighbor_cells) # count the living neighbors

    return living_count


if __name__ == "__main__":
    board = random_board(20, 60) # initial board state

    clear_cmd = 'cls' if os.name == 'nt' else 'clear'

    while True:
        os.system(clear_cmd) # clear terminal
        render_board(board)
        time.sleep(0.3)
        board = next_board_state(board)
