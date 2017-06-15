int: w = 3;
int: h = 3;
float: v = (w*w*w + w)/2;
% array[1..w,1..h] of var int: square;
array[1..w*h] of var int: square;
include "alldifferent.mzn";
% constraint forall(i in 1..w, j in 1..h)(square[i,j]>0 /\ square[i,j]<10);
% constraint forall(i in 1..w)(square[i,1] + square[i,2] + square[i,3] = v);
% constraint forall(i in 1..h)(square[1,i] + square[2,i] + square[3,i] = v);
% constraint forall(i in 1..h)(square[i,i] + square[i,i] + square[i,i] = v);
% constraint forall(i in 1..h)(square[w-i+1,i] + square[w-i+1,i] + square[w-i+1,i] = v);

constraint forall(i in 1..w*h)(square[i]>0 /\ square[i]<10);
constraint forall(i in 0..w-1)(square[i*w+1] + square[i*w+2] + square[i*w+3] = v);
constraint forall(i in 1..h)(square[i] + square[i+w] + square[i+2*w] = v);
constraint square[1*1] + square[2*2] + square[3*3] = v;
constraint square[w] + square[w+2*1] + square[w+2*2] = v;

% constraint forall(i in 1..w)(forall(j in 1..h)())
constraint alldifferent(square);

solve satisfy;
output [show(square)];
% output [show(square[1,i], square[2,i], square[3,i])), "\n"];

% output [ show(square[i,j]) ++
%   if j == h then "\n" else " " endif |
%   i in 1..w, j in 1..h
% ];