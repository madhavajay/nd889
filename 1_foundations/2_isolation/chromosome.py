# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 2 - Build a Game-Playing Agent"""

import copy
from functools import reduce
from typing import NamedTuple, Callable, Any, Tuple

from isolation import Board

# player has no real type so we will use Any
Player = Any
Move = Tuple[int, int]
Timer = Callable[[], int]
Heuristic = Callable[[Board, Player], float]


BOARD_VALUE = {(0, 0): 1, (0, 1): 2, (0, 2): 2, (0, 3): 2, (0, 4): 2, (0, 5): 2, (0, 6): 1, (1, 0): 2, (1, 1): 3, (1, 2): 4, (1, 3): 4, (1, 4): 4, (1, 5): 3, (1, 6): 2, (2, 0): 2, (2, 1): 4, (2, 2): 5, (2, 3): 5, (2, 4): 5, (2, 5): 4, (2, 6): 2, (3, 0): 2, (3, 1): 4, (3, 2): 5, (3, 3): 6, (3, 4): 5, (3, 5): 4, (3, 6): 2, (4, 0): 2, (4, 1): 4, (4, 2): 5, (4, 3): 5, (4, 4): 5, (4, 5): 4, (4, 6): 2, (5, 0): 2, (5, 1): 3, (5, 2): 4, (5, 3): 4, (5, 4): 4, (5, 5): 3, (5, 6): 2, (6, 0): 1, (6, 1): 2, (6, 2): 2, (6, 3): 2, (6, 4): 2, (6, 5): 2, (6, 6): 1}
BOARD_PROXIMITY = {(0, 0): [(1, 2), (2, 1)], (0, 1): [(1, 3), (2, 0), (2, 2)], (0, 2): [(1, 0), (1, 4), (2, 1), (2, 3)], (0, 3): [(1, 1), (1, 5), (2, 2), (2, 4)], (0, 4): [(1, 2), (1, 6), (2, 3), (2, 5)], (0, 5): [(1, 3), (2, 4), (2, 6)], (0, 6): [(1, 4), (2, 5)], (1, 0): [(0, 2), (2, 2), (3, 1)], (1, 1): [(0, 3), (2, 3), (3, 0), (3, 2)], (1, 2): [(0, 0), (0, 4), (2, 0), (2, 4), (3, 1), (3, 3)], (1, 3): [(0, 1), (0, 5), (2, 1), (2, 5), (3, 2), (3, 4)], (1, 4): [(0, 2), (0, 6), (2, 2), (2, 6), (3, 3), (3, 5)], (1, 5): [(0, 3), (2, 3), (3, 4), (3, 6)], (1, 6): [(0, 4), (2, 4), (3, 5)], (2, 0): [(0, 1), (1, 2), (3, 2), (4, 1)], (2, 1): [(0, 0), (0, 2), (1, 3), (3, 3), (4, 0), (4, 2)], (2, 2): [(0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3)], (2, 3): [(0, 2), (0, 4), (1, 1), (1, 5), (3, 1), (3, 5), (4, 2), (4, 4)], (2, 4): [(0, 3), (0, 5), (1, 2), (1, 6), (3, 2), (3, 6), (4, 3), (4, 5)], (2, 5): [(0, 4), (0, 6), (1, 3), (3, 3), (4, 4), (4, 6)], (2, 6): [(0, 5), (1, 4), (3, 4), (4, 5)], (3, 0): [(1, 1), (2, 2), (4, 2), (5, 1)], (3, 1): [(1, 0), (1, 2), (2, 3), (4, 3), (5, 0), (5, 2)], (3, 2): [(1, 1), (1, 3), (2, 0), (2, 4), (4, 0), (4, 4), (5, 1), (5, 3)], (3, 3): [(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)], (3, 4): [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 3), (5, 5)], (3, 5): [(1, 4), (1, 6), (2, 3), (4, 3), (5, 4), (5, 6)], (3, 6): [(1, 5), (2, 4), (4, 4), (5, 5)], (4, 0): [(2, 1), (3, 2), (5, 2), (6, 1)], (4, 1): [(2, 0), (2, 2), (3, 3), (5, 3), (6, 0), (6, 2)], (4, 2): [(2, 1), (2, 3), (3, 0), (3, 4), (5, 0), (5, 4), (6, 1), (6, 3)], (4, 3): [(2, 2), (2, 4), (3, 1), (3, 5), (5, 1), (5, 5), (6, 2), (6, 4)], (4, 4): [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)], (4, 5): [(2, 4), (2, 6), (3, 3), (5, 3), (6, 4), (6, 6)], (4, 6): [(2, 5), (3, 4), (5, 4), (6, 5)], (5, 0): [(3, 1), (4, 2), (6, 2)], (5, 1): [(3, 0), (3, 2), (4, 3), (6, 3)], (5, 2): [(3, 1), (3, 3), (4, 0), (4, 4), (6, 0), (6, 4)], (5, 3): [(3, 2), (3, 4), (4, 1), (4, 5), (6, 1), (6, 5)], (5, 4): [(3, 3), (3, 5), (4, 2), (4, 6), (6, 2), (6, 6)], (5, 5): [(3, 4), (3, 6), (4, 3), (6, 3)], (5, 6): [(3, 5), (4, 4), (6, 4)], (6, 0): [(4, 1), (5, 2)], (6, 1): [(4, 0), (4, 2), (5, 3)], (6, 2): [(4, 1), (4, 3), (5, 0), (5, 4)], (6, 3): [(4, 2), (4, 4), (5, 1), (5, 5)], (6, 4): [(4, 3), (4, 5), (5, 2), (5, 6)], (6, 5): [(4, 4), (4, 6), (5, 3)], (6, 6): [(4, 5), (5, 4)]}
INF = float("inf")
NEGINF = float("-inf")

GENES = {
    'board_value': [0.] * 6,
    'moves_diff': 1.,
    'pos_diff': 1.,
    'block_bonus': 1.
}

class Chromosome(NamedTuple):
    name: str
    score: float
    generations: int
    age: int
    genes: dict
    mutation_rates: dict


def score_chromosome(chromesome) -> Heuristic:
    def score(game: Board, player: Player) -> float:
        # get moves
        own_moves = game.get_legal_moves(player)

        # loser
        if player == game.active_player and not own_moves: return NEGINF

        # get opp moves
        opp = game.get_opponent(player)
        opp_moves = game.get_legal_moves(opp)

        # winner
        if player == game.inactive_player and not opp_moves: return INF

        moves_diff = (len(own_moves) - len(opp_moves))
        loc = game.get_player_location(player)
        opp_loc = game.get_player_location(opp)
        pos_value = chromesome.genes['board_value'][BOARD_VALUE[loc] - 1]
        opp_pos_value = chromesome.genes['board_value'][BOARD_VALUE[opp_loc] - 1]
        pos_value_diff = pos_value - opp_pos_value
        block_bonus = 1 if opp in BOARD_PROXIMITY[loc] else 0

        return float(
            (moves_diff * chromesome.genes['moves_diff']) +
            (pos_value_diff * chromesome.genes['pos_diff']) +
            (block_bonus * chromesome.genes['block_bonus'])
        )

    return score
