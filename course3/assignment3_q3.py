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

    def generate_wis_costs(self):
        '''
        Go through the path graph and generate the weight independent set
        '''

        self.costs = [0 for x in range(self.num_vertex+1)]

        # initialize the base cases
        self.costs[0] = 0
        self.costs[1] = self.weights[1]

        for ii in range(2,self.num_vertex+1):
            self.costs[ii] = max(self.costs[ii-1],self.costs[ii-2]+self.weights[ii])

    def get_wis_set(self):
        '''
        get the indicies in the maximum weight independent set 
        '''

        self.set = [False for _ in range(self.num_vertex+1)]
        ii = self.num_vertex
        while ii > 0:
            if self.costs[ii-1] >= (self.costs[ii-2] + self.weights[ii]):
                ii -= 1
            else:
                self.set[ii] = True
                ii -= 2

    def get_result(self):
        '''
        Get the string that signifies the solution to the homework assignment
        '''

        answer = ""

        for idx in self.to_find:
            if idx > self.num_vertex:
                answer += "0"
            elif self.set[idx]:
                answer += "1"
            else:
                answer += "0"
        return answer


base_path = "course3/test_assignment3/question3"
fname = "input_random_1_10.txt"

wis = MaxWeightIndependentSet(os.path.join(base_path,fname),testing=True)
wis.generate_wis_costs()
wis.get_wis_set()
solution = wis.get_result()
print("Got {} expected {}".format(solution,wis.solution))

for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    print(fname,end="")
    wis = MaxWeightIndependentSet(os.path.join(base_path,fname),testing=True)
    wis.generate_wis_costs()
    wis.get_wis_set()
    solution = wis.get_result()
    if wis.solution == solution:
        print(" Correct! Got {}".format(solution))
    else:
        print("\n\tGot {} expected {}".format(solution,wis.solution))

base_path = "course3/"
fname = "assignment3_q3_input.txt"
print("Starting assignment...")
wis = MaxWeightIndependentSet(os.path.join(base_path,fname),testing=False)
wis.generate_wis_costs()
wis.get_wis_set()
solution = wis.get_result()
print("Got {}".format(solution))
