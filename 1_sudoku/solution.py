# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""
This file is a solution.py proxy to connect the original udacity
solution_test.py test with my project code base
"""

from typing import Dict
from sudoku.board import Board as SB


def solve(board_string: str) -> Dict[str, str]:
    """Call search with diagonal_mode True in board.py"""
    sbrd = SB(diagonal_mode=True)
    board = sbrd.grid_values(board_string)
    return sbrd.search(board)


def naked_twins(board_dict: Dict[str, str]) -> Dict[str, str]:
    """Call naked_twins in board.py"""
    sbrd = SB()
    return sbrd.naked_twins(board_dict)
