int: C;					  % Number of customers
int: T;                     		  % Number of trucks
int: G;                     		  % Number of goods types 
int: MAXCAP;                		  % Upper bound on truck capacity

set of int: trucks = 1..T;    	     	  % Set of trucks
set of int: customers = 0..C;        	  % Set of customers. Includes depot as customer 0
set of int: goods = 1..G;            	  % Set of goods types
int: chilled = 1;  int: ambient = 2; 	  % Good types
set of int: times = 0..C+1;            	  % Enough times to visit each customer once and depot twice if needed

array[trucks] of int: cap;	     	  % Capacity of trucks
array[trucks] of bool: refrig;	     	  % Whether or not trucks are refrigerated
array[goods,customers] of int: order;	  % Number of units of goods types ordered by customers

array[trucks] of var customers: visits;

array[trucks, customers, goods] of var int: allocation;

% an array that stores the order of customers that each truck goes to.
array[trucks, times] of var int: time_table;

% Insert your variables and constraints here
% these 4 constraints are same as Q1's constraints.
constraint forall(i in trucks, j in customers, k in goods)(allocation[i,j,k]>=0 /\ allocation[i,j,k]<=cap[i]);
constraint forall(j in customers, k in goods)(sum(i in trucks)(allocation[i,j,k]) = order[k, j]);
constraint forall(i in trucks)(cap[i] >= sum(j in customers, k in goods)(allocation[i,j,k]));
constraint forall(i in trucks, j in customers, k in goods)(if refrig[i] = false  then allocation[i,j,chilled] = 0 else true endif);

% determine the number of customers that each truck goes to
constraint forall(i in trucks) (
   visits[i] = (sum(j in customers)(bool2int(allocation[i,j,chilled] !=0 \/ allocation[i,j,ambient] !=0)))
);

% if t = 0 or t is greater than the number of customers that each truck goes to, time table value has to be 0
constraint forall(i in trucks, t in times)(if t=0 \/ t>visits[i] then time_table[i, t] = 0 else time_table[i, t]>0 /\ time_table[i, t]<=C endif);
%if the allocation for a customer is 0, the customer is not included in the time table
constraint forall(i in trucks, j in customers, t in times where j>0)(if allocation[i,j,chilled]=0 /\ allocation[i,j,ambient]=0 then time_table[i, t] != j else true endif);
% if the values of the time table is not 0, they have to be different
constraint forall(i in trucks, t_1, t_2 in times where t_1 != t_2)(if time_table[i,t_1]!=0 /\ time_table[i,t_2]!=0 then time_table[i, t_1] != time_table[i,t_2] else true endif);

% In question Q2, we are only finding a satisfying solution
solve satisfy;

% Write a Minizinc output item to print the solution in the desired format for Q2

output[show(T) ++","++ show(C)++"\n"];

output [if fix(time_table[i,t])!=0 then
show(i)++","++ show(t)++","++ show(time_table[i,t])++","++ show(allocation[i,time_table[i,t],chilled])++","++show(allocation[i,time_table[i,t],ambient]) 
  ++ "\n" else "" endif |
  i in trucks, t in times where t!=0
];
