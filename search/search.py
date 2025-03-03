# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import *

import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # Create stack for node expansion
    # Create set of expanded nodes
    # Create actions dictionary
    # create parentPath dictionary
    #
    # NEED TO MAKE SURE A STRAIGHT PATH TO THE GOAL IS LEFT IN A LIST
    #
    # Push the starting value onto stack
    # Add starting value to list
    #
    # While there are values in the stack,
        # Pop value from stack
        # If value is goal,
            # return the path to the goal using parentPath and actions dictionaries
        # Else,
            # for each successor of value,
                # If successor is not in expanded list,
                    # Push to stack
                    # Add to expanded list
                    # Add successor and parent to parentPath
                    # Add parent to successor action to actions
                    # LOGS EVERY PATH TRAVELED IN A DICTIONARY MAP
                # Else
                    # Skip successor

    stateStack = Stack()
    expanded = set()
    actions = {}
    parentMap = {}

    # Initialize stack with starting position
    startState = problem.getStartState()
    stateStack.push(startState)

    while not stateStack.isEmpty():
        # Pop state
        currState = stateStack.pop()

        # If goal is reached, construct path
        if problem.isGoalState(currState):
            path = []
            while currState in parentMap:
                path.append(actions[currState])
                currState = parentMap[currState]
            path.reverse()
            return path

        # If already expanded, skip
        if currState in expanded:
            continue

        # Mark as expanded
        expanded.add(currState)

        # Expand children in correct order (Up, Down, Right, Left)
        for successor, action, _ in reversed(problem.getSuccessors(currState)):  # Reverse for correct DFS order
            if successor not in expanded:
                stateStack.push(successor)
                parentMap[successor] = currState
                actions[successor] = action

    return []



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    stateQueue = Queue()
    expanded = set()
    actions = {}
    parentMap = {}
    
    # Initialize stack with starting position
    startState = problem.getStartState()
    stateQueue.push(startState)

    # Add starting position to expanded set
    expanded.add(startState)
    
    # While the graph is not empty
    while not stateQueue.isEmpty():
        currState = stateQueue.pop()
        
        if problem.isGoalState(currState):
            # Try to construct a path to the goal
            path = []
            while currState != startState:
                path.append(actions[currState])
                currState = parentMap[currState]
            path.reverse()
            return path
        
        
        # Expand children
        for successor, action, empty in problem.getSuccessors(currState):
            # Check if we have expanded this node before
            if successor not in expanded:
                expanded.add(successor)
                stateQueue.push(successor)
                parentMap[successor] = currState  
                actions[successor] = action  
                
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    stateQueue = PriorityQueue()  # UCS uses a priority queue
    actions = {}
    parentMap = {}
    costs = {}

    # Initialize queue with starting position
    startState = problem.getStartState()
    stateQueue.push(startState, 0)
    costs[startState] = 0  # Cost to reach start state is 0

    while not stateQueue.isEmpty():
        # Pop state with lowest cost
        currState = stateQueue.pop()

        # If goal is reached, construct path
        if problem.isGoalState(currState):
            path = []
            while currState in parentMap:
                path.append(actions[currState])
                currState = parentMap[currState]
            path.reverse()
            return path

        # Expand children
        for successor, action, cost in problem.getSuccessors(currState):
            newCost = costs[currState] + cost  # Accumulate total cost

            # If successor has not been seen or we found a cheaper path
            if successor not in costs or newCost < costs[successor]:
                costs[successor] = newCost  # Update cost
                parentMap[successor] = currState  # Track parent
                actions[successor] = action  # Track action
                
                # Push or update the priority queue with the lower cost
                stateQueue.update(successor, newCost)

    return []  # If goal not found, return empty path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    stateQueue = PriorityQueue()  # UCS uses a priority queue
    actions = {}
    parentMap = {}
    costs = {}

    # Initialize queue with starting position
    startState = problem.getStartState()
    stateQueue.push(startState, 0)
    costs[startState] = 0  # Cost to reach start state is 0

    while not stateQueue.isEmpty():
        # Pop state with lowest cost
        currState = stateQueue.pop()

        # If goal is reached, construct path
        if problem.isGoalState(currState):
            path = []
            while currState in parentMap:
                path.append(actions[currState])
                currState = parentMap[currState]
            path.reverse()
            return path

        # Expand children
        for successor, action, cost in problem.getSuccessors(currState):
            newCost = costs[currState] + cost  # Accumulate total cost

            # If successor has not been seen or we found a cheaper path
            if successor not in costs or newCost < costs[successor]:
                costs[successor] = newCost  # Update cost
                parentMap[successor] = currState  # Track parent
                actions[successor] = action  # Track action
                
                # Push or update the priority queue with the lower cost
                stateQueue.update(successor, newCost + heuristic(successor, problem))

    return []  # If goal not found, return empty path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
