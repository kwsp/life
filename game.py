"""
Conway's Game of Life

Rules:
    1. Any live cell with fewer than two live neighbours dies (underpopulation).
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies (overpopulation).
    4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction).

More condensed:
    1. Any live cell with 2 or 3 live neighbours survive.
    2. Any dead cell with 3 live neighbours becomes a live cell.
    3. All other live cells die in the next generation. All other dead cells stay dead.
"""
import numpy as np

ALIVE = True
DEAD = False


def n_neighbours(grid, i, j) -> int:
    "Count the # of neighbours of (i, j) in the grid."
    region = grid[max(0, i - 1) : i + 2, max(0, j - 1) : j + 2]
    return np.sum(region) - grid[i, j]


def tick(grid: np.ndarray) -> np.ndarray:
    "A tick in the Conway's Game of Life"
    new_grid = grid.copy()
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == ALIVE and (2 <= n_neighbours(grid, i, j) <= 3):
                # live cell with 2/3 neighbours survive
                pass
            elif v == DEAD and (n_neighbours(grid, i, j) == 3):
                # Any dead cell with 3 live neighbours becomes a live cell.
                new_grid[i, j] = ALIVE
            else:
                # All other live cells die in the next generation. All other dead cells stay dead.
                new_grid[i, j] = DEAD

    return new_grid


def game(cell_char="o"):
    import time
    import curses

    def curse_main(stdscr):
        curses.noecho()
        rows, cols = stdscr.getmaxyx()
        grid = np.random.randint(0, 2, (rows - 1, cols - 1)).astype(bool)
        s_grid = np.tile(" ", grid.shape)  # for printing

        while True:
            stdscr.clear()

            sg = s_grid.copy()
            sg[grid] = cell_char

            for i, row in enumerate(sg):
                s = " ".join(row)
                stdscr.addstr(i, 0, s)

            # Draw
            stdscr.refresh()

            # update
            grid = tick(grid)

            time.sleep(0.5)

    try:
        curses.wrapper(curse_main)
    except KeyboardInterrupt:
        print("bye bye")
    except curses.error as e:
        print("Your terminal probably resized, I can't handle this yet :(")
        print(e)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        game()
    else:
        game(sys.argv[1][0])
