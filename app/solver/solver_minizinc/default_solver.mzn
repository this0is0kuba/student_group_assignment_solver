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
int: science_research_ects;
int: science_club_section;
int: science_research_section;

array[Student] of bool: student_science_club;
array[Student] of bool: student_science_research;

array[Instructor] of int: instructor_max_h;
array[Section] of int: section_min_ects;
array[Section] of int: section_max_ects;

% Preferences
array[Student, Subject] of Subject: student_preferences;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES AND CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Main array of variables - students' subjects.
% --------------------------------------------------
array[Student, Subject] of var bool: student_subject;
% --------------------------------------------------


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
constraint forall(c in Class, g in Group where g <= number_of_groups_in_class[c] /\ g != 0) (
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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

var int: obj = sum(st in Student, sb in Subject) (student_preferences[st, sb] * student_subject[st, sb]);
solve minimize obj;

output
["obj: ", show(obj), ";\n"] ++
["student_subject: ", show(student_subject), ";\n"] ++
[";\n"] ++
["student_group[1, 1]: ", show(student_group[1, 1]), ";\n"] ++
["student_group[2, 1]: ", show(student_group[2, 1]), ";\n"] ++
["student_group[3, 1]: ", show(student_group[3, 1]), ";\n"] ++
["student_group[4, 1]: ", show(student_group[4, 1]), ";\n"] ++
[";\n"] ++
["student_group[1, 4]: ", show(student_group[1, 4]), ";\n"] ++
["student_group[2, 4]: ", show(student_group[2, 4]), ";\n"] ++
["student_group[3, 4]: ", show(student_group[3, 4]), ";\n"] ++
["student_group[4, 4]: ", show(student_group[4, 4]), ";\n"];




