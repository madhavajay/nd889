# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""This is a test for sudoku board"""

from typing import Any, TYPE_CHECKING
import pytest
from board import Board as SB


def test_cross() -> None:
    """cross returns expected combination of strings in array"""
    expected_array = ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    cross_array = SB.cross('abc', 'def')
    assert cross_array == expected_array


def test_boxes() -> None:
    boxes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
             'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
             'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
             'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
             'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
             'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
             'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
             'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
    assert SB.boxes() == boxes


def test_row_units() -> None:
    first_row = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
    assert SB.row_units()[0] == first_row


def test_column_units() -> None:
    first_column = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
    assert SB.column_units()[0] == first_column


def test_square_units() -> None:
    top_left_square = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    assert SB.square_units()[0] == top_left_square


def test_peers() -> None:
    peer = 'A1'
    a1_peers = ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B1', 'B2',
                'B3', 'C1', 'C2', 'C3', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
    board = SB()
    assert board.peers(peer) == set(a1_peers)


def test_grid_values() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')
    dict = {'A1': '.', 'A2': '.', 'A3': '3', 'A4': '.', 'A5': '2', 'A6': '.',
            'A7': '6', 'A8': '.', 'A9': '.', 'B1': '9', 'B2': '.', 'B3': '.',
            'B4': '3', 'B5': '.', 'B6': '5', 'B7': '.', 'B8': '.', 'B9': '1',
            'C1': '.', 'C2': '.', 'C3': '1', 'C4': '8', 'C5': '.', 'C6': '6',
            'C7': '4', 'C8': '.', 'C9': '.', 'D1': '.', 'D2': '.', 'D3': '8',
            'D4': '1', 'D5': '.', 'D6': '2', 'D7': '9', 'D8': '.', 'D9': '.',
            'E1': '7', 'E2': '.', 'E3': '.', 'E4': '.', 'E5': '.', 'E6': '.',
            'E7': '.', 'E8': '.', 'E9': '8', 'F1': '.', 'F2': '.', 'F3': '6',
            'F4': '7', 'F5': '.', 'F6': '8', 'F7': '2', 'F8': '.', 'F9': '.',
            'G1': '.', 'G2': '.', 'G3': '2', 'G4': '6', 'G5': '.', 'G6': '9',
            'G7': '5', 'G8': '.', 'G9': '.', 'H1': '8', 'H2': '.', 'H3': '.',
            'H4': '2', 'H5': '.', 'H6': '3', 'H7': '.', 'H8': '.', 'H9': '9',
            'I1': '.', 'I2': '.', 'I3': '5', 'I4': '.', 'I5': '1', 'I6': '.',
            'I7': '3', 'I8': '.', 'I9': '.'}
    # replace all . with 123456789
    for key, value in dict.items():
        if value == '.':
            dict[key] = '123456789'

    assert SB.grid_values(board_string) == dict


def test_grid_values_fail() -> None:
    board_string = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
    with pytest.raises(ValueError) as excinfo:
        SB.grid_values(board_string)


def test_board_to_str() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')
    str_list = list(board_string)
    str_list = list(item.replace('.', '123456789') for item in str_list)
    expected_string = ','.join(str_list)

    board = SB.grid_values(board_string)
    string = SB.board_to_str(board)
    assert string == expected_string


def test_eliminate() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')

    # eliminated board in comma separated format for easy comparison
    expected_string = ('45,4578,3,49,2,147,6,5789,57,9,24678,47,3,47,5,78,278,'
                       '1,25,257,1,8,79,6,4,23579,2357,345,345,8,1,3456,2,9,'
                       '34567,34567,7,123459,49,459,34569,4,1,13456,8,1345,'
                       '13459,6,7,3459,8,2,1345,345,134,1347,2,6,478,9,5,1478,'
                       '47,8,1467,47,2,457,3,17,1467,9,46,4679,5,4,1,47,3,'
                       '24678,2467')
    board = SB.grid_values(board_string)
    eliminated_board = SB().eliminate(board)
    eliminated_string = SB.board_to_str(eliminated_board)

    assert eliminated_string == expected_string


def test_only_choice() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')

    expected_string = ('45,8,3,9,2,1,6,5789,57,9,6,47,3,4,5,8,278,1,2,257,1,8,'
                       '7,6,4,23579,2357,345,345,8,1,3456,2,9,34567,34567,7,2,'
                       '9,5,34569,4,1,13456,8,1345,13459,6,7,3459,8,2,1345,'
                       '345,134,1347,2,6,8,9,5,1478,47,8,1467,47,2,5,3,17,6,9,'
                       '6,9,5,4,1,7,3,8,2')
    board_dict = SB.grid_values(board_string)
    sb = SB()
    eliminated_board = sb.eliminate(board_dict)
    only_choice_board = sb.only_choice(eliminated_board)
    only_choice_string = SB.board_to_str(only_choice_board)
    assert only_choice_string == expected_string


