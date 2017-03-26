# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from util import Stack, Queue, PriorityQueue, PriorityQueueWithFunction
from util import manhattanDistance

from typing import NamedTuple, Tuple, List, Any


class Node:
  def __init__(self, state: Tuple[int, int], action: str, cost: int, parent: Any):
    self.state = state
    self.action = action
    if parent:
      self.cost = cost + parent.cost
    else:
      self.cost = 0
    self.parent = parent

  def parent_state(self):
    if self.parent:
      return self.parent.state
    return None

  def get_path(self):
    path = []
    node = self
    while node.parent_state():
      path.append(node.action)
      node = node.parent

    return list(reversed(path))

  def __eq__(self, other):
    if not isinstance(other, Node):
        return NotImplemented
    return (
      self.state == other.state and
      self.action == other.action and
      self.cost == other.cost and
      self.parent_state() == other.parent_state()
    )

  def __ne__(self, other):
    return not self.__eq__(other)

  def __lt__(self, other):
    return self.cost < other.cost

  def __gt__(self, other):
    return self.cost > other.cost

  def __hash__(self):
    return hash(tuple(sorted(self.__dict__.items())))

  def __str__(self):
    return f'{self.state} {self.action} {self.cost} {self.parent_state()}'


class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


def graph_search(problem, frontier) -> List[str]:
  explored = set()
  while not frontier.isEmpty():
    node = frontier.pop()
    if problem.isGoalState(node.state):
      return node.get_path()
    if node.state not in explored:
      explored.add(node.state)
      children = problem.getSuccessors(node.state)
      for child in children:
        child_node = Node(child[0], child[1], child[2], node)
        if child_node.state not in explored:
          if isinstance(frontier, PriorityQueueWithFunction):
            frontier.push(child_node)
          elif isinstance(frontier, PriorityQueue):
            frontier.push(child_node, child_node.cost)
          else:
            frontier.push(child_node)

  return []

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  node = Node(problem.getStartState(), None, 0, None)
  if problem.isGoalState(node.state):
    return node.get_path()

  frontier = Stack()
  frontier.push(node)
  result = graph_search(problem, frontier)
  return result

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  node = Node(problem.getStartState(), None, 0, None)
  if problem.isGoalState(node.state):
    return node.get_path()

  frontier = Queue()
  frontier.push(node)
  return graph_search(problem, frontier)

def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  node = Node(problem.getStartState(), None, 0, None)
  if problem.isGoalState(node.state):
    return node.get_path()

  frontier = PriorityQueue()
  frontier.push(node, 0)
  return graph_search(problem, frontier)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def manhattanHeuristic(state, problem=None):
  return manhattanDistance(state, problem.goal)

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  node = Node(problem.getStartState(), None, 0, None)
  if problem.isGoalState(node.state):
    return node.get_path()

  def wrapper(node):
    return heuristic(node.state, problem)

  frontier = PriorityQueueWithFunction(wrapper)
  frontier.push(node)
  return graph_search(problem, frontier)

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
