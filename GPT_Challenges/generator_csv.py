"""Challenge will combine generators + parsing. 

Requirements: Write a generator that YIELDS tuples (name,age), skips empy lines, and converts age to type INT.

Must use .split(",")
Must use yield
Must handle whitespace
"""

def process_people_file(filename:str) -> tuple:

    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    line = line.strip() ## Handle formatting first, strip off whitespace while a list
                    split_line = line.split(",") ## Split up values in line, name and age. 
                    split_line[1] = int(split_line[1]) ## convert age to type INT
                    yield tuple(split_line) ## finally convert to tuple and yield
    except FileNotFoundError:
        return "File not found!"


for i in process_people_file("test_csv.csv"): ## run through processed values 
    
    print(i)
    print(type(i[0])) ## Print our new tuples, plus type check to confirm age == INT
    print(type(i[1]))

"""--- Improvements---
-> Instead of using indexing, use tuple unpacking like so:
    name, age = line.split(",") this is simultaneously split the line and assign each value to a variable

-> Instead of explicitly stating tuple, simply put the proposed values into parentheses like so: 
    yield (name, int(age)) -> this will just create the tuple. 

-> good habit to strip values when they are returned/yielded.

-> Since this is a generator, we are not actually returning a tuple so the return type hint can be removed.
"""
