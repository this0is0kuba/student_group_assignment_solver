include "globals.mzn"; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Basic info about classes
% --------------------------------------------------
int: number_students;
int: number_instructors;
int: number_subjects;
int: number_class_types;
int: number_classes;

set of int: Student = 1..number_students;
set of int: Instructor = 1..number_instructors;
set of int: Subject = 1..number_subjects;
set of int: ClassType = 1..number_class_types;
set of int: Class = 1..number_classes;

array[Class] of ClassType: class_type;
array[Class] of Subject: class_subject;
array[Class] of Instructor: class_instructor;
array[Class] of int: class_time_h;

array[ClassType] of int: class_type_min_students;
array[ClassType] of int: class_type_max_students;
% --------------------------------------------------

% More constraints
% --------------------------------------------------
array[Instructor] of int: instructor_max_h;
% --------------------------------------------------

% Main array - students' subjects
% --------------------------------------------------
array[Student, Subject] of bool: student_subject;
% --------------------------------------------------

% Student's friends
% --------------------------------------------------
int: max_number_friends;
bool: friend_flag;

set of int: Friend = 1..max_number_friends;

array[Student, Friend] of int: student_friend;
% --------------------------------------------------

%Importance of parallel groups
% --------------------------------------------------
int: weight;
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Student group equals 0 when a student doesn't attend a subject and doesn't equal 0 when student attends a subject.
% --------------------------------------------------
int: max_number_of_groups = number_students div min(class_type_min_students) + 1; 
set of int: Group = 0..max_number_of_groups;

array[Student, Class] of var Group: student_group;

constraint forall(s in Student, c in Class where not student_subject[s, class_subject[c]]) (
    student_group[s, c] == 0
);

constraint forall(s in Student, c in Class where student_subject[s, class_subject[c]]) (
    student_group[s, c] != 0
);
% --------------------------------------------------


% Number of groups in class equals sum of distinct groups for that class.
% --------------------------------------------------
array[Class] of var Group: number_of_groups_in_class;

constraint forall(c in Class) (
  number_of_groups_in_class[c] = nvalue([student_group[s, c] | s in Student where student_group[s, c] != 0])
);
% --------------------------------------------------


% Student group indexes are consecutive natural numbers - we want groups like: [0, 1, 2] instead of: [0, 4, 9].
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_groups_in_class[c] == max([student_group[s, c] | s in Student])
);
% --------------------------------------------------


% Sum of students in each group.
% --------------------------------------------------
array[Class, Group] of var 0..number_students: number_of_students_in_group;

constraint forall(c in Class, g in Group where g <= number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] == sum(s in Student where student_group[s, c] == g) (1) 
);

constraint forall(c in Class, g in Group where g > number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] == 0
);
% --------------------------------------------------


% Sum of students in each group is within the appropriate range.
% --------------------------------------------------
constraint forall(c in Class, g in Group where g != 0 /\ g <= number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] <= class_type_max_students[class_type[c]]
  /\
  number_of_students_in_group[c, g] >= class_type_min_students[class_type[c]]
);
% --------------------------------------------------


% Instructor hours.
% --------------------------------------------------
array[Instructor] of var 0..max(instructor_max_h): instructor_h;

constraint forall(i in Instructor) (
  instructor_h[i] = sum(c in Class where class_instructor[c] == i) (class_time_h[c] * number_of_groups_in_class[c])
);
% --------------------------------------------------


% No instructor can have more hours than allowed to him.
% --------------------------------------------------
constraint forall(i in Instructor) (
  instructor_h[i] <= instructor_max_h[i]
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% We want to minimize the number of groups that have students in common. It's easier to set a schedule when more groups are disjoint.
% --------------------------------------------------
% function var set of int: get_intersection_of_groups(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =
%   {s1 | s1 in Student where student_group[s1, c1] == g1}
%     intersect
%   {s2 | s2 in Student where student_group[s2, c2] == g2};

function var bool: are_groups_have_students_in_common(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =

    exists (s in Student where student_group[s, c1] == g1) (student_group[s, c2] == g2);

%     sum (
%       s in Student where student_group[s, c1] == g1
%      ) (bool2int(student_group[s, c2] == g2)) > 0;
    
%     card(get_intersection_of_groups(c1, g1, c2, g2)) > 0;


var int: meet_condition_magic_number = sum(
  c1 in Class, 
  g1 in Group where g1 != 0 /\ g1 <= number_of_groups_in_class[c1],
  c2 in Class where c1 < c2 /\ class_instructor[c1] != class_instructor[c2],
  g2 in Group where g2 != 0 /\ g2 <= number_of_groups_in_class[c2]) (
  
    bool2int(not are_groups_have_students_in_common(c1, g1, c2, g2))
    
);
% --------------------------------------------------


% Number of friends in the same groups. 
% --------------------------------------------------
% function var set of int: get_set_of_frends(var Class: c, var Group: g, var Student: s) = 
%   {s1 | s1 in Student where student_group[s1, c] == g}
%     intersect
%   {student_friend[s, f] | f in Friend where student_friend[s, f] != 0};
 
 
function var int: get_number_of_friends_in_group(var Class: c, var Group: g, var Student: s) =

      exists (f in Friend where student_friend[s, f] != 0) (student_group[student_friend[s, f], c] == g);

%     sum (
%       f in Friend where student_friend[s, f] != 0
%     ) (bool2int(student_group[student_friend[s, f], c] == g)) > 0;
    
%     card(get_set_of_frends(c, g, s));

var int: number_friends = sum(
  c in Class, 
  g in Group where g != 0 /\ g <= number_of_groups_in_class[c],
  s in Student where student_group[s, c] == g) (
  
  get_number_of_friends_in_group(c, g, s)
  
);
% --------------------------------------------------


% meet_conditon_magic_number < 45 * 22 ~= 1000
% number_of_friends < 100 * 3 * 45 = 13500

var int: obj = weight * meet_condition_magic_number + bool2int(friend_flag) * number_friends;
solve maximize obj;

output
["meet_condition_magic_number: ", show(meet_condition_magic_number), ";\n"] ++
["number_friends: ", show(number_friends), ";\n"] ++
["students' groups: ", show(student_group), ";\n"];