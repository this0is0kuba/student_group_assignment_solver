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


% Info about students' hapiness
% --------------------------------------------------
int: students_happiness;
int: the_saddest_student_happiness;
% --------------------------------------------------


% Custom Constraints
% --------------------------------------------------
int: number_predetermined_subjects;
set of int: PredeterminedSubject = 1..number_predetermined_subjects;
array[PredeterminedSubject] of Subject: predetermined_subjects;

int: number_predetermined_students;
set of int: PredeterminedStudent = 1..number_predetermined_students;
array[PredeterminedStudent] of Student: predetermined_students;
array[PredeterminedStudent, Subject] of 0..number_subjects: predetermined_subjects_for_students;
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


% We force solver to open subjects that are predetermined. 
% --------------------------------------------------
constraint forall(s in PredeterminedSubject) (
  number_of_students_in_subject[predetermined_subjects[s]] > 0
);
% --------------------------------------------------


% We force solver to assign students to their predefined subjects
% --------------------------------------------------
constraint forall(st in PredeterminedStudent, sb in Subject where
   predetermined_subjects_for_students[st, sb] != 0) (
   
  student_subject[predetermined_students[st], predetermined_subjects_for_students[st, sb]] = true
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% We count happiness for each student
% --------------------------------------------------
array[Student] of var int: student_happiness_array;

constraint student_happiness_array == 
  [ sum(sb in Subject) (student_subject[st, sb] * student_preferences[st, sb]) | st in Student ];
% --------------------------------------------------


% students_happiness is equal to sum of the subject's points given by students. We count the points only of the subjects that have started.
% --------------------------------------------------
var int: students_happiness_var;

constraint students_happiness_var = sum(st in Student, sb in Subject) (
  student_subject[st, sb] * student_preferences[st, sb]
);
% --------------------------------------------------


% students_happiness_with_average is equal to sum of the subject's points given by students multiped by student's average. We count the points only for the subjects that started.
% --------------------------------------------------
var int: students_happiness_with_average;

students_happiness_with_average = sum(st in Student, sb in Subject) (
 (student_subject[st, sb] * student_preferences[st, sb] * student_average[st])
);
% --------------------------------------------------


% We can't reduce the happiness of the saddest student
% --------------------------------------------------
var int: the_saddest_student_happiness_var; 

constraint the_saddest_student_happiness_var == min(student_happiness_array);
constraint the_saddest_student_happiness_var >= the_saddest_student_happiness;
% --------------------------------------------------


% Current students_happiness can not be lower than students_hapiness (the one calculated without taking into account the average)
% --------------------------------------------------
constraint students_happiness_var >= students_happiness;
% --------------------------------------------------


solve maximize students_happiness_with_average;

output
["students_happiness_var: ", show(students_happiness_var), ";\n"] ++
["student_subject: ", show(student_subject), ";\n"] ++ 
["number_of_students_in_subject", show(number_of_students_in_subject)];



