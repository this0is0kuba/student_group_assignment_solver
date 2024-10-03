% We want to minimize the number of groups that have students in common. It's easier to set a schedule when more groups are disjoint.
% --------------------------------------------------
function var set of int: get_intersection_of_groups(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =
  {s1 | s1 in Student where student_group[s1, c1] == g1}
        intersect
  {s2 | s2 in Student where student_group[s2, c2] == g2};

function var bool: are_groups_have_students_in_common(var Class: c1, var Group: g1, var Class: c2, var Group: g2) =
    card(get_intersection_of_groups(c1, g1, c2, g2)) > 0;


var int: violation_of_condition_magic_number = 
            sum(c1 in Class, g1 in Group 
                  where g1 != 0 /\ g1 <= number_of_groups_in_class[c1],
                c2 in Class
                  where c1 < c2 /\ class_instructor[c1] != class_instructor[c2],
                g2 in Group
                  where g2 != 0 /\ g2 <= number_of_groups_in_class[c2])
            (bool2int(are_groups_have_students_in_common(c1, g1, c2, g2)));
% --------------------------------------------------