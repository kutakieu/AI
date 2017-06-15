% Baking cakes for the school fete
var int: a;
var int: b;


% flour
constraint a > 0;
constraint a < 3;
constraint b < 3;
constraint b > 0;
constraint a + b < 5;


% maximize our profit
solve satisfy;
output ["a = ", show(a), "\n","b = ", show(b)];
% output ["result"];