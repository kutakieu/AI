"""
    Enter your details below:

    Name:Taku Ueki
    Student Code:u5934839
    email:u5934839@anu.edu.au
"""

import util
from actions import Directions, Actions
from search_strategies import SearchNode
from frontiers import Queue, Stack

def solve(problem) :
    """ *** YOUR CODE HERE *** """
    # util.raise_not_defined() #Remove this line when you have implemented BrFS

    #iterative implementation of BFS
    frontier = Queue()
    s0 = problem.get_initial_state()
    explored = set()
    explored.add(s0)
    sn_root = SearchNode(s0)
    frontier.push(sn_root)
    check = None
    while not frontier.is_empty():
        current_node = frontier.pop()
        explored.add(current_node.state)
        check = check_goal(current_node, problem)
        if check == None:
            for successor, action, cost in problem.get_successors(current_node.state):
                if successor not in explored:
                    sn = SearchNode(successor, action, cost, current_node, current_node.depth + 1)
                    frontier.push(sn)
        else:
            return check


def check_goal(sn, problem):
#take a SearchNode as an argument. If the SearchNode is the goal, return the path from the start node to goal node.
    if problem.goal_test(sn.state):
        path = []
        stack = Stack()
        stack.push(sn.action)
        while sn.parent != None:
            stack.push(sn.parent.action)
            sn = sn.parent
        while not stack.is_empty():
            path.append(stack.pop())
        return path[1:]
    else:
        #if the SearchNode given as an argument is not the goal return None instead of the path to the goal
        return None
