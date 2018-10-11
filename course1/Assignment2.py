'''
Algorithms Divide and Conquer
Week 2
Programming assignment 1

Given a txt file with a list of numbers (1 per line) that are non repeating integers,
find the number of inversions in the list

Implement the divide and conquer method covered in the week 2 lectures
Create test cases for smaller inputs
'''
import math
import time

def get_inputs(fname):
    '''
    take in a file name and return the list of numbers as an array
    '''
    with open(fname,'r') as f:
        data = f.readlines()
    data = [int(x[:-1]) for x in data if x != "\n"]
    return data

def count_split_inversions(left,right):
    '''
    given 2 lists of sorted integers, sort 
    '''
    nl = len(left)
    nr = len(right)
    n = nl + nr
    ii = 0
    jj = 0
    inversions = 0
    output = [0]*n
    for k in range(n):
        if left[ii] < right[jj]:
            output[k] = left[ii]
            ii += 1
        else:
            output[k] = right[jj]
            jj += 1
            inversions += nl-ii

        if ii == nl:
            output[k+1:] = right[jj:]
            break
        elif jj == nr:
            output[k+1:] = left[ii:]
            break
    return (output,inversions)

def count_inversions(arr):
    n = len(arr)
    if n == 1:
        return (arr,0)
    elif n == 2: # base case
        # sort the 2 values
        if arr[0] > arr[1]: 
            return ([arr[1],arr[0]],1)
        else:
            return (arr,0)
    else:
        half = math.floor(n/2)

        left, left_inversions = count_inversions(arr[:half])
        right, right_inversions = count_inversions(arr[half:])
        merged, split_inversions = count_split_inversions(left,right)
    inversions = left_inversions + right_inversions + split_inversions
    return (merged,inversions)

# test left split
input = [1,0,2,3]
sorted_true = [0,1,2,3]
inversion_true = 1
s,inversions = count_inversions(input)
assert sorted_true == s,'Left split failed to sort:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,s,sorted_true)
assert inversion_true == inversions,'Left split failed to count inversions:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,inversions,inversion_true)
print("Completed test left split")

# test right split
input = [0,1,3,2]
sorted_true = [0,1,2,3]
inversion_true = 1
s,inversions = count_inversions(input)
assert sorted_true == s,'Left split failed to sort:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,s,sorted_true)
assert inversion_true == inversions,'Left split failed to count inversions:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,inversions,inversion_true)
print("Completed test right split")

# test split 1
input = [0,2,1,3]
sorted_true = [0,1,2,3]
inversion_true = 1
s,inversions = count_inversions(input)
assert sorted_true == s,'Left split failed to sort:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,s,sorted_true)
assert inversion_true == inversions,'Split failed to count inversions:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,inversions,inversion_true)
print("Completed test split 1")

# test split 2
input = [0,1,3,2,4,5]
sorted_true = [0,1,2,3,4,5]
inversion_true = 1
s,inversions = count_inversions(input)
assert sorted_true == s,'Left split failed to sort:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,s,sorted_true)
assert inversion_true == inversions,'Left split failed to count inversions:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,inversions,inversion_true)
print("Completed test split 2")

# test split 3
input = [1,3,5,2,4,6]
sorted_true = [1,2,3,4,5,6]
inversion_true = 3
s,inversions = count_inversions(input)
assert sorted_true == s,'Left split failed to sort:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,s,sorted_true)
assert inversion_true == inversions,'Left split failed to count inversions:\n\tInput: {}\n\tOutput: {}\n\tTruth: {}'.format(input,inversions,inversion_true)
print("Completed test split 3")

case_name = "TEST CASE - 1 Jeffrey Skonhovd"
input = [1,3,5,2,4,6]
inversion_true = 3
s,inversions = count_inversions(input)
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

case_name = "TEST CASE - 2 Jeffrey Skonhovd"
input = [1,5,3,2,4]
inversion_true = 4
s,inversions = count_inversions(input)
print("{} Output: {} Truth: {}".format(case_name,inversions,inversion_true))
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

case_name = "TEST CASE - 3 Jeffrey Skonhovd"
input = [5,4,3,2,1]
inversion_true = 10
s,inversions = count_inversions(input)
print("{} Output: {} Truth: {}".format(case_name,inversions,inversion_true))
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

case_name = "TEST CASE - 4 Jeffrey Skonhovd"
input = [1,6,3,2,4,5]
inversion_true = 5
s,inversions = count_inversions(input)
print("{} Output: {} Truth: {}".format(case_name,inversions,inversion_true))
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

case_name = "Test Case - #1 - 15 numbers soesilo w"
input = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0]
inversion_true = 56
s,inversions = count_inversions(input)
print("{} Output: {} Truth: {}".format(case_name,inversions,inversion_true))
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

case_name = "Test Case 2 - 50 numbers soesilo w"
input = [37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6, 33, 43, 26, 40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19, 0, 32, 46, 27, 31, 25, 15, 36, 20, 8, 9, 49, 22, 23, 30, 45 ]
inversion_true = 590
s,inversions = count_inversions(input)
print("{} Output: {} Truth: {}".format(case_name,inversions,inversion_true))
assert inversion_true == inversions,'Failed on {}\n\tOutput: {}\n\tTruth: {}'.format(case_name,inversions,inversion_true)

start_time = time.time()

print("Starting final result...")
input = get_inputs("part1/assignment2_inputs.txt")
post_read = time.time()
s, inversions = count_inversions(input)
end_time = time.time()
print("Took {:.3e} total, {:.3e} to read and {:.3e} to compute".format(end_time-start_time,post_read-start_time,end_time-post_read))
print("Inversions: {}".format(inversions))
    