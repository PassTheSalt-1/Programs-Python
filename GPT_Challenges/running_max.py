"""Write a script that: 
Return the maximum sum of any contiguous subarray of size k
Must run in O(n) time
❌ No nested loops
❌ No recomputing sums from scratch

"""

nums = [1,5,7,33,8,10,5,7,9,4]
                    ##list          ## 3
def max_subarray_sum(num_list: list, k:int) -> int:
    total_sum = sum(num_list[:k]) # total of slice of numlist 0->3 
    max_sum = total_sum # save into max sum 
        #num    range of 10 - 3 = 7 starting at first 4 non inclusive would be 1,5,7,33 = 13
    for i in range(len(num_list) - k):
        total_sum = total_sum - num_list[i] + num_list[i+k] # using i as the index to scan the array 
        #scan array using window and calculate next window. subtract 1 and add 33.
        max_sum = max(max_sum, total_sum)
        #compare the initial window with our running tab window to store the max between them both,
        
    return max_sum

print(max_subarray_sum(nums, 3))


"""CORE PRINCIPLE HERE
initialize the first window of 3 values

using the range and the length of the list as the counter. Increment through the list. 

add the new element
removing the old one

max() will compare and retain the max value within any window of 3 values. 

This creates the sliding window and achieves the O(n) time. """
