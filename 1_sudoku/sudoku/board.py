# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 1 - Sudoku"""

from typing import List, Dict, Set

# type alias for the board state
BoardState = Dict[str, str]

# type alias for unit
Unit = List[str]


class Board():
    """
    Sudoku Board which implements various strategies to solve sudoku puzzles
    """
    _values = '123456789'
    _rows = 'ABCDEFGHI'
    _row_squares = ['ABC', 'DEF', 'GHI']
    _cols = '123456789'
    _col_squares = ['123', '456', '789']

    def __init__(self, diagonal_mode: bool=False) -> None:
        self._diagonal_mode = diagonal_mode
        self._peers = None  # type: Dict[str, Set[str]]
        self._all_units = None  # type: List[Unit]
        self._units = None  # type: Dict[str, List[Unit]]

    @staticmethod
    def cross(x_axis: str, y_axis: str) -> List[str]:
        """Zip characters from two strings into a list of 2 character keys"""
        return [x_val + y_val for x_val in x_axis for y_val in y_axis]

    @staticmethod
    def boxes() -> List[str]:
        """Generate all possible box location keys on the board"""
        return Board.cross(Board._rows, Board._cols)

    @staticmethod
    def num_boxes() -> int:
        """Return the number of boxes in the board"""
        return len(Board._rows) * len(Board._cols)

    @staticmethod
    def _row_units() -> List[Unit]:
        """Generate all row units for the board"""
        return [Board.cross(r, Board._cols) for r in Board._rows]

    @staticmethod
    def _column_units() -> List[Unit]:
        """Generate all column units for the board"""
        return [Board.cross(Board._rows, c) for c in Board._cols]

    @staticmethod
    def _diagonal_units() -> List[Unit]:
        """Generate both diagonal units for the board"""
        unit_1 = [Board._rows[int(vl) - 1] + vl for vl in Board._values]
        unit_2 = [Board._rows[::-1][int(vl) - 1] + vl for vl in Board._values]

        return [unit_1, unit_2]

    @staticmethod
    def _square_units() -> List[Unit]:
        """Generate all quadrant units for the board"""
        return [Board.cross(rs, cs)
                for rs in Board._row_squares
                for cs in Board._col_squares]

    def all_units(self) -> List[Unit]:
        """
        Combine all units together into an list of units, supports additional
        diagonal units if self._diagonal_mode is True
        """
        if self._all_units is None:
            self._all_units = (Board._row_units() +
                               Board._column_units() +
                               Board._square_units())
            if self._diagonal_mode:
                self._all_units = self._all_units + Board._diagonal_units()
        return self._all_units

    def generate_units(self) -> Dict[str, List[Unit]]:
        """Generate all units once and cache them"""
        boxes = Board.boxes()

        # add all combinations of units together
        all_u = self.all_units()

        # re-arrange to dictionary of boxes and array of their units
        units = dict(
            (box, [unit for unit in all_u if box in unit]) for box in boxes)
        return units

    def units(self, box: str) -> List[Unit]:
        """Fetch units and generate if they don't exist yet"""
        if self._units is None:
            self._units = self.generate_units()
        return self._units[box]

    def generate_peers(self) -> Dict[str, Set[str]]:
        """Generate all peers for every possible box key"""
        boxes = Board.boxes()

        peers = dict(
            (bx, set(sum(self.units(bx), [])) - set([bx])) for bx in boxes)

        return peers

    def peers(self, box: str) -> Set[str]:
        """Return peers for a given box key"""
        if self._peers is None:
            self._peers = self.generate_peers()
        return self._peers[box]

    @staticmethod
    def grid_values(board_string: str) -> BoardState:
        """Convert unsolved board string into a board state dictionary"""
        if len(board_string) != Board.num_boxes():
            raise ValueError('Board string length must be 81 characters')

        board_dict = {}
        boxes = Board.boxes()
        for index, value in enumerate(board_string):
            if value == '.':
                value = Board._values
            board_dict[boxes[index]] = value
        return board_dict

    @staticmethod
    def board_to_str(board_dict: BoardState) -> str:
        """
        Convert a board dictionary into a comma separated string of values
        in order of the original boxes array for easy comparison during tests
        """
        string = ''
        for key in Board.boxes():
            string += board_dict[key] + ','
        return string[:-1]

    def eliminate(self, board_dict: BoardState) -> BoardState:
        """Apply the eliminate strategy on the supplied board and return it"""
        solved_values = [box for box in board_dict.keys()
                         if len(board_dict[box]) == 1]
        for box in solved_values:
            digit = board_dict[box]
            for peer in self.peers(box):
                board_dict[peer] = board_dict[peer].replace(digit, '')
        return board_dict

    def only_choice(self, board_dict: BoardState) -> BoardState:
        """Apply only choice strategy on the supplied board and return it"""
        all_units = self.all_units()
        for unit in all_units:
            for number in range(1, 10):
                possible_boxes = [box for box in unit
                                  if str(number) in board_dict[box]]
                if len(possible_boxes) == 1:
                    board_dict[possible_boxes[0]] = str(number)
        return board_dict

    @staticmethod
    def num_solved_boxes(board_dict: BoardState) -> int:
        """Calculate number of solved boxes on the board"""
        return len([box for box in board_dict.keys()
                    if len(board_dict[box]) == 1])

    @staticmethod
    def sorted_box_possibilities(board_dict: BoardState) -> List[str]:
        """Return unsolved boxes ordered by lowest combinations first"""
        options = [box for box in board_dict.keys()
                   if len(board_dict[box]) > 1]
        return sorted(options, key=lambda box: len(board_dict[box]))

    def reduce_puzzle(self, board_dict: BoardState) -> BoardState:
        """Recursively apply eliminate and only choice until no change"""
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = Board.num_solved_boxes(board_dict)

            # Use the Eliminate Strategy
            board_dict = self.eliminate(board_dict)

            # Use the Only Choice Strategy
            board_dict = self.only_choice(board_dict)

            # Check how many boxes have a determined value, to compare
            solved_values_after = Board.num_solved_boxes(board_dict)

            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after

            # If no values at all terminate and return None
            if solved_values_after == 0:
                return None
        return board_dict

    def validate(self, board_dict: BoardState) -> bool:
        """Check every unit on the board contains the set 1-9"""
        valid = True
        all_units = self.all_units()
        complete_unit = set(Board._values)
        for unit in all_units:
            unit_values = [board_dict[box] for box in unit]
            unit_set = set(unit_values)
            if unit_set != complete_unit:
                valid = False
                break
        return valid

    def search(self, board_dict: BoardState) -> BoardState:
        """
        Using depth-first search recursively reduce the board state
        until the first leaf is solved or there are no solutions
        """
        # First, reduce the puzzle using the previous function
        reduced = self.reduce_puzzle(board_dict)
        if reduced is None:
            return reduced

        if Board.num_solved_boxes(reduced) == Board.num_boxes():
            if self.validate(reduced):
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
                result = self.search(board_copy)
                if result is not None:
                    return result

        return None

    def naked_twins(self, board_dict: BoardState) -> BoardState:
        """
        Search for pairs of unsolved boxes with 2 matching values in each unit
        and remove both values from all other boxes in that unit
        """

        # get all 2 value boxes
        two_value_boxes = [box for box in board_dict.keys()
                           if len(board_dict[box]) == 2]

        for box in two_value_boxes:
            options = board_dict[box]
            for unit in self.units(box):
                naked_twins = [box for box in unit
                               if board_dict[box] == options]
                if len(naked_twins) == 2:
                    boxes = [bx for bx in unit if bx not in naked_twins]
                    values = set(list(options))
                    board_dict = Board._remove_values_in_boxes(board_dict,
                                                               values, boxes)

        return board_dict

    def naked_multi(self, board_dict: BoardState,
                    size: int) -> BoardState:
        """
        Search for groups of twins, triplets, quads in a more generalized way
        and remove values from all other boxes in that unit

        A set can be defined as two or more boxes in which at least one box
        has as many possible values in it as the size of the group which we
        can call a leader and each other member has the same set or subset
        of those values where the subset is greater than 1 (solved)

        In this case it can be assumed that these units are dependant and
        therefore the other units can have this super set of values removed
        """

        # candidate leader boxes
        size_value_boxes = [box for box in board_dict.keys()
                            if len(board_dict[box]) == size]

        # go through each candidate leader
        for leader_box in size_value_boxes:
            # the options for the box
            options = set(list(board_dict[leader_box]))
            # go through all units that potential leader is in
            for unit in self.units(leader_box):
                subsets = []
                for box in [box for box in unit
                            if box != leader_box]:
                    subset = set(list(board_dict[box]))
                    if len(subset) > 1 and subset.issubset(options):
                        subsets.append(subset)
                if len(subsets) == size - 1:
                    board_dict = Board._remove_values_in_boxes(board_dict,
                                                               options, unit)

        return board_dict

    @staticmethod
    def _remove_values_in_boxes(board_dict: BoardState, values: Set[str],
                                boxes: List[str]) -> BoardState:
        for box in boxes:
            new_set = board_dict[box]
            if not set(list(new_set)).issubset(values):
                for value in values:
                    if len(new_set) > 1:
                        new_set = new_set.replace(value, '')
                if board_dict[box] != new_set:
                    board_dict[box] = new_set
        return board_dict

    @staticmethod
    def display(values: BoardState) -> None:
        """Print ascii board representation of board dictionary"""
        width = 1 + max(len(values[s]) for s in Board.boxes())
        line = '+'.join(['-' * (width * 3)] * 3)
        for row in Board._rows:
            print(''.join(
                values[row + col].center(width) +
                ('|' if col in '36' else '') for col in Board._cols))
            if row in 'CF':
                print(line)
