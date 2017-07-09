# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""nd889 AIND Project 2 - Build a Game-Playing Agent"""

import random
import uuid
import time
import pickle
import copy
import os.path
import multiprocessing
from multiprocessing import Pool
from typing import NamedTuple, Callable, Any, Tuple

from tournament import *
from chromosome import *


MAX_POPULATION = 100


def fitness(fighter) -> float:

    """
    Play one round (i.e., a single match between each pair of opponents)
    """
    CUSTOM_ARGS = {"method": 'alphabeta', 'iterative': True}
    player_1 = CustomPlayer(score_fn=score_chromosome(fighter), **CUSTOM_ARGS)
    agent_1 = Agent(player_1, fighter.name)
    id_improved = CustomPlayer(score_fn=improved_score, **CUSTOM_ARGS)
    agent_2 = Agent(id_improved, "AB_Improved")

    agent_1_wins = 0.
    agent_2_wins = 0.
    total = 0.
    num_matches = 5

    print("\nPlaying Matches:")
    print("----------")

    counts = {agent_1.player: 0., agent_2.player: 0.}
    names = [agent_1.name, agent_2.name]
    print("  Match {}: {!s:^11} vs {!s:^11}".format(1, *names), end=' ')

    # Each player takes a turn going first
    for _ in range(num_matches):
        score_1, score_2 = play_match(agent_1.player, agent_2.player)
        counts[agent_1.player] += score_1
        counts[agent_2.player] += score_2
        total += score_1 + score_2

    agent_1_wins += counts[agent_1.player]
    agent_2_wins += counts[agent_2.player]

    searches_1 = len(agent_1.player.average_depths)
    total_depth_1 = sum(agent_1.player.average_depths)
    avg_1 = total_depth_1 / searches_1

    searches_2 = len(agent_2.player.average_depths)
    total_depth_2 = sum(agent_2.player.average_depths)
    avg_2 = total_depth_2 / searches_2

    print("\nResults {}: {} Avg Depth: {} vs {}: {} Avg Depth: {}".format(
        agent_1.name, int(counts[agent_1.player]), avg_1,
        agent_2.name, int(counts[agent_2.player]), avg_2
    ))

    agent_1_score = 100. * agent_1_wins / total
    return update_score(fighter, agent_1_score)


def update_age(chromosome, age):
    return Chromosome(
        chromosome.name,
        chromosome.score,
        chromosome.generations,
        age,
        chromosome.genes,
        chromosome.mutation_rates)


def update_score(chromosome, score):
    return Chromosome(
        chromosome.name,
        score,
        chromosome.generations,
        chromosome.age,
        chromosome.genes,
        chromosome.mutation_rates)


def random_mutation_rate():
    return random.uniform(0.5, 1)


def random_weight():
    return random.uniform(0, 1)


def get_random_chromosome():
    genes = {}
    mutations = {}
    for key, value in GENES.items():
        if type(value) is list:
            gene = list(value)
            mutation = list(value)
            for i in range(len(gene)):
                gene[i] = random_weight()
                if key == 'board_value':
                    gene[i] = (i + 1) * random_weight()
                mutation[i] = random_mutation_rate()
        elif type(value) is float:
            gene = random_weight()
            mutation = random_mutation_rate()

        genes[key] = gene
        mutations[key] = mutation

    return Chromosome(
        uuid.uuid4().hex, -1, 0, 0,
        genes, mutations
    )


def get_random_population(num=MAX_POPULATION):
    chromosomes = []
    for i in range(num):
        chromosomes.append(get_random_chromosome())
    return chromosomes


def select_breeders(fighters):
    sorted_heroes = sorted(fighters, key=lambda chromosome: chromosome.score)
    sorted_heroes = list(reversed(sorted_heroes))
    return sorted_heroes[:45]


def age_population(chromosomes):
    aged = []
    for chromosome in chromosomes:
        aged.append(update_age(chromosome, chromosome.age + 1))

    return aged


def evolve(gene, gene_mutation):
    if type(gene) is float:
        if random.random() > gene_mutation:
            gene = gene * random.uniform(0.75, 1.25)

        if random.random() > 0.9:
            gene_mutation = gene_mutation * random.uniform(0.75, 1.25)

    elif type(gene) is list:
        new_gene = copy.deepcopy(gene)
        new_mutation = copy.deepcopy(gene_mutation)
        for i in range(len(new_gene)):
            if random.random() > gene_mutation[i]:
                new_gene[i] = gene[i] * random.uniform(0.75, 1.25)
            if random.random() > 0.9:
                new_mutation[i] = gene_mutation[i] * random.uniform(0.75, 1.25)

        gene = new_gene
        gene_mutation = new_mutation

    return gene, gene_mutation


def make_child(chromosome):

    new_genes = copy.deepcopy(chromosome.genes)
    new_mutations = copy.deepcopy(chromosome.mutation_rates)
    for key, value in new_genes.items():
        gene, mutation = evolve(value, new_mutations[key])
        new_genes[key] = gene
        new_mutations[key] = mutation

    child = Chromosome(
        uuid.uuid4().hex, -1, chromosome.generations + 1, 0,
        new_genes, new_mutations
    )

    return child


def average_score(chromosomes):
    all_scores = sum([chromosome.score for chromosome in chromosomes])
    return all_scores / len(chromosomes)


def breed(chromosomes):
    children = []
    for chromosome in chromosomes:
        children.append(make_child(chromosome))

    return children + chromosomes


def main():
    oldest_generation = 0
    generations = 1

    population = get_random_population()
    last_generation = None
    print('Trying to load last generation')
    save_file = 'last_generation.pickle'
    if os.path.isfile(save_file):
        last_file = open(save_file, 'rb')
        last_generation = pickle.load(last_file)

    if last_generation:
        population = last_generation
        print('Loading previous Generation {}'.format(last_generation))

    processes = multiprocessing.cpu_count()
    pool = Pool(processes=processes)
    start_time = time.time()
    for generation in range(generations):
        trained = pool.map(fitness, population)
        breeders = select_breeders(trained)
        breeders = age_population(breeders)
        new_population = breed(breeders)
        new_population = new_population + get_random_population(10)
        print('Generation {} {}'.format(generation, new_population))

        new_average = average_score(new_population)
        population = new_population
        highest = 0
        highest_fighter = None
        for pop in population:
            if pop.score > highest:
                highest = pop.score
                highest_fighter = pop
            if oldest_generation < pop.generations:
                oldest_generation = pop.generations
        print('Highest Score {} Average {} Oldest Gen {}'.format(
            highest, new_average, oldest_generation))
        print('Best Fighter Score {} Age {}'.format(
            highest_fighter.score, highest_fighter.age))
        print('Best Chromosome Fighter {}'.format(highest_fighter))
        fighter_file = 'latest_fighter_{}.pickle'
        protocol = pickle.HIGHEST_PROTOCOL
        with open(fighter_file.format(int(start_time)), 'wb') as handle:
            pickle.dump(highest_fighter, handle, protocol=protocol)
        with open('last_generation.pickle', 'wb') as handle:
            pickle.dump(population, handle, protocol=protocol)
    end_time = time.time()
    print('Total time for {} Generations: {}'.format(
        generations, end_time - start_time))


if __name__ == "__main__":
    main()
