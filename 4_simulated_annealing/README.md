## Udacity - Artificial Intelligence Nanodegree - nd889

# Lab: Simulated Annealing

This lab covers Simulated Annealing to provide fast optimal solutions to the Travelling Salesman problem.

![Simulated Annealing](img/SA_animation.gif)

## What I learned
Simulated Annealing is easy to implement and uses a schedule function which returns a decaying temperature by time unit. While the default implementation uses a shuffling, for every n nodes in the graph, n combinations are created where neighbours are swapped. Changing this to a successor function where any two random nodes are swapped seems to perform better, perhaps because during high tempratures problematic node positions can be relocated much further quicker.

## Instructions
```
$ jupyter notebook simulated_annealing.ipynb
```