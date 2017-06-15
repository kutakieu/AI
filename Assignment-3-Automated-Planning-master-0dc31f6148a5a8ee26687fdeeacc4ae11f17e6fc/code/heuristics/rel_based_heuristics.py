
"""
COMP3620-6320 Artificial Intelligence 2017 - Planning Assignment Q4

Enter your details below:

Name:Taku Ueki
Student Code:u5934839
email:u5934839@anu.edu.au

This module contains relaxation heuristics hadm, hFF. You need to implement
  1) the function calc_goal_h for the hff heuristic.
  2) the __call__(self,node) for the hadm heuristic
calc_goal_h is called within the __call(self,node)__ by the generic call method _RelaxationHeuristic at any step during your search.
for the hff we have done part of the implementation for a reasonably fast reachability analysis. You need to make use of this analysis to extract your hff estimate
Regarding the hadm heuristic, you can either use the relaxation methods or whatever you come up with for devising your admissible estiamte.
"""

from planning_task import Action, Task
from heuristics.heuristic_base import Heuristic
import heapq
import logging
class RelaxedFact:
    """This class represents a relaxed fact."""
    def __init__(self, name):
        """Construct a new relaxed fact.

        Keyword arguments:
        name -- the name of the relaxed fact.

        Member variables:
        name -- the name of the relaxed fact.
        precondition_of -- a list that contains all actions, this fact is a
                           precondition of.
        expanded -- stores whether this fact has been expanded during the
                    reachability forward pass.
        level -- stores the level value of this Fact (the one you get during relaxed reachability). This way we have a much more efficient implementation
        cheapest_achiever -- stores the cheapest action that was applied to reach this fact. Also this information can be obtained
                             during the relaxed reachability
        """
        self.name = name
        self.precondition_of = []
        self.expanded = False
        self.cheapest_achiever = None
        self.level = float('inf')


class RelaxedAction:
    """ This class represents a relaxed action (no delete effects)."""
    def __init__(self, name, preconditions, add_effects):
        """Construct a new relaxed action.

        Keyword arguments:
        name -- the name of the relaxed action.
        preconditions -- the preconditions of this action
        add_effects -- the add effects of this action

        Member variables:
        name -- the name of the relaxed action.
        preconditions -- the preconditions of this action
        counter -- alternative method to check whether all preconditions are
                   True
        add_effects -- the add effects of this action
        cost -- the cost for applying this action
        """
        self.name = name
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.cost = 1
        self.counter = len(preconditions)


