H_ff heuristic tries to estimate the cost to satisfy all the goals by finding actions to achieve each goal proposition and store those actions’ preconditions as new goals to be satisfied and keep finding actions until all goals are satisfied.
As h_ff heuristic is not admissible, it is not guaranteed to obtain optimal solution for problems. Therefore, it returns longer plans than optimal one. However, as this heuristic is more informative, it expands much less nodes and finds an arbitrary solution much quicker as this table illustrates. H_ff can find an arbitrary solution for problems that cannot be solved without heuristic within certain time. Therefore, if you need to find a solution quickly in practical cases just like elevator's tasks, it would be better to use inadmissible heuristic to make the system move as soon as new task is given.

I ran the program with/without heuristic. If it does not terminate within 5 minutes, it stops and return nothing. So, "-" shows that it could not be solved within 5 minutes.

tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal | runtime: hff | nodes expanded: hff | plan length: hff
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0036 | 80 | 6 | 0.023 | 18 | 10
blocks/task02.pddl | 0.0031 | 67 | 10 | 0.014 | 12 | 10
blocks/task03.pddl | 0.003 | 63 | 6 | 0.0091 | 7 | 6
blocks/task04.pddl | 0.03 | 515 | 12 | 0.03 | 16 | 12
blocks/task05.pddl | 0.03 | 550 | 10 | 0.1 | 52 | 14
blocks/task06.pddl | 0.041 | 757 | 16 | 0.13 | 61 | 32
blocks/task07.pddl | 0.16 | 2020 | 12 | 0.075 | 29 | 12
blocks/task08.pddl | 0.31 | 4645 | 10 | 0.032 | 11 | 10
blocks/task09.pddl | 0.43 | 6598 | 20 | 0.12 | 46 | 30
blocks/task10.pddl | 2.7 | 35659 | 20 | 0.48 | 136 | 50
blocks/task11.pddl | 4.5 | 64085 | 22 | 0.22 | 62 | 26
blocks/task12.pddl | 4.1 | 58151 | 20 | 0.64 | 187 | 40
blocks/task13.pddl | 4.3e+01 | 496332 | 18 | 1.7 | 385 | 46
blocks/task14.pddl | 5.2e+01 | 614926 | 20 | 0.69 | 159 | 28
blocks/task15.pddl | 3.6e+01 | 401085 | 16 | 0.57 | 123 | 34

|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal | |runtime: hff | nodes expanded: hff | plan length: hff|
|-----|------|-------|-------|-------|-------|-------|
|elevators/task01.pddl | 3.8e+01 | 82553 | 14 | 0.5 | 19 | 14|
|elevators/task02.pddl | 8.9e+01 | 140343 | 9 | 0.33 | 10 | 9|
|elevators/task03.pddl | - | - | - | 0.88 | 27 | 18|
|elevators/task04.pddl | - | - | - | 1.4 | 23 | 18|
|levators/task05.pddl | - | - | - | 1.5 | 34 | 21|
|elevators/task06.pddl | - | - | - | 3.6 | 45 | 26|
|elevators/task07.pddl | - | - | - | 3.6 | 66 | 29|
|elevators/task08.pddl | - | - | - | 2.2 | 29 | 20|
|elevators/task09.pddl | - | - | - | 2.9 | 42 | 31|
|elevators/task10.pddl | - | - | - | 5.8 | 55 | 32|
|elevators/task11.pddl | - | - | - | 1.1 | 24 | 21|
|elevators/task12.pddl | - | - | - | 4.8 | 67 | 16|
|elevators/task13.pddl | - | - | - | 0.9 | 17 | 15|
|elevators/task14.pddl | - | - | - | 1.5e+01 | 135 | 25|
|elevators/task15.pddl | - | - | - | 5.1 | 47 | 26|
