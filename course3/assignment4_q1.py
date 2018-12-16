'''
Course 3, Week4: Advanced dynamic programming: the knapsack problem, sequence alignment, and optimal binary search trees

There are 2 problems in this assignment, both are solving the knapsack problem.
The first one is the simple naive method where we store all the data we generate.
The second is too large to save all the data and solving every sub problem is infeasible.

Input is:
[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...
For example, the third line of the file is "50074 834558", indicating that the second item has value 50074 and size 834558, respectively.You should assume that item weights and the knapsack capacity are integers.

Output:
The output of the algorithm is the value of the optimal solution

First going to code up the naive method, then the more more advanced method

'''

import os
import sys
import time
sys.setrecursionlimit(3000)

class Knapsack():
    '''
    Class defining a knapsack
    '''
    def __init__(self,fname,testing=False):
        '''
        Read in the input from fname and the solution if testing
        '''

        self.fname = fname
        self.testing = testing

        self.fname_short = fname[fname.rfind("/")+1:] # used for printing out status

        with open(fname,'r') as f:
            data = f.readlines()
        
        self.knapsack_size = int(data[0].split()[0])
        self.num_items = int(data[0].split()[1])

        self.values = [0]
        self.weights = [0]
        self.max_weight = 0
        for item in data[1:]:
            value,weight = item.strip().split()
            self.values.append(int(value))
            self.weights.append(int(weight))
            self.max_weight = max(self.max_weight,int(weight))

        if self.testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                self.solution = int(f.readline())

        self.compute_count = 0 # track how many unique solutions we compute
        self.possible_compute = self.num_items * self.knapsack_size # the number of unique values if we had to do all the computations the naive way

    def naive_solution(self):
        '''
        Find and return the optimal total value of items that can fit in the knapsack.
        Use the naive method filling out the 2d array 
        '''

        self.A = [[0 for ii in range(self.num_items+1)] for x in range(self.knapsack_size+1)]

        for ii in range(1,self.num_items+1):
            for x in range(self.knapsack_size+1):
                value1 = self.A[x][ii-1] # skip item ii
                if self.weights[ii] <= x:
                    if x-self.weights[ii] >=0:
                        value2 = self.A[x-self.weights[ii]][ii-1]+self.values[ii]
                    else:
                        print("Overflow")
                else:
                    value2 = 0
                self.A[x][ii] = max(value1,value2)
        
        return max(self.A[-1])

    def fast_solution(self):
        '''
        Use a hash table to only compute the items we actually need
        By definition the optimal value is stored at A[knapsack size,num_items]
        So only compute values that contribute to that value

        '''
        self.start_time = time.time()
        self.A_hash = {} # store hashed values using (x,ii) tuple as keys

        self.prediction = self.find(self.knapsack_size,self.num_items)

        return self.prediction

    def find(self,x,ii):
        '''
        Lookup the value at x,ii in A_hash
        Recursive compute if needed
        '''

        if ii <= 0: # stop from falling off of table
            return 0
        if (x,ii) in self.A_hash: # if we already computed it just return it
            return self.A_hash[(x,ii)]
        
        value1 = self.find(x,ii-1)
        if self.weights[ii] <= x:
            value2 = self.find(x-self.weights[ii],ii-1) + self.values[ii]
        else:
            value2 = 0
        
        value = max(value1,value2)
        self.A_hash[(x,ii)] = value # cache it
        
        self.compute_count += 1
        if self.compute_count%10000 == 0:
            elapsed = time.time() - self.start_time
            remaining = elapsed/self.compute_count*(self.possible_compute-self.compute_count)
            print("\r{} {}/{} less than {:.2f} seconds remaining".format(self.fname_short,self.compute_count,self.possible_compute,remaining),end="")

        return value


base_path = "course3/test_assignment4"
print("Using naive solution...")
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    knapsack = Knapsack(os.path.join(base_path,fname),testing=True)
    if knapsack.num_items > 1000: # skip large inputs in naive solution
        continue

    print(fname,end="")
    prediction = knapsack.naive_solution()
    if prediction == knapsack.solution:
        print(" Correct, optimal value is {}".format(prediction))
    else:
        print("\n\tExpected {} Got {}".format(knapsack.solution,prediction))


print("\n\nTesting fast version...")
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    knapsack = Knapsack(os.path.join(base_path,fname),testing=True)
    if knapsack.num_items > 100: # skip large inputs in naive solution
        continue

    print(fname,end="")
    prediction = knapsack.fast_solution()
    if prediction == knapsack.solution:
        print("\n\tCorrect, optimal value is {}".format(prediction))
    else:
        print("\n\tExpected {} Got {}".format(knapsack.solution,prediction))
    
    speedup = knapsack.possible_compute/knapsack.compute_count
    print("\tDid {} computations out of {} possible, {:.2f}x speedup".format(knapsack.compute_count,knapsack.possible_compute,speedup))
    print("\tTotal elapsed time: {:.2f}".format(time.time()-knapsack.start_time))


base_path = "course3"
fname = "assignment4_q1_input.txt"
knapsack = Knapsack(os.path.join(base_path,fname),testing=False)
prediction = knapsack.fast_solution()
print("\n\nQuestion 1 solution: {}".format(prediction))
speedup = knapsack.possible_compute/knapsack.compute_count
print("\tDid {} computations out of {} possible, {:.2f}x speedup".format(knapsack.compute_count,knapsack.possible_compute,speedup))
print("\tTotal elapsed time: {:.2f}".format(time.time()-knapsack.start_time))

fname = "assignment4_q2_input.txt"
knapsack = Knapsack(os.path.join(base_path,fname),testing=False)
prediction = knapsack.fast_solution()
print("\n\nQuestion 2 solution: {}".format(prediction))
speedup = knapsack.possible_compute/knapsack.compute_count
print("\tDid {} computations out of {} possible, {:.2f}x speedup".format(knapsack.compute_count,knapsack.possible_compute,speedup))
print("\tTotal elapsed time: {:.2f}".format(time.time()-knapsack.start_time))