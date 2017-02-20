# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""This is a sudoku board"""

from typing import List, Dict, Set, TYPE_CHECKING


class Board:
    values = '123456789'
    rows = 'ABCDEFGHI'
    row_squares = ['ABC', 'DEF', 'GHI']
    cols = '123456789'
    col_squares = ['123', '456', '789']
    _peers = None  # type: Dict[str, Set[str]]
    _all_units = None  # type: List[List[str]]
    _units = None  # type: Dict[str, List[List[str]]]

    @staticmethod
    def cross(x: str, y: str) -> List[str]:
        return [a+b for a in x for b in y]

    @staticmethod
    def boxes() -> List[str]:
        return Board.cross(Board.rows, Board.cols)

    @staticmethod
    def num_boxes() -> int:
        return len(Board.rows) * len(Board.cols)

    @staticmethod
    def row_units() -> List[List[str]]:
        return [Board.cross(r, Board.cols) for r in Board.rows]

    @staticmethod
    def column_units() -> List[List[str]]:
        return [Board.cross(Board.rows, c) for c in Board.cols]

    @staticmethod
    def square_units() -> List[List[str]]:
        return [Board.cross(rs, cs)
                for rs in (Board.row_squares)
                for cs in (Board.col_squares)]

    # TODO optional: if you wanted to make this more "Pythonic" this would be a good place to use the @property decorator
    # which does the work cacheing computations for you
    # https://docs.python.org/3/library/functions.html#property
    # but honestly it's fine, just an FYI
    @staticmethod
    def all_units() -> List[List[str]]:
        if Board._all_units is None:
            Board._all_units = (Board.row_units() +
                                Board.column_units() +
                                Board.square_units())
        return Board._all_units

    @staticmethod
    def generate_units() -> Dict[str, List[List[str]]]:
        boxes = Board.boxes()

        # add all combinations of units together
        all = Board.all_units()

        # re-arrange to dictionary of boxes and array of their units
        units = dict(
            # TODO: all is a builtin keyword, usually not a problem here due to scoping but it's
            # considered bad practice to shadow builtin functions
            (box, [unit for unit in all if box in unit]) for box in boxes)
        return units

    @staticmethod
    def units(box: str) -> List[List[str]]:
        if Board._units is None:
            Board._units = Board.generate_units()
        return Board._units[box]

    @staticmethod
    def generate_peers() -> Dict[str, Set[str]]:
        boxes = Board.boxes()

        peers = dict(
            (bx, set(sum(Board.units(bx), [])) - set([bx])) for bx in boxes)

        return peers

    @staticmethod
    def peers(box: str) -> Set[str]:
        if Board._peers is None:
            Board._peers = Board.generate_peers()
        return Board._peers[box]

    @staticmethod
    def grid_values(board_string: str) -> Dict[str, str]:
        if len(board_string) != Board.num_boxes():
            raise ValueError('Board string length must be 81 characters')

        board_dict = {}
        boxes = Board.boxes()
        for index, value in enumerate(board_string):
            if value == '.':
                value = Board.values
            board_dict[boxes[index]] = value
        return board_dict

    @staticmethod
    def board_to_str(board_dict: Dict[str, str]) -> str:
        """
        Convert a board dictionary into a comma separated string of values
        in order of the original boxes array for easy comparison during tests
        """
        string = ''
        for key in Board.boxes():
            string += board_dict[key] + ','
        return string[:-1]

    @staticmethod
    def eliminate(board_dict: Dict[str, str]) -> Dict[str, str]:
        solved_values = [box for box in board_dict.keys()
                         if len(board_dict[box]) == 1]
        for box in solved_values:
            digit = board_dict[box]
            for peer in Board.peers(box):
                board_dict[peer] = board_dict[peer].replace(digit, '')
        return board_dict

    @staticmethod
    def only_choice(board_dict: Dict[str, str]) -> Dict[str, str]:
        # TODO: see note above, "all" is a builtin function, don't shadow it
        all = Board.all_units()
        for unit in all:
            for number in range(1, 10):
                possible_boxes = [box for box in unit
                                  if str(number) in board_dict[box]]
                if len(possible_boxes) == 1:
                    board_dict[possible_boxes[0]] = str(number)
        return board_dict

    @staticmethod
    def num_solved_boxes(board_dict: Dict[str, str]) -> int:
        return len([box for box in board_dict.keys()
                    if len(board_dict[box]) == 1])

    @staticmethod
    def sorted_box_possibilities(board_dict: Dict[str, str]) -> List[str]:
        options = [box for box in board_dict.keys()
                   if len(board_dict[box]) > 1]

        # TODO: I might be wrong, but I don't think this does what you're
        # expecting -- len(board_dict[box]) should always be the same,
        # maybe you meant len(''.join(board_dict[box]) or something?
        return sorted(options, key=lambda box: len(board_dict[box]))

    @staticmethod
    def reduce_puzzle(board_dict: Dict[str, str]) -> Dict[str, str]:
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = Board.num_solved_boxes(board_dict)

            # Use the Eliminate Strategy
            board_dict = Board.eliminate(board_dict)

            # Use the Only Choice Strategy
            board_dict = Board.only_choice(board_dict)

            # Check how many boxes have a determined value, to compare
            solved_values_after = Board.num_solved_boxes(board_dict)

            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after

            # If no values at all terminate and return None
            if solved_values_after == 0:
                # TODO: this is going to mess up your type annotation
                # maybe return empty dict or change type annotation?
                return None

        return board_dict

    @staticmethod
    def validate(board_dict: Dict[str, str]) -> bool:
        valid = True
        # TODO: shadowing built in keyword
        all = Board.all_units()
        complete_unit = set(Board.values)
        for unit in all:
            unit_values = [board_dict[box] for box in unit]
            unit_set = set(unit_values)
            if unit_set != complete_unit:
                print('bad set {}'.format(unit_set))
                valid = False
                break
        return valid

    @staticmethod
    def search(board_dict: Dict[str, str]) -> Dict[str, str]:
        """
        Using depth-first search and propagation,
        create a search tree and solve the sudoku.
        """
        # First, reduce the puzzle using the previous function
        reduced = Board.reduce_puzzle(board_dict)
        if reduced is None:
            # TODO: messes up annotationgs... make return empty dict
            # or change annotations
            return reduced

        if Board.num_solved_boxes(reduced) == Board.num_boxes():
            if Board.validate(reduced):
                return reduced
            else:
                return None

        # Choose one of the unfilled squares with the fewest possibilities
        possibilities = Board.sorted_box_possibilities(reduced)
        if len(possibilities) > 0:
            smallest_box = possibilities[0]
            choices = list(reduced[smallest_box])

            for combination in choices:
                board_copy = reduced.copy()
                board_copy[smallest_box] = combination
                result = Board.search(board_copy)
                if result is not None:
                    return result

        # TODO: see above note on annotations
        return None

    @staticmethod
    def naked_twins(board_dict: Dict[str, str]) -> Dict[str, str]:
        """
        Where there are 2 identical unsolved boxes with 2 values
        in a given unit, remove both values from all other boxes in their unit
        """

        # get all 2 value boxes
        two_value_boxes = [box for box in board_dict.keys()
                           if len(board_dict[box]) == 2]

        for box in two_value_boxes:
            options = board_dict[box]
            for unit in Board.units(box):
                naked_twins = [box for box in unit
                               if board_dict[box] == options]
                if len(naked_twins) == 2:
                    for obox in [bx for bx in unit if bx not in naked_twins]:
                        new_set = board_dict[obox]
                        for option in options:
                            new_set = new_set.replace(option, '')
                        board_dict[obox] = new_set

        return board_dict

    @staticmethod
    def display(values: Dict[str, str]) -> None:
        width = 1 + max(len(values[s]) for s in Board.boxes())
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in Board.rows:
            print(''.join(
                values[r + c].center(width) +
                ('|' if c in '36' else '')
                for c in Board.cols)
            )
            if r in 'CF':
                print(line)
