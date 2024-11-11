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
% --------------------------------------------------


% Constraints
% --------------------------------------------------
array[Instructor] of int: instructor_max_h;

array[ClassType] of int: class_type_min_students;
array[ClassType] of int: class_type_max_students;
% --------------------------------------------------


% Main array of variables - students' subjects.
% --------------------------------------------------
array[Student, Subject] of bool: student_subject;
% --------------------------------------------------


% Info about groups
% --------------------------------------------------
int: max_number_of_groups; 

set of int: Group = 0..max_number_of_groups;

array[Class] of Group: min_number_of_groups_in_class;
% --------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Student group equals 0 when a student doesn't attend a subject and doesn't equal 0 when student attends a subject.
% --------------------------------------------------
array[Student, Class] of var Group: student_group;

constraint forall(s in Student, c in Class where not student_subject[s, class_subject[c]]) (
    student_group[s, c] == 0
);

constraint forall(s in Student, c in Class where student_subject[s, class_subject[c]]) (
    student_group[s, c] != 0
);
% --------------------------------------------------


% We force solver to choose the min possible number of groups for each class.
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_groups_in_class[c] == min_number_of_groups_in_class[c]
);
% --------------------------------------------------


% Number of groups in class equals sum of distinct groups for that class.
% --------------------------------------------------
array[Class] of var Group: number_of_groups_in_class;

constraint forall(c in Class) (
  number_of_groups_in_class[c] == nvalue([student_group[s, c] | s in Student where student_group[s, c] != 0])
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


% There is at most 1 group for lectures (It can be 0 when subject hasn't started). We assume the first element in class_type is always lecture
% --------------------------------------------------
constraint forall(c in Class where class_type[c] == 1) (
  number_of_groups_in_class[c] <= 1
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


% Number of students in each class.
% --------------------------------------------------
array[Class] of var 0..number_students: number_of_students_in_class;

constraint forall(c in Class) (
  number_of_students_in_class[c] == sum(g in Group where g != 0) (number_of_students_in_group[c, g]) 
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Our objective function is the number of groups that have students in common. We check each pair
% --------------------------------------------------
function var bool: are_groups_have_students_in_common(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =
    sum(s in Student where student_group[s, c1] == g1 /\ student_group[s, c2] == g2) (1) > 0;

var int: groups_with_common_students;

constraint groups_with_common_students == sum (
                  c1 in Class where number_of_students_in_class[c1] > 0,
                  g1 in Group where g1 != 0 /\ g1 <= number_of_groups_in_class[c1],
                  c2 in Class where c2 > c1 /\
                                    class_instructor[c1] != class_instructor[c2],
                  g2 in Group where g2 != 0 /\ g2 <= number_of_groups_in_class[c2]) (
                  
    bool2int(are_groups_have_students_in_common(c1, g1, c2, g2))
);
% --------------------------------------------------

solve minimize groups_with_common_students;

output
["student_group: ", show(student_group), ";\n"] ++
["groups_with_common_students: ", show(groups_with_common_students), ";\n"] ++
% ["number_of_students_in_group: ", show(number_of_students_in_group), ";\n"] ++
% ["number_of_groups_in_class: ", show(number_of_groups_in_class), ";\n"] ++
% ["number_of_students_in_class: ", show(number_of_students_in_class), ";\n"] ++
[];