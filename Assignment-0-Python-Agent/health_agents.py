""" File name:   health_agents.py
    Author:      Taku Ueki
    Date:        24/02/17
    Description: This file contains agents which fight disease. It is used
                 in Exercise 4 of Assignment 0.
"""

import random
from collections import deque
import copy

class HealthAgent(object):
    """ A simple disease fighting agent. """

    def __init__(self, locations, conn):
        """ This contructor does nothing except save the locations and conn.
            Feel free to overwrite it when you extend this class if you want
            to do some initial computation.

            (HealthAgent, [str], { str : set([str]) }) -> None
        """
        self.locations = locations
        self.conn = conn

    def choose_move(self, location, valid_moves, disease, threshold, growth, spread):
        """ Using given information, return a valid move from valid_moves.
            Returning an inalid move will cause the system to stop.

            Changing any of the mutable parameters will have no effect on the operation
            of the system.

            This agent will locally move to the highest disease, of there is
            is no nearby disease, it will act randomly.

            (HealthAgent, str, [str], [str], { str : float }, float, float, float) -> str
        """

        max_disease = None
        max_move = None
        for move in valid_moves:
           if max_disease is None or disease[move] > max_disease:
               max_disease = disease[move]
               max_move = move

        if not max_disease:
            return random.choice(valid_moves)

        return max_move

#Make a new agent here called SmartHealthAgent, which extends HealthAgent and acts a bit more sensibly

class SmartHealthAgent(HealthAgent):
    def __init__(self, locations, conn):
        self.locations = locations
        self.conn = conn
        self.history = []


    def valid_moves(self, location):
        return self.conn[location]

    def move(self, loc, location):
        if loc in self.conn[location]:
            disease[location] = 0
        else:
            raise ValueError

    def spread_disease(self, location, disease, growth, threshold, spread):
        _disease = copy.deepcopy(disease)
        _disease[location] = 0
        for loc in self.locations:
            dis = _disease[loc] * (1 + growth)
            _disease[loc] = dis
        _disease[location] = 0
        for loc in self.locations:
            dis = 0
            for conn in self.conn[loc]:
                if _disease[conn] >= threshold:
                    dis += _disease[conn] * spread
            _disease[loc] += dis
        _disease[location] = 0
        return _disease

    def get_paths(self, loc):
        paths = []
        for vm1 in self.valid_moves(loc):
            for vm2 in self.valid_moves(vm1):
                for vm3 in self.valid_moves(vm2):
                    for vm4 in self.valid_moves(vm3):
                        # for vm5 in self.valid_moves(vm4):
                        #     for vm6 in self.valid_moves(vm5):
                        paths.append([loc, vm1, vm2, vm3, vm4])
        return paths

    def choose_move(self, location, valid_moves, disease, threshold, growth, spread):

        paths = self.get_paths(location)
        best_path_index = 0
        total_disease = 10000000
        temp_total_disease = 1000000
        candidates = []

        for i in range(len(paths)):
            disease_simulation = copy.deepcopy(disease)
            current_path = []
            for loc in paths[i]:
                temp_total_disease = 0
                current_path.append(loc)
                disease_simulation = self.spread_disease(loc, disease_simulation, growth, threshold, spread)
                for l in self.locations:
                    temp_total_disease += disease_simulation[l]
                if temp_total_disease == 0:
                    candidates.append(current_path)
                    break
            if len(current_path) < len(paths[i]):
                continue
            temp_total_disease = 0
            for l in self.locations:
                temp_total_disease += disease_simulation[l]
            if temp_total_disease < total_disease:
                total_disease = temp_total_disease
                best_path_index = i

        num_shortest_path = 100
        if len(candidates) != 0:
            for candidate in candidates:
                if len(candidate) < num_shortest_path:
                    num_shortest_path = len(candidate)
                    shortest_path = candidate
            return shortest_path[1]



        return paths[best_path_index][1]
