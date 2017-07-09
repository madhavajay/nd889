## Udacity - Artificial Intelligence Nanodegree - nd889

# Lab: Teaching Pac-Man to Search

This Lab is from [UC Berkeley CS188 Intro to AI](http://ai.berkeley.edu/project_overview.html).

![Pac-Man](img/pacman_game.gif)

## 🐍 Python 3 Port
I ported the code to python 3.
To run it, I needed to install python 3 with tkinter support. 

On OS X:
```
$ brew install python3 --use-brewed-tk
```

## What I learned
I completed the first 6 questions in this lab. For this I was required to implement: 

* depth-first search
* breadth-first search
* uniform cost search
* A\* search
* A corner heuristic for pruning A\* search

Each algorithm utilized the same shared generic graph search method which utilized a queue, popped the head and checked for goal state, then explored the frontier pushing new child nodes which had not been visited before. The variation in search algorithms is entirely dependant on the queue type and optional priority queue function.

A\* Search is an effective best-first search algorithm combining the best of breadth-first / uniform cost search and a greedy best-first heuristic search using both known and estimated costs and priority queue which is continually attempting to visit the next best frontier node.

Unsurprisingly encoding complex goal states into heuristics is still necessary to find optimal solutions with minimal node expansion.

In the corner heuristic, I tracked the goal state as a set of remaining goal locations which allowed quick manhattan distance calculation to the remaining goals.

My code is in the following files:
* search.py
* searchAgents.py

## Instructions
Open search.html and run the commands for each question.
For example Question 1:
```
$ python pacman.py -l mediumMaze -p SearchAgent
```

## Questions and Results
Question | Algorithm | Points (Bonus) | Size | Path Cost | Nodes Expanded
---------|------|--------|------|-----------|---------------
1|DFS|2|Medium|130|146
2|BFS|2|Medium|68|269
3|UCS|2|Medium|68|270
4|A\*|3|Big|210|467
5|BFS|2|Medium|106|1966
6|A\* + heuristic|3 (+2)|Medium|108|171

