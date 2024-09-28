include "globals.mzn"; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Basic info about classes
int: number_students;
int: number_instructors;
int: number_subjects;
int: number_class_types;
int: number_section;
int: number_classes;

set of int: Student = 1..number_students;
set of int: Instructor = 1..number_instructors;
set of int: Subject = 1..number_subjects;
set of int: ClassType = 1..number_class_types;
set of int: Section = 1..number_section;
set of int: Class = 1..number_classes;

array[Subject] of int: subject_ects;
array[Subject] of Section: subject_section;

array[Class] of ClassType: class_type;
array[Class] of Subject: class_subject;
array[Class] of Instructor: class_instructor;
array[Class] of int: class_time_h;

array[ClassType] of int: class_type_min_students;
array[ClassType] of int: class_type_max_students;

% Info about science club, science research, and more constraints
int: science_club_ects;
int: conduct_research_ects;
int: science_club_section;
int: conduct_research_section;

array[Student] of bool: student_science_club;
array[Student] of bool: student_conduct_research;

array[Instructor] of int: instructor_max_h;
array[Section] of int: section_min_ects;
array[Section] of int: section_max_ects;

% Preferences
array[Student, Subject] of Subject: student_preferences;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Main array of variables - students' subjects
% --------------------------------------------------
array[Student, Subject] of var bool: student_subject;
% --------------------------------------------------


% Total ECTS points for each student in each section are sum of all ECTS of his subjets
% --------------------------------------------------
array[Student, Section] of var min(section_min_ects)..max(section_max_ects): sum_student_ects_in_section;

constraint forall(st in Student, sc in Section) (
  sum_student_ects_in_section[st, sc] == 
      sum(sb in Subject where student_subject[st, sb] /\ subject_section[sb] == sc) (subject_ects[sb])
);
% --------------------------------------------------


% Student group equals 0 when a student doesn't attend a subject and doesn't equal 0 when student attends a subject
% --------------------------------------------------
int: max_number_of_groups = number_students div min(class_type_min_students) + 1; 
array[Student, Class] of var 0..max_number_of_groups: student_group;

constraint forall(s in Student, c in Class where not student_subject[s, class_subject[c]]) (
    student_group[s, c] == 0
);

constraint forall(s in Student, c in Class where student_subject[s, class_subject[c]]) (
    student_group[s, c] != 0
);
% --------------------------------------------------


% Number of groups in class equals sum of distinct groups for that class
% --------------------------------------------------
array[Class] of var 0..max_number_of_groups: number_of_groups_in_class;

number_of_groups_in_class = [nvalue([student_group[s, c] | s in Student where student_group[s, c] != 0]) | c in Class];
% --------------------------------------------------


% Student group indexes are consecutive natural numbers - we want groups like: [0, 1, 2] instead of: [0, 4, 9]
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_groups_in_class[c] == max([student_group[s, c] | s in Student])
);

% --------------------------------------------------


% Instructor hours are equal to the sum of hours of all his groups
% --------------------------------------------------
array[Instructor] of var 0..max(instructor_max_h): instructor_h;

instructor_h = [sum(c in Class where class_instructor[c] == i) (class_time_h[c] * number_of_groups_in_class[c])
                | i in Instructor];
% --------------------------------------------------


% No instructor can have more hours than allowed
% --------------------------------------------------
constraint forall(i in Instructor) (
  instructor_h[i] <= instructor_max_h[i]
);
% --------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

var int: obj = 20;
solve minimize obj;

output
["obj: ", show(obj), ";\n"] ++
["student_subject: ", show(student_subject), ";\n"]




