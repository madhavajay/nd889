# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 2 - Build a Game-Playing Agent"""

import random
import copy
import logging
from functools import reduce
from typing import Any, Set, Dict, Callable, Tuple, List

from isolation import Board

# player has no real type so we will use Any
Player = Any
Move = Tuple[int, int]
Timer = Callable[[], int]
Heuristic = Callable[[Board, Player], float]
MoveLookUp = Dict[Move, List[Move]]


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game: Board, player: Player) -> float:
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    return moves_ratio(game, player)


# Pre calculated Dictionary of Board position to Board value
BOARD_VALUE = {(0, 0): 1, (0, 1): 2, (0, 2): 2, (0, 3): 2, (0, 4): 2, (0, 5): 2, (0, 6): 1, (1, 0): 2, (1, 1): 3, (1, 2): 4, (1, 3): 4, (1, 4): 4, (1, 5): 3, (1, 6): 2, (2, 0): 2, (2, 1): 4, (2, 2): 5, (2, 3): 5, (2, 4): 5, (2, 5): 4, (2, 6): 2, (3, 0): 2, (3, 1): 4, (3, 2): 5, (3, 3): 6, (3, 4): 5, (3, 5): 4, (3, 6): 2, (4, 0): 2, (4, 1): 4, (4, 2): 5, (4, 3): 5, (4, 4): 5, (4, 5): 4, (4, 6): 2, (5, 0): 2, (5, 1): 3, (5, 2): 4, (5, 3): 4, (5, 4): 4, (5, 5): 3, (5, 6): 2, (6, 0): 1, (6, 1): 2, (6, 2): 2, (6, 3): 2, (6, 4): 2, (6, 5): 2, (6, 6): 1}
# Pre calculated Dictionary of Board position to every position 1 move away
BOARD_PROXIMITY = {(0, 0): [(1, 2), (2, 1)], (0, 1): [(1, 3), (2, 0), (2, 2)], (0, 2): [(1, 0), (1, 4), (2, 1), (2, 3)], (0, 3): [(1, 1), (1, 5), (2, 2), (2, 4)], (0, 4): [(1, 2), (1, 6), (2, 3), (2, 5)], (0, 5): [(1, 3), (2, 4), (2, 6)], (0, 6): [(1, 4), (2, 5)], (1, 0): [(0, 2), (2, 2), (3, 1)], (1, 1): [(0, 3), (2, 3), (3, 0), (3, 2)], (1, 2): [(0, 0), (0, 4), (2, 0), (2, 4), (3, 1), (3, 3)], (1, 3): [(0, 1), (0, 5), (2, 1), (2, 5), (3, 2), (3, 4)], (1, 4): [(0, 2), (0, 6), (2, 2), (2, 6), (3, 3), (3, 5)], (1, 5): [(0, 3), (2, 3), (3, 4), (3, 6)], (1, 6): [(0, 4), (2, 4), (3, 5)], (2, 0): [(0, 1), (1, 2), (3, 2), (4, 1)], (2, 1): [(0, 0), (0, 2), (1, 3), (3, 3), (4, 0), (4, 2)], (2, 2): [(0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3)], (2, 3): [(0, 2), (0, 4), (1, 1), (1, 5), (3, 1), (3, 5), (4, 2), (4, 4)], (2, 4): [(0, 3), (0, 5), (1, 2), (1, 6), (3, 2), (3, 6), (4, 3), (4, 5)], (2, 5): [(0, 4), (0, 6), (1, 3), (3, 3), (4, 4), (4, 6)], (2, 6): [(0, 5), (1, 4), (3, 4), (4, 5)], (3, 0): [(1, 1), (2, 2), (4, 2), (5, 1)], (3, 1): [(1, 0), (1, 2), (2, 3), (4, 3), (5, 0), (5, 2)], (3, 2): [(1, 1), (1, 3), (2, 0), (2, 4), (4, 0), (4, 4), (5, 1), (5, 3)], (3, 3): [(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)], (3, 4): [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 3), (5, 5)], (3, 5): [(1, 4), (1, 6), (2, 3), (4, 3), (5, 4), (5, 6)], (3, 6): [(1, 5), (2, 4), (4, 4), (5, 5)], (4, 0): [(2, 1), (3, 2), (5, 2), (6, 1)], (4, 1): [(2, 0), (2, 2), (3, 3), (5, 3), (6, 0), (6, 2)], (4, 2): [(2, 1), (2, 3), (3, 0), (3, 4), (5, 0), (5, 4), (6, 1), (6, 3)], (4, 3): [(2, 2), (2, 4), (3, 1), (3, 5), (5, 1), (5, 5), (6, 2), (6, 4)], (4, 4): [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)], (4, 5): [(2, 4), (2, 6), (3, 3), (5, 3), (6, 4), (6, 6)], (4, 6): [(2, 5), (3, 4), (5, 4), (6, 5)], (5, 0): [(3, 1), (4, 2), (6, 2)], (5, 1): [(3, 0), (3, 2), (4, 3), (6, 3)], (5, 2): [(3, 1), (3, 3), (4, 0), (4, 4), (6, 0), (6, 4)], (5, 3): [(3, 2), (3, 4), (4, 1), (4, 5), (6, 1), (6, 5)], (5, 4): [(3, 3), (3, 5), (4, 2), (4, 6), (6, 2), (6, 6)], (5, 5): [(3, 4), (3, 6), (4, 3), (6, 3)], (5, 6): [(3, 5), (4, 4), (6, 4)], (6, 0): [(4, 1), (5, 2)], (6, 1): [(4, 0), (4, 2), (5, 3)], (6, 2): [(4, 1), (4, 3), (5, 0), (5, 4)], (6, 3): [(4, 2), (4, 4), (5, 1), (5, 5)], (6, 4): [(4, 3), (4, 5), (5, 2), (5, 6)], (6, 5): [(4, 4), (4, 6), (5, 3)], (6, 6): [(4, 5), (5, 4)]}

