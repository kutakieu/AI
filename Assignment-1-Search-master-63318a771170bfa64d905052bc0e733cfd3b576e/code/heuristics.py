# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

#-------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
#-------------------------------------------------------------------------------

def null_heuristic(pos, problem):
    """ The null heuristic. It is fast but uninformative. It always returns 0.
        (State, SearchProblem) -> int
    """
    return 0

def manhattan_heuristic(pos, problem):
  """ The Manhattan distance heuristic for a PositionSearchProblem.
      ((int, int), PositionSearchProblem) -> int
  """
  # print("mahattan")
  return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])

def euclidean_heuristic(pos, problem):
    """ The Euclidean distance heuristic for a PositionSearchProblem
        ((int, int), PositionSearchProblem) -> float
    """
    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5

#Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

#-------------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
#-------------------------------------------------------------------------------

#You can make helper functions here, if you need them

def bird_counting_heuristic(state, problem) :
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """
    heuristic_value = len(yellow_birds)
    # print(heuristic_value)
    return heuristic_value

bch = bird_counting_heuristic

def MHdis(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
def ECdis(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def every_bird_heuristic(state, problem):
    """
        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> number
    """
    position, yellow_birds = state
    yellow_birds = list(yellow_birds)
    heuristic_value = 0
    if len(yellow_birds) == 0:
        return heuristic_value

    """ *** YOUR CODE HERE *** """
    #find nearest yellow bird and add the distance to the heuristic value

    nearest_yb_distance = 10000
    nearest_yb = None
    for yb in yellow_birds:
        distance = problem.maze_distance(yb, position)

        if distance < nearest_yb_distance:
            nearest_yb = yb
            nearest_yb_distance = distance
    heuristic_value += nearest_yb_distance

    """calculate Minimum Spanning Tree as a heuristic function"""
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

    """repeat finding nearest yellow bird from YB_set which is a set of yellow bird already achieved a path to go, until you get minimun edeges to go to all yellow birds"""
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

        # print("yb = " + str(from_yb) + "TO" + str(nearest_yb) + "  dis = " + str(nearest_yb_distance))
        dis_YandY = dis_YandYs[nearest_yb]
        dis_YandY.remove([nearest_yb_distance, from_yb])
        dis_YandY = dis_YandYs[from_yb]
        dis_YandY.remove([nearest_yb_distance, nearest_yb])

    return heuristic_value

every_bird = every_bird_heuristic
