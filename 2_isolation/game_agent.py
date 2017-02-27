# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 2 - Isolation"""

from typing import Any, Callable, Tuple, List

from isolation import Board

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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


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
        if len(legal_moves) == 0:
            return (-1, -1)

        best_move = legal_moves[0]
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            depth = self.search_depth
            if self.iterative:
                depth = 1

            while depth > 0:
                if self.method == 'minimax':
                    _, best_move = self.minimax(game, depth)
                elif self.method == 'alphabeta':
                    _, best_move = self.alphabeta(game, depth)
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

        legal_moves = game.get_legal_moves()

        if depth == 0 or len(legal_moves) == 0:
            # at level 1 maximizing_player
            # at level 2 opponent
            if maximizing_player:
                player = game.active_player
            else:
                player = game.get_opponent(game.active_player)
            utility = self.score(game, player)
            return utility, (-1, -1)

        searches = []
        for move in legal_moves:
            future_game = game.forecast_move(move)
            val, _ = self.minimax(future_game, depth-1, not maximizing_player)
            searches.append((val, move))

        best = searches[0]
        for search in searches:
            if maximizing_player and search[0] > best[0]:
                best = search
            elif not maximizing_player and search[0] < best[0]:
                best = search

        return best

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

        legal_moves = game.get_legal_moves()

        if depth == 0 or len(legal_moves) == 0:
            if maximizing_player:
                player = game.active_player
            else:
                player = game.get_opponent(game.active_player)

            utility = self.score(game, player)
            return utility, (-1, -1)

        if maximizing_player:
            best = (float("-inf"), (-1, -1))
        else:
            best = (float("inf"), (-1, -1))

        for move in legal_moves:
            future_game = game.forecast_move(move)
            child = self.alphabeta(future_game, depth-1,
                                   alpha, beta, not maximizing_player)
            if maximizing_player:
                if child[0] > best[0]:
                    best = child[0], move
                if best[0] >= beta:
                    return best
                alpha = max(alpha, best[0])
            else:
                if child[0] < best[0]:
                    best = child[0], move
                if best[0] <= alpha:
                    return best
                beta = min(beta, best[0])

        return best
