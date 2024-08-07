import unittest
import numpy as np

from game import n_neighbours, tick_slow, tick_fast


class TestNNeighbours(unittest.TestCase):
    def test1(self):
        grid = np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 0],
            ]
        )
        self.assertEqual(n_neighbours(grid, 0, 0), 1)
        self.assertEqual(n_neighbours(grid, 0, 1), 1)
        self.assertEqual(n_neighbours(grid, 0, 2), 2)
        self.assertEqual(n_neighbours(grid, 1, 0), 3)
        self.assertEqual(n_neighbours(grid, 1, 1), 4)
        self.assertEqual(n_neighbours(grid, 1, 2), 2)
        self.assertEqual(n_neighbours(grid, 2, 0), 1)
        self.assertEqual(n_neighbours(grid, 2, 1), 2)
        self.assertEqual(n_neighbours(grid, 2, 2), 2)


class TestTick(unittest.TestCase):
    def test_slow(self):
        grid = np.array([[0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0]])
        new_grid = tick_slow(grid)
        new_grid_true = np.array(
            [[1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0]]
        )
        self.assertTrue(np.all(new_grid == new_grid_true))

    def test_fast(self):
        grid = np.array([[0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0]])
        new_grid = tick_fast(grid)
        new_grid_true = np.array(
            [[1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0]]
        )
        self.assertTrue(np.all(new_grid == new_grid_true))


if __name__ == "__main__":
    unittest.main()
