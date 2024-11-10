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


% Students' subjects.
% --------------------------------------------------
array[Student, Subject] of bool: student_subject;
% --------------------------------------------------

% Info about groups
% --------------------------------------------------
int: max_number_of_groups; 

set of int: Group = 1..max_number_of_groups;

array[Class] of Group: min_number_of_groups_in_class;
% --------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Main array of variables - students' groups.
% --------------------------------------------------
set of int: AllGroups = 1..max_number_of_groups*number_classes;

array[Student, AllGroups] of var bool: student_group;
% --------------------------------------------------


% Student group equals false when a student doesn't attend a group
% --------------------------------------------------
array[AllGroups] of Class: group_class = [(g - 1) div max_number_of_groups + 1 | g in AllGroups];
array[AllGroups] of Class: group_subject = [class_subject[group_class[g]] | g in AllGroups]; 

constraint forall(s in Student, 
                  g in AllGroups where not student_subject[s, group_subject[g]]) ( 
  student_group[s, g] == false
);
% --------------------------------------------------


% Student group equals true when a student is in a group. Student can be only in one group per class
% --------------------------------------------------
function var int: group_index(var Class: c, var Group: g) =
  (c-1)*max_number_of_groups + g;

constraint forall(s in Student,
                  c in Class where student_subject[s, class_subject[c]]) (
                  
    sum(g in Group) (bool2int(student_group[s, group_index(c, g)])) == 1
  
);
% --------------------------------------------------


% Sum of students in each group.
% --------------------------------------------------
array[AllGroups] of var 0..number_students: number_of_students_in_group;

constraint forall(g in AllGroups) (
  number_of_students_in_group[g] == sum(s in Student) (bool2int(student_group[s, g])) 
);
% --------------------------------------------------


% Sum of students in each group is within the appropriate range.
% --------------------------------------------------
constraint forall(g in AllGroups) (
    ( 
      number_of_students_in_group[g] <= class_type_max_students[class_type[group_class[g]]]
      /\
      number_of_students_in_group[g] >= class_type_min_students[class_type[group_class[g]]]
    )
    \/
      number_of_students_in_group[g] == 0
    
);
% ---------------------------------------------


% Student group indexes are consecutive natural numbers - we want groups for class like: [0, 1, 2] instead of: [0, 4, 9]. If some group has no students then the group with higher index shouldn't have studnets as well. 
% --------------------------------------------------
constraint forall(g1 in AllGroups, 
                  g2 in AllGroups where g2 == g1 + 1 /\ group_class[g1] == group_class[g2]) (
  number_of_students_in_group[g1] == 0 -> number_of_students_in_group[g2] == 0
);
% --------------------------------------------------


% We force solver to choose the min possible number of groups for each class.
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_groups_in_class[c] == min_number_of_groups_in_class[c]
);
% --------------------------------------------------


% Number of groups in class
% --------------------------------------------------
array[Class] of var 0..max_number_of_groups: number_of_groups_in_class;

constraint forall(c in Class) (
  number_of_groups_in_class[c] == 
    sum(g in Group where number_of_students_in_group[group_index(c, g)] != 0) (1)
);
% --------------------------------------------------


% Instructor hours.
% --------------------------------------------------
array[Instructor] of var 0..max(instructor_max_h): instructor_h;

constraint forall(i in Instructor) (
  instructor_h[i] == sum(c in Class where class_instructor[c] == i) (class_time_h[c] * number_of_groups_in_class[c])
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
  number_of_students_in_class[c] == sum(g in Group) (number_of_students_in_group[group_index(c, g)]) 
);
% --------------------------------------------------


% Break symmetry 
% --------------------------------------------------
constraint forall(g1 in AllGroups where
                    number_of_students_in_group[g1] > 0,
                  g2 in AllGroups where 
                    g2 == g1 + 1 /\
                    group_class[g1] == group_class[g2] /\ 
                    number_of_students_in_group[g2] > 0) (
                    
  lex_greatereq(student_group[.., g1], student_group[.., g2])
);
% --------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Z
% --------------------------------------------------
array[AllGroups, AllGroups] of var 0..1: array_z;

constraint forall(g1 in AllGroups where 
                     number_of_students_in_group[g1] > 0,
                     
                  g2 in AllGroups where 
                     g2 > g1 /\ number_of_students_in_group[g2] > 0 /\ 
                     group_class[g1] != group_class[g2] /\
                     class_instructor[group_class[g1]] != class_instructor[group_class[g2]],
                     
                  s in Student ) (

  array_z[g1, g2] >= student_group[s, g1] + student_group[s, g2] - 1
                                                      
);
% --------------------------------------------------

solve minimize sum(array_z);

output
["groups_with_common_students: ", show(sum(array_z)), ";\n"] ++
% ["Group: ", show(Group), ";\n"] ++
% ["transformed student_group: ", show(student_group), ";\n"] ++
% ["number_of_students_in_group: ", show(number_of_students_in_group), ";\n"] ++
% ["number_of_groups_in_class: ", show(number_of_groups_in_class), ";\n"] ++
% ["number_of_students_in_class: ", show(number_of_students_in_class), ";\n"] ++
[];



