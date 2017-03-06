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


BOARD_SIZE = 7
EMPTY_BOARD = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
DIRECTIONS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2),  (1, 2), (2, -1),  (2, 1)]
DIMENSIONS = {i for i in range(BOARD_SIZE)}
MAX_SCORING_DISTANCE = 5
GENES = {
    'scoring_values': [0] * 15
}


class Chromosome(NamedTuple):
    name: str
    score: float
    generations: int
    age: int
    genes: dict
    mutation_rates: dict


def score_board_distance(distance_map, scoring_values):
    distances = reduce(lambda x, y: x + y, distance_map)
    value = 0
    for distance in distances:
        if distance < MAX_SCORING_DISTANCE:
            if distance != 0:
                value = value + scoring_values[distance - 1]
    return value


def possible_moves(moves):
    valid_moves = []
    for move in moves:
        if move[0] in DIMENSIONS and move[1] in DIMENSIONS:
            valid_moves.append(move)
    return valid_moves


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


def plane_walker(game, player, scoring_values):
    blanks = game.get_blank_spaces()

    moves = game.get_legal_moves(player)
    distance_map = build_map(moves, blanks)
    board_value = score_board_distance(distance_map, scoring_values)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_distance_map = build_map(opp_moves, blanks)
    opp_board_value = score_board_distance(opp_distance_map, scoring_values)

    return float(board_value - opp_board_value)


def score_chromosome(chromesome) -> Heuristic:
    def score(game: Board, player: Player) -> float:
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        plane_walker_score = plane_walker(game, player,
                                          chromesome.genes['scoring_values'])

        return plane_walker_score

    return score
