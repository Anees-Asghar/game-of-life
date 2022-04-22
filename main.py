import os
import sys
import time
import random

LIVE_CELL_CHAR = '+'
DEAD_CELL_CHAR = ' '
SLEEP_TIME = 0.5 # dictates how long before the next generation is loaded on the terminal (seconds) 
DEAD_CELL_PER = 0.8 # percentage of dead cells in initial state of the board


def random_board(height, width):
    """
        Return a board of size height x width where each cell is either 0 (dead) or 1 
        (live). The ratio of dead to live cells is defined by the constant THRESHOLD.
    """
    board = []
    for _ in range(height):
        row = [1 if random.random() > DEAD_CELL_PER else 0 for _ in range(width)]
        board.append(row)
    return board


def render_board(board):
    """
        Print board on the terminal.
    """
    board_str = ""
    for row in board:
        board_str += "".join([LIVE_CELL_CHAR if cell else DEAD_CELL_CHAR for cell in row])
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
            count = live_neighbor_count(board, (r, c))
            if cell == 1: # if live cell
                # acording to the rules of game of life, the only case when a live cell 
                # doesn't die off is when it has the right numbers of neighbors, i.e, 2 or 3
                new_cell = 0 if count not in [2, 3] else 1
                new_row.append(new_cell)
            else: # if dead cell
                # dead cell becomes alive if the neighbor count is exactly 3
                new_cell = 1 if count == 3 else 0
                new_row.append(new_cell)
        next_state.append(new_row)
    return next_state


def live_neighbor_count(board, cell_index):
    """
        Return the count of live neighbors of a cell, provided the index 
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

    live_count = sum(neighbor_cells) # count the live neighbors

    return live_count


def save_board(board, filename="last_image"):
    """
        Save board state in a file for later use.
    """
    with open(f"saved_states/{filename}", 'w') as f:
        lines = []
        for row in board:
            line = ''.join([str(i) for i in row])
            lines.append(line)
        f.write('\n'.join(lines))


def load_board(filename):
    """
        Load a saved board state.
    """
    board = []

    with open(f"saved_states/{filename}", 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            row = [int(i) for i in line]
            board.append(row)

    return board


def main():
    """
        Loads an initial board state and runs the game of life.
    """
    if len(sys.argv) > 1:
        board = load_board(filename=sys.argv[1])
    else:
        board = random_board(20, 60)
        save_board(board)

    clear_cmd = 'cls' if os.name == 'nt' else 'clear'

    while True:
        os.system(clear_cmd) # clear terminal
        render_board(board)
        time.sleep(SLEEP_TIME)
        board = next_board_state(board) 


if __name__ == "__main__":
    main()
