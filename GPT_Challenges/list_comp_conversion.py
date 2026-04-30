## Convert the following to a list comprehension
"""result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x * 2)
        
    output = [0, 4, 8, 12, 16]"""
         
result = [x * 2 for x in range(10) if x % 2 == 0 ]
# x*2 is the value we want to append, the EXPRESSION
# the standard for loop ITERATION follows, then the condition or FILTER
# this is all then saved into a new list and printed 
print(result)

