# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name:Taku Ueki
    Student Code:u5934839
    email:u5934839@anu.edu.au
"""
from actions import Directions
from agents import Agent
import util

from search_problems import AdversarialSearchProblem

class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
            (MinimaxAgent, str) -> None
        """
        self.max_player = max_player
        self.depth = int(depth)

    def evaluation(self, problem, state):

        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """

        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        # return score

        if problem.terminal_test(state):
                return score

        dis_RandY = 1000000
        dis_BandY = 1000000
        for yellow_pos in yellow_birds:
            tmp_RY = problem.maze_distance(red_pos, yellow_pos)
            if dis_RandY > tmp_RY:
                dis_RandY = tmp_RY
            tmp_BY = problem.maze_distance(black_pos, yellow_pos)
            if dis_BandY > tmp_BY:
                dis_BandY = tmp_BY
        dis_RandB = problem.maze_distance(black_pos, red_pos)

        """if the distance between red bird and black bird is 1, make the red bird think about its potential points not current score that can be achieved easily and seems good for the moment(make red bird not eat black bird because it may get more points in the future)"""
        evaluation_score = 0
        if dis_RandB <= 1:
            yb4red = []
            yb4black = []
            # estimate the number of yellow birds red_bird can eat and black_bird can eat, by counting the number of close yellow birds to each red and black bird
            for yellow_pos in yellow_birds:
                tmp_RY = problem.maze_distance(red_pos, yellow_pos)
                tmp_BY = problem.maze_distance(black_pos, yellow_pos)
                if tmp_RY > tmp_BY:
                    evaluation_score -= 100
                    yb4red.append(yellow_pos)
                elif tmp_RY < tmp_BY:
                    evaluation_score += 100
                    yb4black.append(yellow_pos)
            return (self.Minimum_Spanning_Tree(black_pos, yb4black, problem) - self.Minimum_Spanning_Tree(red_pos, yb4red, problem))*10 + evaluation_score*5 + score
        """as the red bird gets closer to a yellow bird the evaluation increases
        as the black bird gets closer to a yellow bird the evaluation goes down
        as red bird and black bird get closer each other the evaluation increases
        repeated tuning with different parameters and coefficients and finally got not bad results with these parameters"""
        return dis_BandY - dis_RandY + score*1.5 - dis_RandB/2

    def Minimum_Spanning_Tree(self, position, yellow_birds, problem):
        """calculate Minimum Spanning Tree to estimate potential points"""
        # player, red_pos, black_pos, yellow_birds, score, yb_score = state
        heuristic_value = 0
        if len(yellow_birds) == 0:
            return heuristic_value
        nearest_yb_distance = 10000
        nearest_yb = None
        for yb in yellow_birds:
            distance = problem.maze_distance(yb, position)

            if distance < nearest_yb_distance:
                nearest_yb = yb
                nearest_yb_distance = distance
        heuristic_value += nearest_yb_distance

        #prepare a dictionary {yellow_bird : [distances_between_other_yellow_birds, yellow_bird_position]}
        dis_YandYs = {}
        for yb1 in yellow_birds:
            dis_YandY = []
            for yb2 in yellow_birds:
                if yb1 != yb2:
                    distance = problem.maze_distance(yb1, yb2)
                    dis_YandY.append([distance, yb2])
            dis_YandY.sort()
            dis_YandYs[yb1] = dis_YandY

        # choose yellow_birds until the tree covers the all unvisited yellow_birds
        YB_set = set()
        YB_set.add(nearest_yb)
        while len(YB_set) < len(yellow_birds):
            nearest_yb_distance = 10000
            nearest_yb = None
            from_yb = None
            for yb in YB_set:
                dis_YandY = dis_YandYs[yb]
                temp_yb_distance, temp_yb = dis_YandY[0]
                if temp_yb_distance < nearest_yb_distance:
                    nearest_yb_distance = temp_yb_distance
                    nearest_yb = temp_yb
                    from_yb = yb
            if nearest_yb not in YB_set:
                YB_set.add(nearest_yb)
                heuristic_value += nearest_yb_distance

            dis_YandY = dis_YandYs[nearest_yb]
            dis_YandY.remove([nearest_yb_distance, from_yb])
            dis_YandY = dis_YandYs[from_yb]
            dis_YandY.remove([nearest_yb_distance, nearest_yb])

        return heuristic_value




    # def maximize(self, problem, state, current_depth, alpha, beta):
    def maximize(self, problem, state, current_depth):
        """
            This method should return a pair (max_utility, max_action).

             (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> (number, str)
        """

        "*** YOUR CODE GOES HERE ***"
        if current_depth == self.depth:
            return self.evaluation(problem, state), Directions.STOP

        else:
            temp = []
            for successor, action, cost in problem.get_successors(state):
                temp.append([self.minimize(problem, successor, current_depth+1),action])
            return max(temp)

        # alpha beta pruning still not working properly
        # if current_depth == self.depth:
        #     return self.evaluation(problem, state), Directions.STOP
        # else:
        #     v = -10000000000
        #     temp = []
        #     for successor, action, cost in problem.get_successors(state):
        #         temp.append([self.minimize(problem, successor, current_depth+1, alpha, beta),action])
        #     v = [max(v, max(temp)[0]), max(temp)[1]]
        #     if v[0] >= beta:
        #         return v
        #     alpha = max(alpha, v[0])
        #     return v

        # You can remove this line once you finished your implementation
        # util.raise_not_defined()


    # def minimize(self, problem, state, current_depth, alpha, beta):
    def minimize(self, problem, state, current_depth):
        """
            This function should just return the minimum utility.

            (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> number
        """

        "*** YOUR CODE GOES HERE ***"
        if current_depth == self.depth:
            return self.evaluation(problem, state)

        else:
            temp = []
            for successor, action, cost in problem.get_successors(state):
                temp.append(self.maximize(problem, successor, current_depth+1))
            return min(temp)

        # alpha beta pruning
        # if current_depth == self.depth:
        #     return self.evaluation(problem, state)
        # else:
        #     v = 10000000000
        #     temp = []
        #     for successor, action, cost in problem.get_successors(state):
        #         temp.append(self.maximize(problem, successor, current_depth+1, alpha, beta))
        #
        #     min_temp = min(temp)[0]
        #     v = min(v, min_temp)
        #     if v <= alpha:
        #         return v
        #     beta = min(beta, v)
        #     return v


        #You can remove this line once you finished your implementation
        # util.raise_not_defined()


    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        #We tell the search problem what the current state is and which player
        #is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        # utility, max_action = self.maximize(problem, state, 0, -10000000000,10000000000)
        print("At Root: Utility:", utility, "Action:", max_action, "Expanded:", problem._expanded)
        return max_action
