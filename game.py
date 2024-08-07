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
from scipy.signal import convolve2d


ALIVE = True
DEAD = False


def n_neighbours(grid, i, j) -> int:
    "Count the # of neighbours of (i, j) in the grid."
    region = grid[max(0, i - 1) : i + 2, max(0, j - 1) : j + 2]
    return np.sum(region) - grid[i, j]


def tick_slow(grid: np.ndarray) -> np.ndarray:
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


def tick_fast(grid: np.ndarray) -> np.ndarray:
    new_grid = np.zeros(grid.shape).astype(bool)
    neighbours = convolve2d(grid, _kernel, "same")
    new_grid[neighbours == 3] = ALIVE
    new_grid[np.logical_and(neighbours == 2, grid == ALIVE)] = ALIVE
    return new_grid


_kernel = np.array(
    [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
)


def game(cell_char: bytes = b"o"):
    import time
    import curses

    def curse_main(stdscr):
        curses.noecho()
        curses.curs_set(False)
        rows, cols = stdscr.getmaxyx()
        cols = cols // 2  # space between each cell
        grid = np.random.randint(0, 2, (rows, cols)).astype(bool)
        s_grid = np.tile(b" ", grid.shape)  # for printing

        while True:
            # update
            grid = tick_fast(grid)
            sg = s_grid.copy()
            sg[grid] = cell_char

            # built screen buffer
            buf = b"\n".join([b" ".join(row) for row in sg])

            # Draw
            stdscr.clear()
            stdscr.addstr(buf)
            stdscr.refresh()

            time.sleep(0.5)

    try:
        curses.wrapper(curse_main)
    except KeyboardInterrupt:
        print("bye bye")
    except curses.error as e:
        print("Your terminal probably resized, I can't handle that yet :(")
        print(e)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        game()
    else:
        game(bytes(sys.argv[1][0], "utf-8"))
