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

array[Subject] of int: subject_ects;
array[Subject] of Section: subject_section;

array[Class] of ClassType: class_type;
array[Class] of Subject: class_subject;
array[Class] of Instructor: class_instructor;
array[Class] of int: class_time_h;
% --------------------------------------------------


% Info about science club, science research
% --------------------------------------------------
int: science_club_ects;
int: science_research_ects;
int: science_club_section;
int: science_research_section;

array[Student] of bool: student_science_club;
array[Student] of bool: student_science_research;
% --------------------------------------------------


% Constraints
% --------------------------------------------------
array[Instructor] of int: instructor_max_h;

array[Section] of int: section_min_ects;
array[Section] of int: section_max_ects;
array[Section] of int: section_min_subjects;

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


% Instructor hours. We assume the most optymistic situation. We check if it's possible to create grous. Is there a situation in which instructor is able to handle all the groups for his class.
% --------------------------------------------------
array[Instructor] of var 0..max(instructor_max_h): instructor_h;

function var int: ceil_div(var int: a, var int: b) =
    if a mod b == 0 then
        a div b
    else
        a div b + 1
    endif;

constraint forall(i in Instructor) (
  instructor_h[i] = sum(c in Class where class_instructor[c] == i) (
      class_time_h[c] * 
      ceil_div(number_of_students_in_subject[class_subject[c]], class_type_max_students[class_type[c]])
  )
);
% --------------------------------------------------


% No instructor can have more hours than allowed to him. It's related to the previous constraint.
% --------------------------------------------------
constraint forall(i in Instructor) (
  instructor_h[i] <= instructor_max_h[i]
);
% --------------------------------------------------

// repair this, check why output doesn't work, set leccture to have only one group
% Check if it's possible to create grous. Check if there is no too little students in class
% --------------------------------------------------
constraint forall(c in Class) (
  number_of_students_in_subject[class_subject[c]] >= class_type_min_students[class_type[c]]
);
% --------------------------------------------------



% Total ECTS points for each student in each section are sum of all ECTS of his subjets. It's also neccesary to count ects of science club and science research becase each student who's declared particpation in these activities should be assined to them.
% --------------------------------------------------
array[Student, Section] of var min(section_min_ects)..max(section_max_ects): sum_student_ects_in_section;

constraint forall(st in Student, sc in Section) (
  sum_student_ects_in_section[st, sc] == 
      sum(sb in Subject where student_subject[st, sb] /\ subject_section[sb] == sc) (subject_ects[sb])
      +
      bool2int(science_club_section == sc) * student_science_club[st] * science_club_ects
      +
      bool2int(science_research_section == sc) * student_science_research[st] * science_research_ects
);
% --------------------------------------------------


% Each student has appropriate number of ECTS in each section.
% --------------------------------------------------
constraint forall(st in Student, sc in Section) (
  sum_student_ects_in_section[st, sc] <= section_max_ects[sc]
  /\
  sum_student_ects_in_section[st, sc] >= section_min_ects[sc]
);
% --------------------------------------------------


% Total number of subjects for each student in each section. Similar to sum of ECTS
% --------------------------------------------------
array[Student, Section] of var int: sum_student_subjects_in_section;

constraint forall(st in Student, sc in Section) (
  sum_student_subjects_in_section[st, sc] == 
      sum(sb in Subject where student_subject[st, sb] /\ subject_section[sb] == sc) (1)
      +
      bool2int(science_club_section == sc) * student_science_club[st]
      +
      bool2int(science_research_section == sc) * student_science_research[st]
);
% --------------------------------------------------


% Each student has appropriate number of subjects in each section.
% --------------------------------------------------
constraint forall(st in Student, sc in Section) (
  sum_student_subjects_in_section[st, sc] >= section_min_subjects[sc]
);
% --------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Students' happiness is equal to sum of the subject's points given by students. We count the points only of the subjects that have started.
% --------------------------------------------------
var int: students_happiness = sum(st in Student, sb in Subject) (
 student_subject[st, sb] * pow(student_preferences[st, sb], 2)
);
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
["student_subject: ", show(student_subject), ";\n"];



