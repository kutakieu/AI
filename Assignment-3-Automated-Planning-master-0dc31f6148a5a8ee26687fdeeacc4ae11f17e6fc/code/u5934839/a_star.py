
"""
COMP3620-6320 Artificial Intelligence 2017 - Planning Assignment Q2

Enter your details below:

Name:Taku Ueki
Student Code:u5934839
email:u5934839@anu.edu.au


Implements the A* (a-star) search algorithm for planning.

Method to be implemented is a_star.

We import some basic data-structure that can be useful to tackle the problem.
Have a look at *heapq* that is an efficient implementation of a priority queue using a heap data-structure
Have a look at searchspace that gives you an implementation of a searchnode. In particular look at make_root_node and make_child_node
"""

import heapq
import logging

from search import searchspace
from planning_task import Task
from heuristics import BlindHeuristic



def a_star(task, heuristic=BlindHeuristic):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved
    @param heuristic  A heuristic callable which computes the estimated steps
                      from a search node to reach the goal.
    """
    import time
    start = time.time()
    explored = {}
    queue = []

    # create initial node and push into the queue
    sn_0 = searchspace.make_root_node(task.initial_state)
    heapq.heappush(queue, (heuristic(sn_0) + sn_0.g, 0, sn_0))

    temp = 0    # counter for the queue to break overlab
    num_nodes = 0   # number of pxpanded nodes
    while len(queue) != 0:

        # timer to timeout the program
        # if time.time() - start > 60:
        #     print("time out")
        #     exit()

        # dequeue a top priority node
        current_node = heapq.heappop(queue)[2]
        # count the number of expanded nodes
        num_nodes += 1

        # check if the state is the goal or not
        if task.goal_reached(current_node.state):
            print(current_node.extract_solution())
            logging.info("Number of nodes: " + str(num_nodes))
            return current_node.extract_solution()

        # put this node's state in the explored dictionary with its cost
        explored[current_node.state] = heuristic(current_node) + current_node.g

        for action, state in task.get_successor_states(current_node.state):
            # create new node for the successor
            new_node = searchspace.make_child_node(current_node, action, state)
            # calculate the heuristic value for this new node
            heuristic_new_node = heuristic(new_node) + current_node.g
            # if this state is not visited yet or the cost to get this state is cheper than current cost, register/update the cost to get this state
            if state not in explored or explored[state] > heuristic_new_node:
                    explored[state] = heuristic_new_node
                    temp += 1
                    heapq.heappush(queue, (heuristic_new_node, temp, new_node))
