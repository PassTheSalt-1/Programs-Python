"""
Take input, which is a list of tuples as shown below and return the sum of only the first elements. 
[(1,2), (3,4), (5,6)] → 9"""

tuple_list = [(1,2), (3,4), (5,6)]

def sum_first_tuple_num(pairs:list): 
    """Takes tuple list, unpacks to access first item and then sums together"""
    first_elements = 0
    # for pair in pairs:
    #     first_elements += pair[0] ## incorrect for challenge, must use UNPACKING not INDEXING

    for first, second in pairs: ## This splits the tuple and allows us to access it without having to use indexing.
        first_elements += first ## Accumulate values as we loop 
        
    return first_elements   ## return total



result = sum_first_tuple_num(tuple_list)
print(result)