def test_reduce_puzzle() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')
    expected_string = ('4,8,3,9,2,1,6,5,7,9,6,7,3,4,5,8,2,1,2,5,1,8,7,6,4,9,3,'
                       '5,4,8,1,3,2,9,7,6,7,2,9,5,6,4,1,3,8,1,3,6,7,9,8,2,4,5,'
                       '3,7,2,6,8,9,5,1,4,8,1,4,2,5,3,7,6,9,6,9,5,4,1,7,3,8,2')

    board = SB.grid_values(board_string)
    sb = SB()
    solution = sb.reduce_puzzle(board)
    solution_string = sb.board_to_str(solution)
    assert solution_string == expected_string


def test_reduce_puzzle_incomplete() -> None:
    board_string = ('4.....8.5.3..........7......2.....6.....8.4......1.......'
                    '6.3.7.5..2.....1.4......')
    expected_string = ('4,1679,12679,139,2369,269,8,1239,5,26789,3,1256789,'
                       '14589,24569,245689,12679,1249,124679,2689,15689,'
                       '125689,7,234569,245689,12369,12349,123469,3789,2,'
                       '15789,3459,34579,4579,13579,6,13789,3679,15679,15679,'
                       '359,8,25679,4,12359,12379,36789,4,56789,359,1,25679,'
                       '23579,23589,23789,289,89,289,6,459,3,1259,7,12489,5,'
                       '6789,3,2,479,1,69,489,4689,1,6789,4,589,579,5789,'
                       '23569,23589,23689')

    board = SB.grid_values(board_string)
    sb = SB()
    solution = sb.reduce_puzzle(board)
    solution_string = sb.board_to_str(solution)
    assert solution_string == expected_string


def test_reduce_puzzle_fail() -> None:
    board_string = '.' * (9 * 9)
    board = SB.grid_values(board_string)

    sb = SB()
    solution = sb.reduce_puzzle(board)

    assert solution is None


def test_validate() -> None:
    board_string = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82..'
                    '..26.95..8..2.3..9..5.1.3..')
    board = SB.grid_values(board_string)
    sb = SB()
    solution = sb.reduce_puzzle(board)
    valid = sb.validate(solution)

    assert valid is True


def test_validate_fail() -> None:
    board_string = ('4.....8.5.3..........7......2.....6.....8.4......1.......'
                    '6.3.7.5..2.....1.4......')
    board = SB.grid_values(board_string)
    sb = SB()
    solution = sb.reduce_puzzle(board)
    valid = sb.validate(solution)

    assert valid is False


def test_sorted_box_possibilities() -> None:
    board_string = ('4.....8.5.3..........7......2.....6.....8.4......1.......'
                    '6.3.7.5..2.....1.4......')
    expected_sort = ['G2', 'H7', 'A4', 'A6', 'E4', 'F4', 'G1', 'G3', 'G5',
                     'H5', 'H8', 'I4', 'I5', 'A2', 'A5', 'A8', 'B8', 'C1',
                     'D1', 'D4', 'D6', 'E1', 'G7', 'H2', 'H9', 'I2', 'I6',
                     'A3', 'B1', 'B4', 'B5', 'B7', 'C2', 'C7', 'C8', 'D3',
                     'D5', 'D7', 'D9', 'E2', 'E3', 'E6', 'E8', 'E9', 'F1',
                     'F3', 'F6', 'F7', 'F8', 'F9', 'G9', 'I7', 'I8', 'I9',
                     'B6', 'B9', 'C3', 'C5', 'C6', 'C9', 'B3']
    board = SB.grid_values(board_string)
    sb = SB()
    reduced = sb.reduce_puzzle(board)
    SB.display(reduced)
    sorted_boxes = SB.sorted_box_possibilities(reduced)
    assert sorted_boxes == expected_sort


def test_search() -> None:
    board_string = ('4.....8.5.3..........7......2.....6.....8.4......1.......'
                    '6.3.7.5..2.....1.4......')
    expected_string = ('4,1,7,3,6,9,8,2,5,6,3,2,1,5,8,9,4,7,9,5,8,7,2,4,3,1,6,'
                       '8,2,5,4,3,7,1,6,9,7,9,1,5,8,6,4,3,2,3,4,6,9,1,2,7,5,8,'
                       '2,8,9,6,4,3,5,7,1,5,7,3,2,9,1,6,8,4,1,6,4,8,7,5,2,9,3')
    board = SB.grid_values(board_string)
    sb = SB()
    solution = sb.search(board)
    SB.display(solution)
    solution_string = SB.board_to_str(solution)
    assert solution_string == expected_string


def test_diagonal_board() -> None:
    sb = SB()
    sb_diagonal = SB(diagonal_mode=True)
    assert sb.all_units() != sb_diagonal.all_units()
    assert sb.all_units() + SB.diagonal_units() == sb_diagonal.all_units()


def test_diagonal_units() -> None:
    units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
             ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
    diagonal_units = SB.diagonal_units()
    assert diagonal_units == units


def test_display_board(capsys: Any) -> None:
    board_string = ('483921657967345821251876493548132976729564138136798245'
                    '372689514814253769695417382')
    # display stdout for printing sudoku board
    with capsys.disabled():
        print('\n')
        SB.display(SB.grid_values(board_string))
        print('\n')
