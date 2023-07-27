import unittest
import numpy as np
from grids import *
from solver import solve_sudoku

# TODO add tests


class Test_sudoku(unittest.TestCase):

    def test_1(self):
        np.testing.assert_equal(solve_sudoku(grid_1), grid_1_solution)

    def test_2(self):
        np.testing.assert_equal(solve_sudoku(grid_2), grid_2_solution)

    def test_3(self):
        np.testing.assert_equal(solve_sudoku(grid_3), grid_3_solution)

    def test_4(self):
        np.testing.assert_equal(solve_sudoku(grid_4), grid_4_solution)

    def test_5(self):
        np.testing.assert_equal(solve_sudoku(grid_5), grid_5_solution)