class _RelaxationHeuristic(Heuristic):
    """This class is the base class for all relaxation heuristics.
       You need to look into this code to understand how to compute
       the hff heurstic
    """
    def __init__(self, task):
        """Construct a instance of _RelaxationHeuristic.

        Keyword arguments:
        task -- an instance of the Task class.

        Member variables:
        facts -- a dict that maps from fact names to fact objects
        actions -- a list of actions
        init -- the set of facts that define the initial state
        goals -- the set of facts that define the goal state
        tie_breaker -- a tie breaker needed for qeueing
        eval -- a function that is used to evaluate the cost of applying an
                action
        """
        self.facts = dict()
        self.actions = []
        self.goals = task.goals
        self.init = task.initial_state
        self.tie_breaker = 0
        self.start_state = RelaxedFact("start")

        # Create relaxed facts for all facts in the task description.
        for fact in task.facts:
            self.facts[fact] = RelaxedFact(fact)

        for op in task.actions:
            # Relax actions and add them to action list.
            ro = RelaxedAction(op.name, op.preconditions, op.add_effects)
            self.actions.append(ro)

            # Initialize precondition_of-list for each fact
            for var in op.preconditions:
                self.facts[var].precondition_of.append(ro)

            # Handle actions that have no preconditions.
            if not op.preconditions:
                # We add this action to the precondtion_of list of the start
                # state. This way it can be applied to the start state. This
                # helps also when the initial state is empty.
                self.start_state.precondition_of.append(ro)

    def __call__(self, node):
        """This function is called whenever the heuristic needs to be computed.

        Keyword arguments:
        node -- the current state
        """
        state = node.state
        state = set(state)

        # Reset level and set to default values.
        self.init_level(state)

        # Construct the priority queue.
        heap = []
        # Add a dedicated start state, to cope with actions without
        # preconditions and empty initial state.
        heapq.heappush(heap, (0, self.tie_breaker, self.start_state))
        self.tie_breaker += 1

        for fact in state:
            # Its order is determined by the level the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(heap, (self.facts[fact].level, self.tie_breaker,
                                  self.facts[fact]))
            self.tie_breaker += 1

        # Call the reachability search that performs the forward pass.
        self.reachability(heap)

        # Extract the goal heuristic.
        h_value = self.calc_goal_h()

        return h_value

    def init_level(self, state):
        """
        This function resets all member variables that store information that
        needs to be recomputed for each call of the heuristic.
        """
        def reset_fact(fact):
            fact.expanded = False
            fact.cheapest_achiever = None
            if fact.name in state:
                fact.level = 0
                fact.sa_set = set()
            else:
                fact.sa_set = None
                fact.level = float('inf')
        # Reset start state
        reset_fact(self.start_state)

        # Reset facts.
        for fact in self.facts.values():
            reset_fact(fact)

        # Reset actions.
        for action in self.actions:
            action.counter = len(action.preconditions)

    def get_cost(self, action, pre):
        """This function calculated the cost of applying an action, and is an utility
           function for the reachability algorithm.
        """

        if action.preconditions:
            # If this action has preconditions, we sum over the
            # heuristic values of all preconditions.
            cost = sum([self.facts[pre].level
                              for pre in action.preconditions])
        else:
            # If there are no preconditions for this action, its cost is 0.
            cost = 0

        # this function return the cost of getting to that precondition
        return cost + action.cost



    def finished(self, achieved_goals, queue):
        """
        This function is used as a stopping criterion for the reachability search
        """
        return achieved_goals == self.goals or not queue

    def reachability(self, queue):
        """This function is an implementation of a reachability search.

        For efficiency reasons, it is used instead of an explicit level by level construction.
        Note that this is basically the relaxed reachability algorithm presented during the lecture, with the
        difference that here levels are organised in a queue so that always the smaller level is expanded first. Every time
        a new fact is achieved by some action in some previous level, this fact may activate new actions. So on and so forth
        till the goal is reached.
        """
        # Stores the achieved goals and facts.
        achieved_goals = set()
        while not self.finished(achieved_goals, queue):
            # Get the fact with the lowest level value.
            (dist, tie, fact) = heapq.heappop(queue)
            # If this node is part of the goal, we add to the goal set, which is used
            # in the finished testing
            if fact.name in self.goals:
                achieved_goals.add(fact.name)
            # Check whether we already expanded this fact.
            if not fact.expanded:
                # Iterate over all actions this fact is a precondition of.
                for action in fact.precondition_of:
                    # Decrease the precondition counter. This is an efficient way to establish whether that action
                    # is reached in the computation
                    action.counter -= 1
                    # Check whether all preconditions are True and we can apply
                    # this action.
                    if action.counter <= 0:
                        for n in action.add_effects:
                            rel_fact = self.facts[n]
                            # Calculate the cost of applying this action. This will determine the best achiever
                            tmp_dist = self.get_cost(action,fact)
                            if tmp_dist < rel_fact.level:
                                # If the new costs are cheaper, then the old
                                # costs, we change the rel_fact level value
                                rel_fact.level = tmp_dist
                                rel_fact.cheapest_achiever = action
                                # And push it on the queue.
                                heapq.heappush(queue, (tmp_dist,
                                                       self.tie_breaker,
                                                       rel_fact))
                                self.tie_breaker += 1
                # Finally the fact is marked as expanded.
                fact.expanded = True

