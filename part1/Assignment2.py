'''
Algorithms Divide and Conquer
Week 2
Programming assignment 1

Given a txt file with a list of numbers (1 per line) that are non repeating integers,
find the number of inversions in the list

Implement the divide and conquer method covered in the week 2 lectures
Create test cases for smaller inputs


TODO:
[X] Read in file
[ ] Count left/right inversions
[ ] Count split inversion
'''

def get_inputs(fname):
    '''
    take in a file name and return the list of numbers as an array
    '''
    with open(fname,'r') as f:
        data = f.readlines()
    data = [int(x[:-1]) for x in data]
    return data

print(get_inputs("part1/assignment2_test_inputs1.txt"))

def count_split_inversions(left,right):
    '''
    given 2 lists of sorted integers, sort 
    '''

def count_inversions(arr):
    n = len(arr)
    if n == 2:
        if arr[0] > arr[1]:
            return ([arr[1],arr[0]],1)
        else:
            return (arr,0)
    else:
        left, left_inversions = count_inversions(arr[:n//2])
        right, right_inversions = count_inversions(arr[n//2:])
        split_inversions = count_split_inversions(left,right)
    return left_inversions + right_inversions + split_inversions
        
    