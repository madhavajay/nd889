# Udacity - Artificial Intelligence Nanodegree - nd889

# Heuristics Analysis

The "improved_score" heuristics simply takes the number of available moves for both players and diffs them.

Since the game is a zero sum game and losing means having no where to move, it makes sense that the difference in available moves would be a valuable metric.

The first few ideas I had were naive and attempted to manipulate combinations of the available game state properties or variations on "improved_score" using different weights.

None of these strategies provided any meaningful scores so I decided to take another approach.

![Paper Game](img/paper.jpg)

I played a few games and realized a few things about the game.

* The distance between squares is not what I expected, particularly when a player is in the corner

* The center of the board is quite different to the edges

* You can't win if you can't move so ultimately having options to move is important

* Partitions can happen, but are hard due to the jumping nature of the knights but this could be something to explore

My first new heuristic was called **rush_middle** and it's goal was to increase the weighting of squares in the middle of the board.

After that the next heuristic I made was called **build_wall** with the purpose of returning higher values if the current position is in the center row or column.

It was interesting that the basic heuristic of (players valid moves - opponents moves) was so effective, so I decided to play the game some more and consider the knights movement and the relationship between the distance from each square to the other squares on the board.

## Game Play
To help gaining insight by playing the game I made some adjustments to the board printing method to add the rows and columns, colors and to show the current valid moves as well as showing which moves both players can move to.

![Computer Game](img/play.jpg)

Unfortunately, after many manual games I still couldn't find a reliable way to beat the AI.

## More Heuristics

It seemed like blocking an opponent might be a good idea, so I tried a heuristic called **block_move** which checked if any of the available moves were also valid for the opponent.

I also considered a level past this called **clover_leaf** which checks if the move would block the opponent after their next valid move, which happens if you move to the diagonal square next to the other player. The diagonal squares form a kind of clover leaf hence the name.

While waiting for tournament runs I was doodling on paper and it occurred to me to draw out the distance from every square to every other square out of interest.

![Distance](img/distance.jpg)

This lead me to the heuristic **plane_walker** which attempts to map out the distance to every square on the board which is reachable and blank.

This acts a little bit like a tree search except that each square is only considered once and the different distances can have varying values applied to them.

Interestingly I seem to be able to sometimes beat improved_score with a lower average depth which suggests that the heuristic is smarter but slower.


## Ensemble

I attempted to combine some of my heuristics into an ensemble, however manually tweaking weights for each heuristic was taking too long so I looked for an alternative solution.

## Genetic Algorithms

Hoping to improve some of my heuristics I wrote some genetic algorithm code to attempt to vary and mutate various weights for different heuristics in various combinations.

The code created a population of 100 chromosomes with random weights and then ran them against a modified version of the tournament where they only played an opponent with Alpha Beta pruning and improved_score.

After each generation the top scoring 45 were kept and cloned with a random chance of mutation, and 10 new random mutants were added to the population.

I ran various different versions of the code for several nights on a 16 core machine with python multiprocessing Pool but the results never managed to approach the improved_score.

I believe that either the heuristics were never capable of achieving a strong enough performance or there were some issues with the genetic algorithm code or a combination of both. It was however a fun learning experience.

A version of the genetic algorithm code can be found in **pit.py**

## Performance
heuristic | ID % | ID Avg Depth | Student % | Student Avg Depth
-----------|-------|-------|---------|-------|
build_wall | 75.71% | 12.38 | 61.43% | 11.50
rush_middle | 75.00% | 12.22 | 78.57% | 12.57
block_move | 80.71% | 12.17 | 64.29% | 11.37
clover_leaf | 80.71% | 12.18 | 61.43% | 11.34
plane_walker | 75.71% | 12.37 | 80.00 | 10.46
ensemble | 80.71% | 12.20 | 72.86% | 9.27

## Results
Even though I was able to get a run where **plane_walker** and **rush_middle** beat improved_score when running for much bigger tournaments those advantages evened out. I figure this is because what **plane_walker** does is essentially just continuing the tree search in the heuristic so its not really any different. While **rush_middle** keeps the player centered which also often results in more move choices.

I noticed there seemed to be a relationship between the average depth reached for a given heuristic and the performance of that heuristic.

This would make sense as too much time wasted in each evaluation over the entire iterative search could lessen the depth significantly.

Currently I must recommend the supplied improved_score heuristic as it has the most consistently high score and reaches a higher average depth than most of the other heuristics.

## Future Ideas

For the future I would like to explore the relationship between the distances on the board and the available paths using a graph system, I think this might be much more efficient and provide some new interesting ways of viewing the problem.

I also think some of these simpler heuristics might be able to be combined together to into an ensemble and optimal weights could be discovered using something like a genetic algorithm.

In addition I get the feeling that there are phases of the game and taking into account the move_count might provide some additional gains.
