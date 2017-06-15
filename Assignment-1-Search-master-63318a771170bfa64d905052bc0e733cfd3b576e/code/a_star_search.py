
"""
    Enter your details below:

    Name:Taku Ueki
    Student Code:u5934839
    email:u5934839@anu.edu.au
"""

import util
from actions import Directions, Actions
from search_strategies import SearchNode
from frontiers import Queue, Stack, PriorityQueue
import heuristics
def solve(problem, heuristic) :
    """ *** YOUR CODE HERE *** """
    # util.raise_not_defined() #Remove this line when you have implemented BrFS

    frontier = PriorityQueue()
    s0 = problem.get_initial_state()
    closedSet = set()
    # closedSet.add(s0)
    openSet = set()
    openSet.add(s0)
    sn_root = SearchNode(s0)
    frontier.push(sn_root, heuristic(s0,problem))
    gScore = {}
    gScore[s0] = 0

    check = None
    while not frontier.is_empty():
        current_node = frontier.pop()
        # print(current_node.path_cost + heuristic(current_node.state,problem))
        closedSet.add(current_node.state)
        openSet.discard(current_node.state)
        check = check_goal(current_node, problem)

        if check == None:
            for successor, action, cost in problem.get_successors(current_node.state):
                if successor not in closedSet:
                    tentative_gScore = current_node.path_cost + cost
                    if successor not in openSet:
                        openSet.add(successor)
                    #if there is a path that can be reached to this node more efficiently, discard this successor
                    elif tentative_gScore >= gScore[successor]:
                        continue
                    gScore[successor] = tentative_gScore
                    sn = SearchNode(successor, action, tentative_gScore, current_node, current_node.depth + 1)
                    # push this node to the Queue with gScore and hScore(caluculated by heuristic function)
                    frontier.push(sn, sn.path_cost + heuristic(successor,problem))
                    # total = sn.path_cost + heuristic(successor,problem)
                    # print(str(current_node.state) + "TO" + str(successor) + " path_cost=" + str(sn.path_cost) + " heuristic=" + str(heuristic(successor,problem)) + " total=" + str(total))
        else:
            return check


def check_goal(sn, problem):

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
        return None
