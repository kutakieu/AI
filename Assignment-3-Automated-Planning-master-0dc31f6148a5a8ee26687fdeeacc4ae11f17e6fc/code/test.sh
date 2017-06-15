#!/bin/bash

FIRST=blocks
SECOND=elevators
TASK_NO=15

declare -a RUNTIME
declare -a NODE
declare -a LENGTH
declare -a RUNTIME_HFF
declare -a NODE_HFF
declare -a LENGTH_HFF

function initVar()
{
  for i in `seq $TASK_NO`
  do
    RUNTIME[$i]='-'
    RUNTIME_HFF[$i]='-'
    NODE[$i]='-'
    NODE_HFF[$i]='-'
    LENGTH[$i]='-'
    LENGTH_HFF[$i]='-'
  done
}

echo 'tasks | runtime(hgoal) | nodes expanded(hgoal) | plan length(hgoal) | runtime(hff) | nodes expanded(hff) | plan length(hff)' > hadm_evaluation_extra.md
echo '-----|------|-------|-------|-------|-------|-------' >> hadm_evaluation_extra.md

for j in $FIRST
do
  echo "using $j..."
  initVar
  for h in hadm hgoal
  do
    for i in `seq $TASK_NO`
    do
      echo "start processing $j/task$(printf "%02d" $i).pddl..."
      while read line; do
        # this part DEPENDS on your output, my output for number of nodes is
        # 2017-05-20 21:49:27,634 INFO     Number of nodes expanded: 41
        if echo $line | grep -q 'Number of nodes'; then
          if [ "$h" == "hgoal" ]; then
            NODE[$i]=`echo $line | cut -d' ' -f7` # needed change
          else
            NODE_HFF[$i]=`echo $line | cut -d' ' -f7`
          fi
        fi
        if echo $line | grep -q 'Wall-clock search time'; then
          if [ "$h" == "hgoal" ]; then
            RUNTIME[$i]=`echo $line | cut -d' ' -f7`
          else
            RUNTIME_HFF[$i]=`echo $line | cut -d' ' -f7`
          fi
        fi
        if echo $line | grep -q 'Plan length'; then
          if [ "$h" == "hgoal" ]; then
            LENGTH[$i]=`echo $line | cut -d' ' -f6`
          else
            LENGTH_HFF[$i]=`echo $line | cut -d' ' -f6`
          fi
        fi
        # you need the gtimeout command which is available by installing coreutil
        # you might also need to change the file task file here
      done < <(python3 pddl_planner.py ../benchmarks/$j/task$(printf "%02d" $i).pddl -H $h -s astar)
    done
  done
  for i in `seq $TASK_NO`
  do
    echo "$j/task$(printf "%02d" $i).pddl | ${RUNTIME[$i]} | ${NODE[$i]} | ${LENGTH[$i]} | ${RUNTIME_HFF[$i]} | ${NODE_HFF[$i]} | ${LENGTH_HFF[$i]}" >> hadm_evaluation_extra.md
  done
done

cat hadm_evaluation_extra.md
