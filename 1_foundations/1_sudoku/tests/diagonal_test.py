# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""This is a test for diagonal functionality"""

from sudoku.board import Board as SB

# Unit Test Solutions copied directly from solution_test.py and reformatted

# pylint: disable=invalid-name
solved_diag_sudoku = {
    'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4',
    'G1': '6', 'G9': '5', 'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1',
    'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3', 'C5': '2', 'C4': '8',
    'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
    'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7',
    'B5': '1', 'B6': '6', 'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3',
    'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2', 'I1': '7', 'I3': '8',
    'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
    'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5',
    'A9': '1', 'A8': '8', 'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4',
    'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6', 'H9': '4', 'H2': '3',
    'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
    'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3',
    'D2': '7', 'D3': '6', 'D1': '5'
}


def test_diagonal() -> None:
    """Solve problem with diagonal constraint enabled"""
    diagonal_grid = ('2.............62....1....7...6..8...3...9...7...6..4...4'
                     '....8....52.............3')
    sbrd = SB(diagonal_mode=True)
    board = sbrd.grid_values(diagonal_grid)

    result = sbrd.search(board)

    assert result == solved_diag_sudoku
