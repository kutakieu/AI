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
array[trucks] of int: centsPerKm;         % Cost of running trucks (in cents per km)
array[customers,customers] of int: D;  	  % Distances between customers (including the depot)

var int: tot_cost;	      	   	  % Total cost of the solution

% Insert your other variables and constraints here
array[trucks] of var customers: visits;
array[trucks, customers, goods] of var int: allocation;

% an array that stores the order of customers that each truck goes to.
array[trucks, times] of var int: time_table;

% by using the time_table array determine the order of customers that each truck goes to and calculate the distance and cost.
tot_cost = sum(i in trucks, t in times where t>0 )(if time_table[i, t]!=0  then centsPerKm[i] * D[time_table[i, t-1], time_table[i, t]] else 0 endif);

% these 8 constraints are same as Q2's constraints.
constraint forall(i in trucks, j in customers, k in goods)(allocation[i,j,k]>=0 /\ allocation[i,j,k]<=cap[i]);
constraint forall(j in customers, k in goods)(sum(i in trucks)(allocation[i,j,k]) = order[k, j]);
constraint forall(i in trucks)(cap[i] >= sum(j in customers, k in goods)(allocation[i,j,k]));
constraint forall(i in trucks, j in customers, k in goods)(if refrig[i] = false  then allocation[i,j,chilled] = 0 else true endif);

constraint forall(i in trucks) (   visits[i] = (sum(j in customers)(bool2int(allocation[i,j,chilled] !=0 \/ allocation[i,j,ambient] !=0)))   );  
constraint forall(i in trucks, t in times)(if t=0 \/ t>visits[i] then time_table[i, t] = 0 else time_table[i, t]>0 /\ time_table[i, t]<=C endif);
constraint forall(i in trucks, j in customers, t in times where j>0)(if allocation[i,j,chilled]=0 /\ allocation[i,j,ambient]=0 then time_table[i, t] != j else true endif);
constraint forall(i in trucks, t_1, t_2 in times where t_1 != t_2)(if time_table[i,t_1]!=0 /\ time_table[i,t_2]!=0 then time_table[i, t_1] != time_table[i,t_2] else true endif);


% In question Q3, we are optimising the total cost
solve minimize tot_cost;
% solve satisfy;

% Write a Minizinc output item to print the solution in the desired format for Q3
output[show(T) ++", "++ show(C) ++", "++ show(fix(tot_cost)/100)];
output["\n"];

output [if fix(time_table[i,t])!=0 then
show(i)++","++ show(t)++","++ show(time_table[i,t])++","++ show(allocation[i,time_table[i,t],chilled])++","++show(allocation[i,time_table[i,t],ambient]) 
  ++ "\n" else "" endif |
  i in trucks, t in times where t!=0
];
