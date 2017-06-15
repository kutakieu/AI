import argparse
import subprocess
import random

# Complete the file with your LNS solution

if __name__ =='__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('problem_filename', help='problem file')
   parser.add_argument('start_solution_filename', help='file describing the solution to improve')
   args = parser.parse_args()
   start_solution_filename = args.start_solution_filename
   problem_filename = args.problem_filename

   print(problem_filename)

   """define the probability that decides if change each parameter or not"""
   probability = 0.5
   best_output = ""

   """extract the information about the number of customers, Trucks and Goods from the problem file"""
   problemFile = open(problem_filename)
   lines = problemFile.readlines()
   C = int(lines[0].split(" ")[2][:-2])+1
   T = int(lines[1].split(" ")[2][:-2])
   G = int(lines[2].split(" ")[2][:-2])

   fin = open(start_solution_filename)
   lines = fin.readlines()
   current_score = float(lines[0][:-1].split(", ")[2])

   """a counter to count how many times the score is not improved"""
   count = 0
   """if this program does not improve this many times consecutively, terminate this program"""
   terminate_times = 50
   while True:
       if count > 0:
           print(count)
       else:
           print(current_score)

       allocation_array = [0 for i in range(C*T*G)]

       """extract parameters from current allocation table and store in the allocation_array"""
       for line in lines[1:]:
           if len(line) < 2:
               break
           if line[-1] == "\n":
               line = line[:-1]

           parameters = line.split(",")
           truck_id = int(parameters[0])
           customer_id = int(parameters[2])
           chill_goods = int(parameters[3])
           ambient_goods = int(parameters[4])

           index = (truck_id-1) * (C * G) + (customer_id) * 2
           allocation_array[index] = chill_goods
           allocation_array[index+1] = ambient_goods

       """create keep.dzn file and write the parameters that are passed to minizinc program"""
       file_keep = open("keep.dzn","w")
       file_keep.write("allocation = array3d(trucks, customers, goods,[")
       for i in allocation_array:
           if random.random() < probability:
               file_keep.write("_,")
           else:
               file_keep.write(str(i) + ",")
       file_keep.write("]);")
       file_keep.close()

    #    for debug
    #    keep_dzn = open("keep.dzn")
    #    keep_dzn_lines = keep_dzn.readlines()
    #    print(keep_dzn_lines)

       """call the minizinc program"""
       process = subprocess.Popen(['minizinc', 'Logistics-sat.mzn', problem_filename, 'keep.dzn', "--soln-sep", "", "--search-complete-msg", ""], stdout=subprocess.PIPE)
       output, err = process.communicate()
       output = output.decode("utf-8")
       new_score = float(output.split("\n")[0].split(", ")[2])

       """if new score is better than current score, update the score and parameters information"""
       if new_score < current_score:
           count = 0
           probability = 0.5
           current_score = new_score
           print(output)
           best_output = output
           lines = output.split("\n")
        #    for debug
        #    fout = open("test.csv", "w")
        #    fout.write(output)
        #    fout.close()
       else:
           count+=1
           """as the number of times this program stop improving, increase the probability that modify the parameters to search widely"""
           if count % 10 == 0:
               probability += 0.05
           """if this program stop improving the score certain times consecutively terminate this program"""
           if count == terminate_times:
               file_result = open("best-solution-" + str(T) + "-" + str(C-1) + ".csv", "w")
               file_result.write(best_output)
               file_result.close()
               print("best score is " + str(current_score))
               exit()
