'''
Course 3, Week3: Huffman codes and Intro to Dynamic Programming, Assignment 3: Q3
Maximum Weight independent set of a path graph

This assignment is an introduction to dynamic programming.

Given a listing of weights for each verticie, find the maximum independed set.
This means that no adjacent verticies can be in the set.

The output is a binary string indicating if some specific verticies are in the set:
    1,2,3,4,17,117,517,997
    Note that the solution is 1 indexed not 0 indexed

'''

import os

class MaxWeightIndependentSet():
    '''
    Defines the max weight for an independent set of a path graph
    '''

    def __init__(self,fname,testing=False):
        '''
        read in the input and optional solution data (if testing)
        '''

        self.fname = fname
        self.testing = testing
        self.to_find = [1, 2, 3, 4, 17, 117, 517, 997] # the nodes we are looking to see if they are in the graph

        with open(fname,'r') as f:
            data = f.readlines()

        self.num_vertex = int(data[0])
        data[0] = 0 # pad the front with 0 to handle 1 based indexing
        self.weights = [int(x) for x in data]

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                data = f.readlines()

            self.solution = data[0].strip()


base_path = "course3/test_assignment3/question3"
fname = "input_random_1_10.txt"

wis = MaxWeightIndependentSet(os.path.join(base_path,fname),testing=True)
print(wis.weights)
print(wis.solution)

'''
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    print(fname,end="")
    if (min_len == huffman.solution_2) and (max_len == huffman.solution_1):
        print(" Correct! Min: {} Max: {}".format(min_len,max_len))
    else:
        print("\n\tMin Got {} expected {}\n\tMax got {} expected {}".format(min_len,huffman.solution_2,max_len,huffman.solution_1))

'''



