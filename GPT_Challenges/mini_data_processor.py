

## Given a list of integers, return adictionaru with list of EVENS, ODDS, and SUM.

ints = [1,2,3,6,7,10,14,5,9,11,21,55,62,31]

def even_odds_and_sum(int_list:list) -> dict: 
    """Takes in a list of integers. Identifies even and odd integers presents and puts them into a respective dictionary key/value entry, returns as sorted dictionary"""

    sorted_int_dict = {
        "evens": [],
        "odds": [],
        "sum": 0
    } ## Create new dictionary, and new keys/list values we want to populate

    for num in int_list:
        sorted_int_dict["sum"] += num ## accumulate the nums into the sum value
        if num % 2 == 0:
            sorted_int_dict["evens"].append(num) ## if even append the number
        else:
            sorted_int_dict["odds"].append(num) ## if odd append the number

    return sorted_int_dict ## return the new dictionary


result = even_odds_and_sum(ints)
print(result) ## run function and print the result



"""improvments noted
-> function naming convention doesn't need to be super specific. shorter and more general pupose"""