int: n;
array[0..n-1] of var 0..n: s;
var int: k;
constraint k=0;

constraint forall(i in 0..n-1) (
   s[i] = (sum(j in 0..n-1)(bool2int(s[j]=i))));

solve satisfy;   

output [if k = 0 then show(k) else "aaa" endif];
output ["\n"];
output [ "s = ", show(s), ";\n" ] ;

int: T = 4;
int: C = 2;
set of int: trucks = 1..T;    	     	  % Set of trucks
set of int: customers = 1..C;  
array[trucks] of var customers: a;
output[show(a)];