
enum person = {A, B, C, D, E, F};
array[person] of var 1..2: floor;
array[person] of var 1..3: roomNumber;
int: a = 3;
int: b = 3;
constraint floor[A] = 2;
constraint floor[B] = 1;
constraint floor[D] = 2;
constraint roomNumber[A] = roomNumber[B];
constraint abs(roomNumber[A] - roomNumber[D]) = 1;
constraint roomNumber[E] < roomNumber[F];
constraint abs(roomNumber[C] - roomNumber[F]) = 1;
% constraint ((floor[A] != floor[C]) \/ (roomNumber[A] != roomNumber[C])) /\ not((floor[A] != floor[C]) /\ (roomNumber[A] != roomNumber[C]))

constraint %% ensure the tasks occur in sequence forall(i in 1..jobs) (
forall( i in 1..length(person))(
  forall(j in 2..length(person))(
  if i = j then true else
    ((floor[person[i]] != floor[person[j]]) \/ (roomNumber[person[i]] != roomNumber[person[j]])) /\ not((floor[person[i]] != floor[person[j]]) /\ (roomNumber[person[i]] != roomNumber[person[j]]))
  endif
  )
);
        
% % maximize our profit
solve satisfy;
output ["A = ", show(floor[A]), show(roomNumber[A]), "\n","B = ", show(floor[B]), show(roomNumber[B]), "C = ", show(floor[C]), show(roomNumber[C]), "\n","D = ", show(floor[D]), show(roomNumber[D]),"E = ", show(floor[E]), show(roomNumber[E]), "\n","F = ", show(floor[F]), show(roomNumber[F])];
% output [forall(i in 1..3)(show(i))];
output [show(length(person))];
% output [show(floor[A])];
% output ["result"];