I implemented h_max heuristic for this question. For each goal proposition, determine how many actions need to be operated to achieve it and return the highest one among those numbers as a heuristic value.
As the table shows, it takes more time than running this program without heuristic. This is because this heuristic value is not very informative, it needs to expand more nodes than admissible heuristic such as h_ff or h_sum. Therefore, I tried other heuristic values such as (h_sum - h_max) or (h_sum * x : x is a certain scalar value), but they are not guaranteed to return admissible heuristic value. So I adopted h_max heuristic.
H_max heuristic expands less nodes than without heuristic, However, even though h_max expands less nodes, it takes more time than without heuristic. This implies that although h_max's time complexity is polynomial, it is not informative enough to make planning searches faster in these cases.

I ran the program with/without heuristic. If it does not terminate within 5 minutes, it stops and return nothing. So, "-" shows that it could not be solved within 5 minutes.

|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0045 | 102 | 6 | 0.041 | 22 | 6
blocks/task02.pddl | 0.0036 | 70 | 10 | 0.041 | 22 | 10
blocks/task03.pddl | 0.0031 | 66 | 6 | 0.031 | 17 | 6
blocks/task04.pddl | 0.033 | 587 | 12 | 0.44 | 163 | 12
blocks/task05.pddl | 0.034 | 575 | 10 | 0.4 | 150 | 10
blocks/task06.pddl | 0.043 | 799 | 16 | 0.91 | 377 | 16
blocks/task07.pddl | 0.16 | 2166 | 12 | 1.2 | 315 | 12
blocks/task08.pddl | 0.35 | 4922 | 10 | 4.5 | 1161 | 10
blocks/task09.pddl | 0.44 | 6688 | 20 | 1.1e+01 | 3251 | 20
blocks/task10.pddl | 3.2 | 38689 | 20 | 4.2e+01 | 8276 | 20
blocks/task11.pddl | 4.9 | 64677 | 22 | 1.8e+02 | 41297 | 22
blocks/task12.pddl | 4.6 | 59168 | 20 | 1.1e+02 | 23404 | 20
blocks/task13.pddl | 5.8e+01 | 531358 | 18 | - | - | -
blocks/task14.pddl | 6.6e+01 | 638232 | 20 | - | - | -
blocks/task15.pddl | 4.6e+01 | 439350 | 16 | - | - | -

|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
elevators/task01.pddl | 4.8e+01 | 105709 | 14 | - | - | -
elevators/task02.pddl | 9e+01 | 142267 | 9 | - | - | -
elevators/task03.pddl | - | - | - | - | - | -
elevators/task04.pddl | - | - | - | - | - | -
elevators/task05.pddl | - | - | - | - | - | -
elevators/task06.pddl | - | - | - | - | - | -
elevators/task07.pddl | - | - | - | - | - | -
elevators/task08.pddl | - | - | - | - | - | -
elevators/task09.pddl | - | - | - | - | - | -
elevators/task10.pddl | - | - | - | - | - | -
elevators/task11.pddl | - | - | - | - | - | -
elevators/task12.pddl | - | - | - | - | - | -
elevators/task13.pddl | - | - | - | - | - | -
elevators/task14.pddl | - | - | - | - | - | -
elevators/task15.pddl | - | - | - | - | - | -



These tables are results for heuristic such that "h_sum * x : x is a certain scalar value" with different x value.
When x = 1/2, it returns optimal length of plans, but it is still not confirmed that this is admissible heuristic. However, empirically it may be heuristic and for some tasks it finds the solution faster than without heuristic. So, it may be able to be used as one of options of admissible heuristic, although it needs to be proved mathematically.
When x = 2/3, 3/5, they find optimal plans for most of tasks in this domain quite quickly, although normal h_sum heuristic returns not optimal solutions for many of tasks. However, they still got not optimal solution for some of tasks (when x = 2/3 task11, when x = 3/5 task7). So they are not admissible.
Hence, although they are not admissible, they find better plans than normal h_sum and find an arbitrary plan quicker than h_max, they may be good options to be used in practical cases.

h_sum * (1/2)  : x = 1/2
|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0068 | 102 | 6 | 0.044 | 25 | 6
blocks/task02.pddl | 0.0034 | 70 | 10 | 0.029 | 18 | 10
blocks/task03.pddl | 0.0046 | 66 | 6 | 0.02 | 12 | 6
blocks/task04.pddl | 0.04 | 587 | 12 | 0.16 | 56 | 12
blocks/task05.pddl | 0.034 | 575 | 10 | 0.19 | 69 | 10
blocks/task06.pddl | 0.043 | 799 | 16 | 0.52 | 194 | 16
blocks/task07.pddl | 0.17 | 2166 | 12 | 0.17 | 45 | 12
blocks/task08.pddl | 0.34 | 4922 | 10 | 0.47 | 115 | 10
blocks/task09.pddl | 0.45 | 6688 | 20 | 3.5 | 947 | 20
blocks/task10.pddl | 3.1 | 38689 | 20 | 1.6 | 319 | 20
blocks/task11.pddl | 4.9 | 64677 | 22 | 3.8e+01 | 7013 | 22
blocks/task12.pddl | 4.6 | 59168 | 20 | 8.4 | 1504 | 20
blocks/task13.pddl | 5.6e+01 | 531358 | 18 | 9.5 | 1218 | 18
blocks/task14.pddl | 6.7e+01 | 638232 | 20 | 7.1e+01 | 9886 | 20
blocks/task15.pddl | 4.6e+01 | 439350 | 16 | 6.0 | 820 | 16

