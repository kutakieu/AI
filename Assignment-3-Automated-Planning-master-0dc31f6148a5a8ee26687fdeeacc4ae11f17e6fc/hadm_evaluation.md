I implemented h_max heuristic for this question. For each goal proposition, determine how many actions need to be operated to achieve it and return the highest one among those numbers as a heuristic value.
As the table shows, it takes more time than running this program without heuristic. This is because this heuristic value is not very informative, it needs to expand more nodes than admissible heuristic such as h_ff or h_sum. Therefore, I tried other heuristic values such as (h_sum - h_max) or (h_sum * x : x is a certain scalar value), but they are not guaranteed to return admissible heuristic value. So I adopted h_max heuristic.
H_max heuristic expands less nodes than without heuristic, However, even though h_max expands less nodes, it takes more time than without heuristic. This implies that although h_max's time complexity is polynomial, it is not informative enough to make planning searches faster in these cases.

I ran the program with/without heuristic. If it does not terminate within 5 minutes, it stops and return nothing. So, "-" shows that it could not be solved within 5 minutes.

|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal | |runtime: hadm | nodes expanded: hadm | plan length: hadm|
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

|tasks | runtime: hgoal | nodes expanded: hgoal | plan length: hgoal | |runtime: hadm | nodes expanded: hadm | plan length: hadm|
|-----|------|-------|-------|-------|-------|-------|
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
