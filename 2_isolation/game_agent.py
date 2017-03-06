# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 2 - Isolation"""

import random
import copy
from functools import reduce
from typing import Any, Callable, Tuple, List

from isolation import Board
from sample_players import improved_score

# player has no real type so we will use Any
Player = Any
Move = Tuple[int, int]
Timer = Callable[[], int]
Heuristic = Callable[[Board, Player], float]


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
    return improved_score(game, player)


EMPTY_BOARD = [[0 for x in range(7)] for y in range(7)]
SCORING_VALUES = [0, 5, 4, 3, 2, 1]
DIMENSIONS = {0, 1, 2, 3, 4, 5, 6}
DIRECTIONS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]


def plane_walker(game: Board, player: Player) -> float:
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blanks = game.get_blank_spaces()

    moves = game.get_legal_moves(player)
    distance_map = build_map(moves, blanks)
    board_value = score_board_distance(distance_map)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_distance_map = build_map(opp_moves, blanks)
    opp_board_value = score_board_distance(opp_distance_map)

    return float(board_value - opp_board_value)


def build_map(moves, blanks):
    depth = 1
    board = copy.deepcopy(EMPTY_BOARD)
    start_moves = set(moves)
    while len(start_moves) > 0:
        new_moves = set()
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


def possible_moves(moves):
    valid_moves = []
    for move in moves:
        if move[0] in DIMENSIONS and move[1] in DIMENSIONS:
            valid_moves.append(move)
    return valid_moves


def score_board_distance(distance_map):
    distances = reduce(lambda x, y: x + y, distance_map)
    value = 0
    for distance in distances:
        if distance < len(SCORING_VALUES):
            value = value + SCORING_VALUES[distance]
    return value


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
        self.time_left = None  # type: Timer
        self.timer_threshold = timeout

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
            return (-1, -1)

        best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        best_score = float('-inf')

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method is 'minimax':
                search = self.minimax
            elif self.method is 'alphabeta':
                search = self.alphabeta

            depth = self.search_depth
            if self.iterative:
                depth = 1

            while True:
                score, move = search(game, depth)

                if (score, move) > (best_score, best_move):
                    best_score, best_move = score, move

                if depth == self.search_depth:
                    break
                else:
                    depth = depth + 1
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

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
