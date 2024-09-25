%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

% Info about science club, science research, constraints
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

