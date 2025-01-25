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


% Custom Constraints
% --------------------------------------------------
int: number_predetermined_subjects;
set of int: PredeterminedSubject = 1..number_predetermined_subjects;
array[PredeterminedSubject] of Subject: predetermined_subjects;

int: number_predetermined_students;
set of int: PredeterminedStudent = 1..number_predetermined_students;
array[PredeterminedStudent] of Student: predetermined_students;
array[PredeterminedStudent, Subject] of 0..number_subjects: predetermined_subjects_for_students;

int: number_conditional_students;
set of int: ConditionalStudent = 1..number_conditional_students;
array[ConditionalStudent] of Student: conditional_students;
% --------------------------------------------------


% The happiness of the saddest student
% --------------------------------------------------
int: the_saddest_student_happiness;
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Main array of variables - students' subjects.
% --------------------------------------------------
array[Student, Subject] of var bool: student_subject;
% --------------------------------------------------


% Sum of students in each subject (conditional students and normal students).
% --------------------------------------------------
array[Subject] of var int: number_of_students_in_subject;

constraint forall(sb in Subject) (
  number_of_students_in_subject[sb] == sum(st in Student) (student_subject[st, sb])
);
% --------------------------------------------------


% Sum of conditional students in each subject. 
% --------------------------------------------------
array[Subject] of var int: number_of_conditional_students_in_subject;

constraint forall(sb in Subject) (
  number_of_conditional_students_in_subject[sb] == sum(st in ConditionalStudent) (student_subject[conditional_students[st], sb])
);
% --------------------------------------------------


% Instructor hours. We assume the most optimistic situation. We check if it's possible to create groups. Should be a situation in which instructor is able to handle all the groups for his classes.
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


% Check if it's possible to create groups. Check if there is no too little students in class. We need to remember about the conditional students. It's necessary to consider a situation without them and check if the condition is still met.
% --------------------------------------------------
constraint forall(c in Class) (

  (
   number_of_students_in_subject[class_subject[c]] - 
   number_of_conditional_students_in_subject[class_subject[c]]
  )  
    >= class_type_min_students[class_type[c]]
    
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
  

% We can't reduce the happiness of the saddest student
% --------------------------------------------------
var int: the_saddest_student_happiness_var; 

constraint the_saddest_student_happiness_var == min(student_happiness_array);
constraint the_saddest_student_happiness_var >= the_saddest_student_happiness;
% --------------------------------------------------


% Students' happiness is equal to sum of the subject's points given by students. We count the points only of the subjects that have started.
% --------------------------------------------------
var int: students_happiness; 

constraint students_happiness = sum(st in Student, sb in Subject) (
  student_subject[st, sb] * student_preferences[st, sb]
);
% --------------------------------------------------

solve maximize students_happiness;

output
["students_happiness: ", show(students_happiness), ";\n"] ++
["student_subject: ", show(student_subject), ";\n"] ++ 
["number_of_students_in_subject", show(number_of_students_in_subject)];



