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

    stack = Stack()
    depth_limit = 0
    s0 = problem.get_initial_state()
    sn_root = SearchNode(s0)


    # depth += 1
    check = None
    while True:
        explored = []
        explored.append(s0)
        stack = Stack()

        stack.push(sn_root)
        while not stack.is_empty():
            # print("here")
            # check_limit = stack.peek()
            frontier = stack.pop()
            # if depth_limit != 0:
            #     print(str(frontier.action) + " "+ str(frontier.depth))
            check = check_goal(frontier, problem)

            if check != None:
                return check
            else:
                if(frontier.depth == depth_limit):
                    continue
                for successor, action, cost in problem.get_successors(frontier.state):
                    # if successor != frontier.state:
                    if successor not in explored:
                        explored.append(successor)
                        sn = SearchNode(successor, action, cost, frontier, frontier.depth + 1)

                        # if stack.find(sn)
                        stack.push(sn)

        depth_limit += 1
        print(depth_limit)
        print(" ")


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
