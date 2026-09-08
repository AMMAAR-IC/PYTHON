cet = ["ammaar", "ayaan", "aiman"]
neet = ["ammaar", "yahiya", "ali"]
jee = ["ammaar", "aiman", "bruce"]

def list_intersection(list1, list2):
    return [student for student in list1 if student in list2]

def list_intersection_three(list1, list2, list3):
    return [student for student in list1 if student in list2 and student in list3]

def unique_students(*lists):
    all_students = []
    for lst in lists:
        all_students.extend(lst)
    return list(set(all_students))  # Remove duplicates by converting to set and back to list

print(f"The people that attempt CET and JEE both are : {list_intersection(cet, jee)}")
print(f"The people that attempt CET and NEET both are : {list_intersection(cet, neet)}")
print(f"The people that attempt NEET and JEE both are : {list_intersection(neet, jee)}")
print(f"The people that attempt CET, NEET and JEE all are : {list_intersection_three(cet, neet, jee)}")
print(f"The total number of unique students are : {len(unique_students(cet, neet, jee))}")
