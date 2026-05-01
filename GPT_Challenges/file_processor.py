"""Task is: write a function that opens a file, counts the NON-empty lines, and returns that count.

Constraints: no .readlines()"""


def count_file_lines(filename:str) -> int:
    non_empty = 0 
    ## initialize counter for accumulation
    try:
        with open(filename, 'r') as file:  ## open file in readmode 
            ##lines = [line.split() for line in file if line]  ## split each line in a new list entry in the lines list


            # for line in lines:                 
            #     if len(line) > 0:           OLD
            
            for line in file:
                ##IMPROVMENT -> simply take each line 
                if line.strip():       # -> conditional to see if the stripped line containts actual content.
                    non_empty += 1 

            return non_empty
    except FileNotFoundError:  
        ## basic error handling for if file does not exist
        return "File not found."

result=count_file_lines("test_file.txt") 
## return the new list and run function on text file.
print(result)

"""---Improvements to be made---"""

# if line in this context is only checking if the line is NOT NONE, but will still show lines like "\n" or newlines.

# Dont need to actually split the line, just need to check for whitespace.

