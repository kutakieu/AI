int: C;					  % Number of customers
int: T;                     		  % Number of trucks
int: G;                     		  % Number of goods types 
int: MAXCAP;                		  % Upper bound on truck capacity

set of int: trucks = 1..T;    	     	  % Set of trucks
set of int: customers = 0..C;        	  % Set of customers. Includes depot as customer 0
set of int: goods = 1..G;            	  % Set of goods types
int: chilled = 1;  int: ambient = 2; 	  % Good types

array[trucks] of int: cap;	     	  % Capacity of trucks
array[trucks] of bool: refrig;	     	  % Whether or not trucks are refrigerated
array[goods,customers] of int: order;	  % Number of units of goods types ordered by customers

% array that saves how the number of each type of goods that each truck carries to each customer
array[trucks, customers, goods] of var int: allocation;

% Insert your variables and constraints here

% each allocation cannot exceeds the capacity of each truck
constraint forall(i in trucks, j in customers, k in goods)(allocation[i,j,k]>=0 /\ allocation[i,j,k]<=cap[i]);
% the total number of goods that trucks carry must be same as the order
constraint forall(j in customers, k in goods)(sum(i in trucks)(allocation[i,j,k]) = order[k, j]);
% the total number of allocation of each truck has to be less than the truck's capacity
constraint forall(i in trucks)(cap[i] >= sum(j in customers, k in goods)(allocation[i,j,k]));
% the numbers of chilled goods that not refrigerated trucks carry have to be 0
constraint forall(i in trucks, j in customers, k in goods)(if refrig[i] = false  then allocation[i,j,chilled] = 0 else true endif);

% In question Q1, we are only finding a satisfying solution
solve satisfy;


% Write a Minizinc output item to print the solution in the desired format for Q1

% output [show(allocation)];
output[show(T) ++","++ show(C) ++ "\n"];
output [if (fix(allocation[i,j,chilled]) != 0 \/ fix(allocation[i,j,ambient]) != 0) then
show(i)++","++ show(j)++","++ show(allocation[i,j,chilled])++","++show(allocation[i,j,ambient]) 
  ++ "\n" else "" endif |
  i in trucks, j in customers
];


