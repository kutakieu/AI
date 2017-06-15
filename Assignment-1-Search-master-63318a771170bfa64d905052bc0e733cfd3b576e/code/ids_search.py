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

    depth_limit = 0
    s0 = problem.get_initial_state()
    sn_root = SearchNode(s0)

    check = None
    while True:
        frontier = Stack()
        frontier.push(sn_root)

        while not frontier.is_empty():

            current_node = frontier.pop()
            #check if this node is the goal or not
            check = check_goal(current_node, problem)

            if check != None:   #if check != None: reached goal, so "check" contains the path
                return check
            else:
                if(current_node.depth == depth_limit):
                    continue
                for successor, action, cost in problem.get_successors(current_node.state):
                    # if the successor is not explored yet, append this new successor to the explored dictionary
                    tmp = current_node
                    flag = True
                    while tmp.parent != None:
                        if successor == tmp.parent.state:
                            flag = False
                            break
                        tmp = tmp.parent
                    if flag:
                        sn = SearchNode(successor, action, cost, current_node, current_node.depth + 1)
                        frontier.push(sn)
        print("depth limit = " + str(depth_limit))
        depth_limit += 1


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
        return None
