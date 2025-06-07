cet = {"ammaar", "ayaan", "aiman"}
neet = {"ammaar", "yahiya", "ali"}
jee = {"ammaar", "aiman", "bruce"}

def cmp2(set1, set2):
    return set1.intersection(set2)

def cmp3(set1, set2, set3):
    return set1.intersection(set2, set3)

print(f"The total people that attempt CET and JEE both are : {cmp2(cet, jee)}")
print(f"The total people that attempt CET and NEET both are : {cmp2(cet, neet)}")
print(f"The total people that attempt NEET and JEE both are : {cmp2(neet, jee)}")
print(f"The total people that attempt CET, NEET and JEE all are : {cmp3(cet, neet, jee)}")
print(f"The total number of unique students are : {len(jee.union(cet, neet))}")