# Infinity and negative infinity constants
INF = float("inf")
NEGINF = float("-inf")


def mov_pos_block(game: Board, player: Player) -> float:
    """
    Get the diff of moves between users and then add the value of the diff
    of each players board positions, finally add a bonus if the move blocks
    the opponent
    """
    # get moves
    own_moves = game.get_legal_moves(player)

    # loser
    if player == game.active_player and not own_moves:
        return NEGINF

    # get opp moves
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)

    # winner
    if player == game.inactive_player and not opp_moves:
        return INF

    moves_diff = (len(own_moves) - len(opp_moves))
    loc = game.get_player_location(player)
    opp_loc = game.get_player_location(opp)
    pos_value_diff = BOARD_VALUE[loc] - BOARD_VALUE[opp_loc]
    block_bonus = 1 if opp in BOARD_PROXIMITY[loc] else 0

    return float(moves_diff + pos_value_diff + block_bonus)


def moves_ratio(game: Board, player: Player) -> float:
    """
    Calculate the ratio by dividing players moves and opponents moves
    """
    # get moves
    own_moves = game.get_legal_moves(player)

    # loser
    if player == game.active_player and not own_moves:
        return NEGINF

    # get opp moves
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)

    # winner
    if player == game.inactive_player and not opp_moves:
        return INF

    num_own_moves = len(own_moves)
    num_opp_moves = len(opp_moves)
    # edge case where opponents turn hasnt happened yet but they have 0 moves
    # the game is technically over but num_opp_moves is 0 do it cant be a
    # denominator
    if (player == game.active_player and
       num_own_moves > 0 and num_opp_moves == 0):
        return INF

    return float(num_own_moves / num_opp_moves)


def quick_center(game: Board, player: Player) -> float:
    """
    Encourage player to move to the middle of the board with minimal compute
    """
    # get moves
    own_moves = game.get_legal_moves(player)

    # loser
    if player == game.active_player and not own_moves:
        return NEGINF

    # get opp moves
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)

    # winner
    if player == game.inactive_player and not opp_moves:
        return INF

    loc = game.get_player_location(player)
    opp_loc = game.get_player_location(opp)
    loc_dist = abs(loc[0] - 3) + abs(loc[1] - 3)
    opp_loc_dist = abs(opp_loc[0] - 3) + abs(opp_loc[1] - 3)
    return float(opp_loc_dist - loc_dist)


# 2 dimensional array, [x][y] of 0s representing an empty board
EMPTY_BOARD = [[0 for x in range(7)] for y in range(7)]
# Array of board values indexed from 0 where 0 is none and distance of
# 1 is worth 5 and so on
SCORING_VALUES = [0, 5, 4, 3, 2, 1]
# Set of board dimensions
DIMENSIONS = {0, 1, 2, 3, 4, 5, 6}
# Move operations for all directions from a single square
DIRECTIONS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]
# Location operations for clover positions around a square
CLOVER = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

