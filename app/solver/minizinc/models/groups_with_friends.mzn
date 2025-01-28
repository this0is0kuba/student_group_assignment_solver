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


% Custom Constraints
% --------------------------------------------------
int: number_predetermined_students;
set of int: PredeterminedStudent = 1..number_predetermined_students;
array[PredeterminedStudent] of Student: predetermined_students;

set of int: PredeterminedClasses = 0..number_classes;

% Each predetermined group is associated with each predetermined class
array[PredeterminedStudent, Class] of PredeterminedClasses: predetermined_classes_for_students;
array[PredeterminedStudent, Class] of int: predetermined_groups_for_students;

int: number_conditional_students;
set of int: ConditionalStudent = 1..number_conditional_students;
array[ConditionalStudent] of Student: conditional_students;
% --------------------------------------------------


% Main array of constants - students' subjects. We have it from the previous solvers.
% --------------------------------------------------
array[Student, Subject] of bool: student_subject;
% --------------------------------------------------


% Info about groups
% --------------------------------------------------
int: max_number_of_groups; 

set of int: Group = 0..max_number_of_groups;

array[Class] of Group: min_number_of_groups_in_class;
int: groups_with_common_students;
% --------------------------------------------------


% Info about Friends
% --------------------------------------------------
int: friends_max_number;
set of int: Friend = 1..friends_max_number;

array[Student, Friend] of 0..number_students: friends_array;
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


% Number of groups in class equals sum of distinct groups for that class. (Redundant Constraint)
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


% Sum of students in each group (conditional students and normal students).
% --------------------------------------------------
array[Class, Group] of var 0..number_students: number_of_students_in_group;

constraint forall(c in Class, g in Group where g <= number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] == sum(s in Student where student_group[s, c] == g) (1) 
);

constraint forall(c in Class, g in Group where g > number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] == 0
);
% --------------------------------------------------


% Sum of conditional students in each group.
% --------------------------------------------------
array[Class, Group] of var 0..number_students: number_of_conditional_students_in_group;

constraint forall(c in Class, g in Group where g <= number_of_groups_in_class[c]) (
  number_of_conditional_students_in_group[c, g] 
    == 
  sum(s in ConditionalStudent where student_group[conditional_students[s], c] == g) (1) 
);

constraint forall(c in Class, g in Group where g > number_of_groups_in_class[c]) (
  number_of_conditional_students_in_group[c, g] == 0
);
% --------------------------------------------------


% Sum of students in each group is within the appropriate range.
% --------------------------------------------------
constraint forall(c in Class, g in Group where g != 0 /\ g <= number_of_groups_in_class[c]) (
  number_of_students_in_group[c, g] <= class_type_max_students[class_type[c]]
  /\
  (number_of_students_in_group[c, g] - number_of_conditional_students_in_group[c, g])
    >= class_type_min_students[class_type[c]]
);
% --------------------------------------------------


% Number of students in each class.
% --------------------------------------------------
array[Class] of var 0..number_students: number_of_students_in_class;

constraint forall(c in Class) (
  number_of_students_in_class[c] == sum(g in Group where g != 0) (number_of_students_in_group[c, g]) 
);
% --------------------------------------------------


% We force solver to assign students to their predefined groups
% --------------------------------------------------
constraint forall(p in PredeterminedStudent, c in Class where 
  predetermined_classes_for_students[p, c] != 0) (
    
  student_group[
    predetermined_students[p], 
    predetermined_classes_for_students[p, c]
  ] 
    == 
  predetermined_groups_for_students[p, c]
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% We cannot reduce the number of groups that have students in common. We check each pair
% --------------------------------------------------
predicate are_groups_have_students_in_common(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =
    sum(s in Student where student_group[s, c1] == g1 /\ student_group[s, c2] == g2) (1) > 0;

var int: groups_with_common_students_var;

constraint groups_with_common_students_var == sum (
                  c1 in Class where number_of_students_in_class[c1] > 0,
                  g1 in Group where g1 != 0 /\ g1 <= number_of_groups_in_class[c1],
                  c2 in Class where c2 > c1 /\
                                    class_instructor[c1] != class_instructor[c2],
                  g2 in Group where g2 != 0 /\ g2 <= number_of_groups_in_class[c2]) (
                  
    bool2int(are_groups_have_students_in_common(c1, g1, c2, g2))
);

constraint groups_with_common_students_var <= groups_with_common_students;
% --------------------------------------------------


% We will maximize the number of friends in each group
% --------------------------------------------------
var int: number_of_friends;

constraint number_of_friends == sum (
            c in Class where number_of_students_in_class[c] > 0,
            g in Group where g != 0 /\ g <= number_of_groups_in_class[c],
            s in Student where student_group[s, c] == g,
            f in Friend where friends_array[s, f] != 0 /\ student_group[friends_array[s, f], c] == g) 
  (1);
% --------------------------------------------------

solve maximize number_of_friends;

output
["student_group: ", show(student_group), ";\n"] ++
["groups_with_common_students_var: ", show(groups_with_common_students_var), ";\n"] ++
["number_of_friends: ", show(number_of_friends), ";\n"] ++
% ["number_of_students_in_group: ", show(number_of_students_in_group), ";\n"] ++
% ["number_of_groups_in_class: ", show(number_of_groups_in_class), ";\n"] ++
% ["number_of_students_in_class: ", show(number_of_students_in_class), ";\n"] ++
[];