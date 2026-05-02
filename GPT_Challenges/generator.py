"""In this challenge write a function that returns non-empty lines in a file, but YIELDS them instead of RETURN. 

Requirements: yield one non-empty line at a time, strip whitespace before yielding"""

def read_non_empty_lines(filename:str):
    with open(filename, 'r') as file: 
        for line in file:
            if line.strip():
                yield line.strip()


for i in read_non_empty_lines("test_file.txt"):
    print(i)
#print(read_non_empty_lines("test_file.txt"))


"""---Small Improvements---
-> Logic and code is correct. 
--> introduce error handling for new challenges as a practice. """