h_sum * (2/3)	:	x = 2/3
|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0043 | 102 | 6 | 0.022 | 13 | 6
blocks/task02.pddl | 0.0032 | 70 | 10 | 0.025 | 15 | 10
blocks/task03.pddl | 0.0039 | 66 | 6 | 0.017 | 10 | 6
blocks/task04.pddl | 0.034 | 587 | 12 | 0.087 | 33 | 12
blocks/task05.pddl | 0.036 | 575 | 10 | 0.069 | 27 | 10
blocks/task06.pddl | 0.048 | 799 | 16 | 0.21 | 71 | 16
blocks/task07.pddl | 0.17 | 2166 | 12 | 0.23 | 56 | 12
blocks/task08.pddl | 0.36 | 4922 | 10 | 0.16 | 37 | 10
blocks/task09.pddl | 0.43 | 6688 | 20 | 1.1 | 289 | 20
blocks/task10.pddl | 3.1 | 38689 | 20 | 0.49 | 101 | 22
blocks/task11.pddl | 5.2 | 64677 | 22 | 5.7 | 1045 | 22
blocks/task12.pddl | 4.9 | 59168 | 20 | 1.3 | 248 | 20
blocks/task13.pddl | 5.6e+01 | 531358 | 18 | 3.3 | 444 | 18
blocks/task14.pddl | 6.7e+01 | 638232 | 20 | 6.5 | 955 | 20
blocks/task15.pddl | 4.6e+01 | 439350 | 16 | 1.6 | 242 | 16

h_sum * (3/5)  : x=3/5
|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0045 | 102 | 6 | 0.025 | 13 | 6
blocks/task02.pddl | 0.0039 | 70 | 10 | 0.026 | 15 | 10
blocks/task03.pddl | 0.0031 | 66 | 6 | 0.021 | 10 | 6
blocks/task04.pddl | 0.034 | 587 | 12 | 0.086 | 34 | 12
blocks/task05.pddl | 0.038 | 575 | 10 | 0.077 | 28 | 10
blocks/task06.pddl | 0.047 | 799 | 16 | 0.32 | 109 | 16
blocks/task07.pddl | 0.17 | 2166 | 12 | 0.36 | 89 | 14
blocks/task08.pddl | 0.34 | 4922 | 10 | 0.17 | 39 | 10
blocks/task09.pddl | 0.44 | 6688 | 20 | 1.4 | 364 | 20
blocks/task10.pddl | 3.1 | 38689 | 20 | 0.47 | 99 | 20
blocks/task11.pddl | 4.9 | 64677 | 22 | 1.5e+01 | 2680 | 22
blocks/task12.pddl | 4.6 | 59168 | 20 | 2.6 | 480 | 20
blocks/task13.pddl | 5.6e+01 | 531358 | 18 | 4.1 | 511 | 18
blocks/task14.pddl | 6.7e+01 | 638232 | 20 | 1.7e+01 | 2486 | 20
blocks/task15.pddl | 4.6e+01 | 439350 | 16 | 1.8 | 257 | 16


h_sum * 1 :  x=1 (normal h_sum)
|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal |runtime: hadm | nodes expanded: hadm | plan length: hadm|
-----|------|-------|-------|-------|-------|-------
blocks/task01.pddl | 0.0044 | 102 | 6 | 0.028 | 15 | 6
blocks/task02.pddl | 0.0034 | 70 | 10 | 0.026 | 15 | 10
blocks/task03.pddl | 0.0039 | 66 | 6 | 0.016 | 10 | 6
blocks/task04.pddl | 0.034 | 587 | 12 | 0.058 | 24 | 12
blocks/task05.pddl | 0.036 | 575 | 10 | 0.06 | 23 | 10
blocks/task06.pddl | 0.046 | 799 | 16 | 0.1 | 36 | 16
blocks/task07.pddl | 0.17 | 2166 | 12 | 0.63 | 152 | 14
blocks/task08.pddl | 0.36 | 4922 | 10 | 0.12 | 29 | 10
blocks/task09.pddl | 0.45 | 6688 | 20 | 0.45 | 121 | 22
blocks/task10.pddl | 3.1 | 38689 | 20 | 0.23 | 48 | 22
blocks/task11.pddl | 5.0 | 64677 | 22 | 0.96 | 175 | 24
blocks/task12.pddl | 4.5 | 59168 | 20 | 0.57 | 98 | 24
blocks/task13.pddl | 5.6e+01 | 531358 | 18 | 2.2 | 311 | 22
blocks/task14.pddl | 6.7e+01 | 638232 | 20 | 2.1 | 310 | 20
blocks/task15.pddl | 4.6e+01 | 439350 | 16 | 0.71 | 107 | 18
