include "globals.mzn"; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Basic info about classes
% --------------------------------------------------
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

array[Student] of int: student_average;
array[Subject] of Section: subject_section;

array[Class] of ClassType: class_type;
array[Class] of Subject: class_subject;
array[Class] of Instructor: class_instructor;
array[Class] of int: class_time_h;
% --------------------------------------------------


% Constraints
% --------------------------------------------------
array[Instructor] of int: instructor_max_h;

array[Student, Section] of 0..number_subjects: student_subjects_in_section;

array[ClassType] of int: class_type_min_students;
array[ClassType] of int: class_type_max_students;
% --------------------------------------------------


% Preferences
% --------------------------------------------------
array[Student, Subject] of Subject: student_preferences;
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Main array of variables - students' subjects.
% --------------------------------------------------
array[Student, Subject] of var bool: student_subject;
% --------------------------------------------------


% Sum of students in each subject.
% --------------------------------------------------
array[Subject] of var int: number_of_students_in_subject;

constraint forall(sb in Subject) (
  number_of_students_in_subject[sb] == sum(st in Student) (student_subject[st, sb])
);
% --------------------------------------------------


% Instructor hours. We assume the most optymistic situation. We check if it's possible to create grous. Should be a situation in which instructor is able to handle all the groups for his classes.
% --------------------------------------------------
array[Instructor] of var 0..max(instructor_max_h): instructor_h;

function var int: my_ceil(var int: a, var int: b) =
    if a mod b == 0 then
        a div b
    else
        a div b + 1
    endif;

constraint forall(i in Instructor) (
  instructor_h[i] = sum(c in Class where class_instructor[c] == i) (
      class_time_h[c] * 
      my_ceil(number_of_students_in_subject[class_subject[c]], class_type_max_students[class_type[c]])
  )
);
% --------------------------------------------------


% No instructor can have more hours than allowed to him. It's related to the previous constraint.
% --------------------------------------------------
constraint forall(i in Instructor) (
  instructor_h[i] <= instructor_max_h[i]
);
% --------------------------------------------------


% Check if it's possible to create groups. Check if there is no too little students in class
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_students_in_subject[class_subject[c]] >= class_type_min_students[class_type[c]]
  \/
  number_of_students_in_subject[class_subject[c]] == 0
);
% --------------------------------------------------


% Total number of subjects for each student in each section.
% --------------------------------------------------
array[Student, Section] of var int: student_subjects_in_section_var;

constraint forall(st in Student, sc in Section) (
  student_subjects_in_section_var[st, sc] == 
      sum(sb in Subject where student_subject[st, sb] /\ subject_section[sb] == sc) (1)
);
% --------------------------------------------------


% Each student has appropriate number of subjects in each section.
% --------------------------------------------------
constraint forall(st in Student, sc in Section) (
  student_subjects_in_section_var[st, sc] == student_subjects_in_section[st, sc]
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Students' happiness is equal to sum of the subject's points given by students. We count the points only of the subjects that have started.
% --------------------------------------------------
var int: students_happiness = pow(
  sum(st in Student, sb in Subject) (student_subject[st, sb] * student_preferences[st, sb]), 
  2);
% --------------------------------------------------


% students_happiness_with_average is equal to sum of the subject's points given by students multiped by student's average. We count the points only for the subjects that started.
% --------------------------------------------------
var int: students_happiness_with_average = sum(st in Student, sb in Subject) (
 student_preferences[st, sb] * student_subject[st, sb] * student_average[st]
);
% --------------------------------------------------


% The weight is used to make students_happiness always grater than students_happiness_with_average. We want students with a higher average to be happier while only one student with a lower average will be sadder (not more than one)
% --------------------------------------------------
var int: weight = (max(student_average) - min(student_average)) * number_students;
% --------------------------------------------------

var int: obj = weight * students_happiness + students_happiness_with_average;
solve maximize obj;

output
["obj: ", show(obj), ";\n"] ++
["students_happiness: ", show(students_happiness), ";\n"] ++
["student_subject: ", show(student_subject), ";\n"] ++ 
["number_of_students_in_subject", show(number_of_students_in_subject)];



