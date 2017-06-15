""" File name:   disease_scenario.py
    Author:      Taku Ueki
    Date:        24/02/17
    Description: This file represents a scenario simulating the spread of an
                 infectious disease around Australia. It should be
                 implemented for Part 1 of Exercise 4 of Assignment 0.

                 See the lab notes for a description of its contents.
"""
import copy
class DiseaseScenario():

    def read_scenario_file(self, scenario_file_name):
        try:
            fin = open(scenario_file_name, "r")
            # fin = open(scenario_file_name, "r")
            lines = fin.readlines()

            self.locations = []
            self.disease = {}
            self.conn = {}
            for line in lines:
                line = line[:-1]
                attributes = line.split(" ")

                if attributes[0] == "threshold":
                    self.threshold = float(attributes[1])

                elif attributes[0] == "growth":
                    self.growth = float(attributes[1])

                elif attributes[0] == "spread":
                    self.spread = float(attributes[1])

                elif attributes[0] == "location":
                    self.locations.append(attributes[1])
                    self.conn[attributes[1]] = set()
                    self.disease[attributes[1]] = 0.0

                elif attributes[0] == "start":
                    self.location = attributes[1]

                elif attributes[0] == "disease":
                    self.disease[attributes[1]] = float(attributes[2])

                elif attributes[0] == "conn":
                    self.conn[attributes[1]].add(attributes[2])
                    self.conn[attributes[2]].add(attributes[1])
                    
            return True

        except:
            return False

    def valid_moves(self):
        temp = list(self.conn[self.location])
        temp.append(self.location)
        return temp

    def move(self, loc):
        if loc in self.conn[self.location]:
            self.location = loc
            self.disease[self.location] = 0
        else:
            raise ValueError

    def spread_disease(self):
        _disease = copy.deepcopy(self.disease)
        for loc in self.locations:
            self.disease[loc] += self.disease[loc] * self.growth
        self.disease[self.location] = 0
        for loc in self.locations:
            dis = 0
            for conn in self.conn[loc]:
                if _disease[conn] >= self.threshold:
                    dis += _disease[conn] * self.spread
            self.disease[loc] += dis
        self.disease[self.location] = 0