# Outer rows and columns
OUTSIDE = [{0}, {6}]
# Outer corners
CORNERS = [{0, 6}] + OUTSIDE
# Rows and columns one square in
IN_ONE = [{1}, {5}]
# Corners one square in
IN_CORNERS = [{1, 5}] + IN_ONE
# Rows and Columns one square in
IN_TWO = [{2}, {4}]


# position value
def board_rank(game: Board, player: Player) -> Dict[Move, int]:
    """
    Calculate a dictionary of board positions with values for each position
    starting from the outside and working its way in one square at a time
    """
    values = {}
    for x in range(7):
        for y in range(7):
            loc = (x, y)
            if set(loc) in CORNERS:
                values[loc] = 1
            elif {loc[0]} in OUTSIDE or {loc[1]} in OUTSIDE:
                values[loc] = 2
            elif set(loc) in IN_CORNERS:
                values[loc] = 3
            elif {loc[0]} in IN_ONE or {loc[1]} in IN_ONE:
                values[loc] = 4
            elif {loc[0]} in IN_TWO or {loc[1]} in IN_TWO:
                values[loc] = 5
            else:
                values[loc] = 6
    return values


def board_proximity(game: Board, player: Player) -> MoveLookUp:
    """
    Calculate a dictionary with board positions as the key and for the value
    a list of the board positions which are 1 move away as a knight
    """
    values = {}
    for x in range(7):
        for y in range(7):
            loc = (x, y)
            possible_moves = []
            for direction in DIRECTIONS:
                move = (loc[0] + direction[0], loc[1] + direction[1])
                if move[0] in DIMENSIONS and move[1] in DIMENSIONS:
                    possible_moves.append(move)
            values[loc] = possible_moves
    return values


def ensemble(game: Board, player: Player) -> float:
    """
    Combine several different heuristics into one function
    """

    plane_walker_score = plane_walker(game, player)
    build_wall_score = build_wall(game, player)
    rush_middle_score = rush_middle(game, player)
    block_move_score = block_move(game, player)
    clover_leaf_score = clover_leaf(game, player)

    return (
        plane_walker_score +
        build_wall_score +
        rush_middle_score +
        block_move_score +
        clover_leaf_score
    )


def plane_walker(game: Board, player: Player) -> float:
    """
    Calculate the number of board squares available to the player
    and give each a value decreasing as they are more moves away from the
    current move, then add these up and diff them between players
    """
    blanks = game.get_blank_spaces()

    moves = game.get_legal_moves(player)
    distance_map = build_map(moves, blanks)
    board_value = score_board_distance(distance_map)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_distance_map = build_map(opp_moves, blanks)
    opp_board_value = score_board_distance(opp_distance_map)

    return float(board_value - opp_board_value)


def build_map(moves: List[Move], blanks: List[Move]) -> List[List[int]]:
    """
    Build a map of how many turns each square is away from the current
    players board position, starting with an empty board and assigning
    a number on each reachable square
    """
    depth = 1
    board = copy.deepcopy(EMPTY_BOARD)
    start_moves = set(moves)
    while len(start_moves) > 0:
        new_moves = set()  # type: Set[Move]
        for move in start_moves:
            if move in blanks and board[move[0]][move[1]] == 0:
                board[move[0]][move[1]] = depth
                new_possibles = set([(move[0] + direction[0],
                                      move[1] + direction[1])
                                     for direction in DIRECTIONS])
                new_moves = new_moves | new_possibles
        start_moves = possible_moves(new_moves)
        depth = depth + 1
    return board


def possible_moves(moves: Set[Move]) -> Set[Move]:
    """
    Reduce a set of moves down to ones which are within the proximity
    of the board
    """
    valid_moves = []
    for move in moves:
        if move[0] in DIMENSIONS and move[1] in DIMENSIONS:
            valid_moves.append(move)
    return set(valid_moves)


def score_board_distance(distance_map: List[List[int]]) -> int:
    """
    Score the entire board based on the mappings between number of moves
    to a square and the value of squares at that distance
    """
    distances = reduce(lambda x, y: x + y, distance_map)
    value = 0
    for distance in distances:
        if distance < len(SCORING_VALUES):
            value = value + SCORING_VALUES[distance]
    return value