class hff(_RelaxationHeuristic):
    """ This class is an implementation of the hFF heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def __init__(self, task):
        """Construct a hFFHeuristic.
        """
        super().__init__(task)


    def calc_goal_h(self):
        """
        This is the function that needs to be implemented.
        IMPORTANT: Albeit the function can be rebuilt from scratch, we suggest to make use of the
        data-structure computed in the _RelaxationHeuristic. In particular we suggest you to use
        the facts data structure. This structure is a dictionary mapping facts of your planning
        problem to Relaxed Facts. Each Relaxed Fact contains information regarding the cheapest
        achiever (relaxed action) used to achieve that condition. This should be enough for you to
        extract plan. Also, remember that if *at least* one goal in the problem is at level = inf
        then the problem is not solvable.

        The procedure needs to return a float value.
        """

        # determine M which is minimum time step to satisfy all goal propositions
        M = -100
        for goal in self.goals:
            firstlevel = self.firstlevel(goal)
            if M < firstlevel:
                M = firstlevel
        # create a dictionary which map time to goals that are satisfied at this time step
        G = {}
        for t in range(0,M+1):
            G[t] = set()
            for goal in self.goals:
                # determine when each goal gets satisfied
                if self.firstlevel(goal) == t:
                    # print(goal)
                    G[t].add(self.facts[goal])

        relaxed_plan = set()    # a set to store relaxed plan
        for t in range(M, 0 , -1):
            for goal_t in G[t]:
                # for goals at time step t, put actions to the relaxed_plan which lead to the goal
                relaxed_plan.add(goal_t.cheapest_achiever)

                # put each goal's preconditions as new goals to be satisfied to certain time step of G
                for precondition in goal_t.cheapest_achiever.preconditions:
                    G[self.firstlevel(precondition)].add(self.facts[precondition])

        # print(len(relaxed_plan))
        # print(relaxed_plan)
        return len(relaxed_plan)


    def firstlevel(self, goal):
        return self.facts[goal].level

    # def firstlevel4action(self, action, facts):
    #     # level = 10000
    #     for fact in facts.keys():
    #         if action == facts[fact].cheapest_achiever:
    #             return facts[fact].level

class hadm(_RelaxationHeuristic):
    """ This class is an implementation of your admissible heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def __init__(self, task):
        """Construct the heuristic
        """
        super().__init__(task)

    def __call__(self, node):

        state = node.state
        state = set(state)

        # Reset level and set to default values.
        self.init_level(state)

        # Construct the priority queue.
        heap = []
        # Add a dedicated start state, to cope with actions without
        # preconditions and empty initial state.
        heapq.heappush(heap, (0, self.tie_breaker, self.start_state))
        self.tie_breaker += 1

        for fact in state:
            # Its order is determined by the level the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(heap, (self.facts[fact].level, self.tie_breaker,
                                  self.facts[fact]))
            self.tie_breaker += 1

        # Call the reachability search that performs the forward pass.
        self.reachability(heap)

        # Extract the goal heuristic.
        # H = self.calc_goal_h(self.goals)
        H = self.H(self.goals, state)
        # print(H)

        # print(max(H.values()))
        return max(H.values())

        # return sum(H.values())
        # return sum(H.values())*1/2
        # return sum(H.values()) - max(H.values())


    def H_max(self, goals, state):
        from copy import deepcopy

        H = {}
        # for each goal find the cost to achive it.
        for goal in goals:
            # reset the state to the original state
            _state = deepcopy(state)
            # initialize the cost to 0 for each goal
            H[goal] = 0
            queue = []  # queue to store preconditions for each action to achive this goal
            queue.append(goal)
            while len(queue) != 0:
                current_proposition = queue.pop()
                # if the current proposition is not satisfied yet, put this proposition to the queue to find an action to satisfy it.
                if current_proposition not in _state:
                    _state.add(current_proposition)
                # find an action to achieve this proposition
                action = self.facts[current_proposition].cheapest_achiever
                if action == None:
                    continue
                H[goal] += 1
                # if a precondition of this action is not satisfied yet put this precondition to the queue
                for pre in action.preconditions:
                    if pre not in _state:
                        queue.append(pre)
        # return H
        return max(H.values())
