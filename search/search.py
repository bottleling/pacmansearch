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
    from util import Stack
    frontier=Stack()
    start_node = Node(problem.getStartState(), step_cost=0)
    explored = []
    frontier.push(start_node)
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node.state)
        if problem.isGoalState(node.state):
            return node.getPath()
        for child in node.getChildren(problem):
            if not child.state in explored:
                frontier.push(child)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    frontier=Queue()
    start_node = Node(problem.getStartState(), step_cost=0)
    explored = []
    frontier.push(start_node)
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node.state)
        if problem.isGoalState(node.state):
            return node.getPath()
        for child in node.getChildren(problem):
            h = isStateInList(frontier.list,child.state)
            if not child.state in explored and h == -1:
                frontier.push(child)

def isStateInList(queue,state):
    for i in range(0,len(queue)):
        if queue[i].state == state:
            return i
    return -1

def isStateInHeap(heap, state):
    for i in range(0,len(heap)):
        if heap[i][2].state == state:
            return i
    return -1

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    frontier=PriorityQueue()
    start_node = Node(problem.getStartState(), step_cost=0)
    explored = []
    frontier.push(start_node, start_node.path_cost)
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node.state)
        if problem.isGoalState(node.state):
            return node.getPath()
        for child in node.getChildren(problem):
            h = isStateInHeap(frontier.heap,child.state)
            if not child.state in explored and h == -1:
                frontier.push(child, child.path_cost)
            elif h > -1:
                if (frontier.heap[h][2].path_cost > child.path_cost):
                    frontier.heap.pop(h)
                    frontier.push(child, child.path_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    frontier=PriorityQueue()
    start_node = Node(problem.getStartState(), step_cost=0)
    explored = []
    frontier.push(start_node, start_node.path_cost+heuristic(problem.getStartState(),problem))
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node.state)
        if problem.isGoalState(node.state):
            return node.getPath()
        for child in node.getChildren(problem):
            h = isStateInHeap(frontier.heap,child.state)
            if not child.state in explored and h == -1:
                evaluation_cost=child.path_cost+heuristic(child.state,problem)
                frontier.push(child, evaluation_cost)
            elif h > -1:
                if (frontier.heap[h][2].path_cost > child.path_cost):
                    frontier.heap.pop(h)
                    frontier.push(child, child.path_cost)

class Node:
    def __init__(self, state, parent=None, action=None, step_cost=1):
        self.state = state
        self.parent= parent #parent node
        self.action=action #action on parent to get to this state
        if (parent !=None):
            self.path_cost = self.parent.path_cost + step_cost
        else:
            self.path_cost = step_cost

    def __repr__(self):
        s = "Node %s" % self.state
        return s

    def getChildren(self, problem): #from searchAgents
        successors = problem.getSuccessors(self.state)
        children = []
        for s in successors:
            node = Node(s[0],self,s[1],s[2])
            children.append(node)
        return children

    def getPath(self):
        current_node = self
        path = []
        while current_node:
            if current_node.parent:
                path.append(current_node.action)
            current_node = current_node.parent
        list.reverse(path)
        #print path
        return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