def build_wall(game: Board, player: Player) -> float:
    """
    Encourage the player to go the middle row and column of the board
    to increase the chances of a partition in the later game
    """

    position = game.get_player_location(player)
    blanks = game.get_blank_spaces()
    blank_vertical = [loc for loc in blanks
                      if position[1] == 3]
    blank_horizontal = [loc for loc in blanks
                        if position[0] == 3]

    vertical = len(blank_vertical)
    horizontal = len(blank_horizontal)

    if position == (3, 3):
        return max(vertical, horizontal)
    elif position[0] == 3:
        return horizontal
    elif position[1] == 3:
        return vertical
    else:
        return 0


def rush_middle(game: Board, player: Player) -> float:
    """
    Encourage the player to go to the center of the board giving the middle
    100 bonus points and the squares around the middle 50 bonus points
    """
    loc = game.get_player_location(player)
    center = (3, 3)
    middle = {2, 3, 4}
    if loc == center:
        return 100
    elif loc[0] in middle and loc[1] in middle:
        return 50
    else:
        return 0


def block_move(game: Board, player: Player) -> float:
    """
    Encourage moves which happen to block one of the possible moves of the
    opponent on their next turn
    """
    loc = game.get_player_location(player)
    opp = game.get_player_location(game.get_opponent(player))

    for dir in DIRECTIONS:
        if (loc[0] + dir[0], loc[1] + dir[1]) == opp:
            return 1.

    return 0.


def clover_leaf(game: Board, player: Player) -> float:
    """
    Encourage moves which happen to block one of the possible moves of the
    opponent in two turns
    """
    loc = game.get_player_location(player)
    opp = game.get_player_location(game.get_opponent(player))
    for leaf in CLOVER:
        if (opp[0] + leaf[0], opp[1] + leaf[1]) == loc:
            return 1.
    return 0.


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, search_depth: int=3, score_fn: Heuristic=custom_score,
                 iterative: bool=True, method: str='minimax',
                 timeout: float=10.) -> None:
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = Timer
        self.timer_threshold = timeout
        self.average_depths = []  # type: List[int]
        self.name = "computer"

    def get_move(self, game: Board, legal_moves: List[Move],
                 time_left: Timer) -> Move:
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            logging.info('Computer Player has no more legal moves')
            return (-1, -1)

        best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        best_score = float("-inf")

        max_depth = game.width * game.height - game.move_count

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method is 'minimax':
                search = self.minimax
            elif self.method is 'alphabeta':
                search = self.alphabeta

            if self.iterative:
                current_depth = 1
                while current_depth <= max_depth:
                    score, move = search(game, current_depth)
                    if (score, move) > (best_score, best_move):
                        best_score, best_move = score, move
                    current_depth = current_depth + 1
            else:
                current_depth = self.search_depth
                best_score, best_move = search(game, self.search_depth)
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass
        self.average_depths.append(current_depth)
        return best_move

    def minimax(self, game: Board, depth: int,
                maximizing_player: bool=True) -> Tuple[float, Move]:
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        if self.time_left() < self.timer_threshold:
            raise Timeout()

        best_move = (-1, -1)
        best_score = float("-inf") if maximizing_player else float("inf")
        comparison = max if maximizing_player else min

        if depth is 0:
            return self.score(game, self), best_move

        for move in game.get_legal_moves():
            score, _ = self.minimax(
                game.forecast_move(move), depth - 1, not maximizing_player)
            best_score, best_move = comparison(
                (best_score, best_move), (score, move))

        return best_score, best_move

    def alphabeta(self, game: Board, depth: int,
                  alpha: float=float("-inf"), beta: float=float("inf"),
                  maximizing_player: bool=True) -> Tuple[float, Move]:
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.timer_threshold:
            raise Timeout()

        best_move = (-1, -1)
        best_score = alpha if maximizing_player else beta
        if depth is 0:
            return self.score(game, self), best_move

        for move in game.get_legal_moves():
            future_game = game.forecast_move(move)
            score, _ = self.alphabeta(future_game, depth - 1,
                                      alpha, beta, not maximizing_player)
            if maximizing_player:
                if score > best_score:
                    best_score, best_move = score, move
                if best_score >= beta:
                    return best_score, best_move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score, best_move = score, move
                if best_score <= alpha:
                    return best_score, best_move
                beta = min(beta, best_score)

        return best_score, best_move
