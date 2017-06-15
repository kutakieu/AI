""" File name:   dfa.py
    Author:      Taku Ueki
    Date:        23/02/17
    Description: This file defines a function which reads in
                 a DFA described in a file and builds an appropriate datastructure.

                 There is also another function which takes this DFA and a word
                 and returns if the word is accepted by the DFA.

                 It should be implemented for Exercise 3 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""

def load_dfa(dfa_file_name):
    """ This function reads the DFA in the specified file and returns a
        data structure representing it. It is up to you to choose an appropriate
        data structure. The returned DFA will be used by your accepts_word
        function. Consider using a tuple to hold the parts of your DFA, one of which
        might be a dictionary containing the edges.

        We suggest that you return a tuple containing the names of the start
        and accepting states, and a dictionary which represents the edges in
        the DFA.

        (str) -> Object
    """
    fin = open(dfa_file_name, "r")
    lines = fin.readlines()
    initial = []
    accepting = []
    transition = {}
    for line in lines:
        line = line[:-1]
        if "initial" in line:
            line = line.split(" ")
            for attribute in line[1:]:
                initial.append(int(attribute[5:]))

        if "accepting" in line:
            line = line.split(" ")
            for attribute in line[1:]:
                accepting.append(int(attribute[5:]))

        if "transition" in line:
            line = line.split(" ")
            start = int(line[1][5:])
            end = int(line[2][5:])
            character = line[3]
            transition[start, character] = end
    dfa = [initial, accepting, transition]
    return dfa



def accepts_word(dfa, word):
    """ This function takes in a DFA (that is produced by your load_dfa function)
        and then returns True if the DFA accepts the given word, and False
        otherwise.

        (Object, str) -> bool
    """

    initial = dfa[0]
    accepting = dfa[1]
    transition = dfa[2]

    state = initial[0]
    n = 1

    for character in word:

        try:
            state = transition[state,character]
        except:
            print("unacceptable word")
            return False

        if n == len(word):
            if state in accepting:
                return True
            else:
                return False
        n += 1

    print("here")
    return False

def main():

    dfa = load_dfa("/Users/tAku/Desktop/AI/COMP3620-6230-2017-Assignment-0-Python-Agent/exercise3_dfa/test3.dfa")

    while True:
        word = input("new input = ")
        if word == "exit":
            return
        print(accepts_word(dfa, word))

if __name__ == "__main__":
   main()
