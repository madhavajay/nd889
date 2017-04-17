## Udacity - Artificial Intelligence Nanodegree - nd889

# Project 3: Implement a Planning Search

![Planning](img/statespace.png)

For the AIND Project 3 on planning we learnt the language of formal logic to describe and define complex planning problems and how they can be implemented as a graph. Once in graph form, solutions to planning problems can be found using many well known graph search algorithms.

## The Air Cargo Transport Problem
In the air cargo problem, there are three distinct variables, airports, planes and cargo. There are several states and actions available such as, cargo can either be at airports or in planes and be loaded or unloaded from planes, while planes are at an airport, but as an action can travel between airports. 

The problems begin with cargo and planes in an initial state and define which airport each piece of cargo should be at in the goal state.

Airports are defined by their 3 letter airport code such as SFO for San Francisco, cargo and planes are simply numbered C1, C2 and P1, P2 etc.

## Instructions
```
$ python run_search.py -m
```

## Additional Material

1. [Heuristics Analysis](heuristic_analysis.md)

2. [Research Review](research_review.md)