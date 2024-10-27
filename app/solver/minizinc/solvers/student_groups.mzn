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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Main array of variables - students' groups.
% --------------------------------------------------
function int: my_ceil(int: a, int: b) =
    if a mod b == 0 then
        a div b
    else
        a div b + 1
    endif;
    
function int: my_min(array[int] of int: arr) =
    if length(arr) == 1 then
        arr[1]
    else
        min(arr[2..])
    endif;
    
    
int: max_number_of_groups = my_ceil(number_students, my_min(class_type_min_students)); 

set of int: Group = 1..max_number_of_groups;
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


% There is at most 1 group for lectures (It can be 0 when subject hasn't started). We assume the first element in class_type is always lecture
% --------------------------------------------------
constraint forall(c in Class where class_type[c] == 1,
                  g in Group where g != 1) (
  number_of_students_in_group[group_index(c, g)] == 0  
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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

solve satisfy;

output
["transformed student_group: ", show(bool2int(student_group)), ";\n"] ++
["number_of_students_in_group: ", show(number_of_students_in_group), ";\n"] ++
["number_of_groups_in_class: ", show(number_of_groups_in_class), ";\n"] ++
[];



