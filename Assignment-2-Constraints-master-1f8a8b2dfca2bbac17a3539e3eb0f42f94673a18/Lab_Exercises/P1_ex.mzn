% Baking cakes for the school fete
var int: a;
var int: b;
var int: c;
var int: d;

% flour
constraint a > 0;
constraint b < 7;
constraint c > 3;
constraint d < a + b;
constraint d*2 > a + b + c;
constraint b - c > a;

% maximize our profit
solve satisfy;
output ["a = ", show(a), "\n","b = ", show(b), "\n","c = ", show(c), "\n","d = ", show(d), "\n"];
% output ["result"];