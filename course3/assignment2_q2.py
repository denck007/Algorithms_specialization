'''
Course 3 Week 2:Greedy Algorithms, Minimum Spanning Trees, and Dynamic Programming
Question 2: Clustering large dataset

We are given a large dataset with each node having 24 'values'.
The values are boolean.
We are tasked with finding the number of clusters needed so that the spacing between any 2 nodes
    in seperate clusters have at least 2 different 'values'

The dataset is large and it is advised to no try and measure the distance between all the points.


My idea to start is to do some simple filtering based on the known data:
- We want to know the number of clusters
- The minimum spacing between clusters is >=3

So if we sum the number of 1's at each node, then only compute the distance between the items
    that have a potential of being close by. To do this we make a hash table, where the keys are 
    the sum of 1's, and point to a list of nodes. We then perform the comparision of the 2 values.

The exhaustive search of every combination is 20,000,000,000 symmetric comparisions. 
Doing this filtering step will bring us down to 200,000*(24+(24choose2))=30,000,000 symmetric comparisions or 667x less work

'''

import os
import sys
sys.path.append("/home/neil/Algorithms_specialization")
from helpers.Heap import Heap
from helpers.UnionFind import UnionFind

import time


# useful tool to compute n choose r which will be used to allocate an array
#https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
import operator as op
from functools import reduce
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer//denom

class list_string(list):
    '''
    extend the list class with the ability to turn it into a string
        of just the elements
    Not elegent, but handy
    '''
    def __init__(self,*args):
        list.__init__(self,*args)
        self.string = None # allows caching of the result
    def stringify(self):
        if self.string is None:
            self.string = ""
            for idx in range(self.__len__()):
                self.string += str(self.__getitem__(idx))
        return self.string
    def __hash__(self):
        return hash(self.stringify())
    def __copy__(self):
        self.string = None
        self.stringify()


class HammingCluster():
    def __init__(self,fname,testing=False):
        '''
        Load the dataset and convert it to booleans
        '''
        self.fname = fname
        self.testing = testing

        self.keys_iter = 0
        self.union_iter = 0
        self.list_string_iter = 0

        with open(fname,'r') as f:
            data = f.readlines()
        self.num_nodes = int(data[0].strip().split()[0]) # number of nodes in the graph
        self.num_dims = int(data[0].strip().split()[1]) # number of dimensions the node has, number of values it has
        
        self.unionfind = UnionFind(self.num_nodes)

        self.data = {}
        for node,line in enumerate(data[1:]):
            vals = list_string(line.strip().split())

            if vals not in self.data:
                self.data[vals] = [node]
            else:
                self.data[vals].append(node)

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                self.correct_solution = int(f.read())


    def cluster(self):
        '''
        
        '''

        for key in self.data:
            self.keys_iter += 1
            if len(self.data[key]) != 1:
                u = self.data[key][0]
                for v in range(1,len(self.data[key])):
                    self.union_iter += 1
                    self.unionfind.union_if_unique(u,v)

        for key in self.data:
            self.keys_iter += 1
            # all verticies at same location are set to be children of the first vertex with that code
            u = self.data[key][0]
            for idx in range(self.num_dims):
                self.list_string_iter += 1
                u_value_new = list_string(key)
                if u_value_new[idx] == "0":
                    u_value_new[idx] = "1"
                else:
                    u_value_new[idx] = "0"
                if u_value_new in self.data:
                    v = self.data[u_value_new][0]
                    self.union_iter += 1
                    self.unionfind.union_if_unique(u,v)

        for key in self.data:
            self.keys_iter += 1
            u = self.data[key][0]
            for idx_1 in range(self.num_dims):
                self.list_string_iter += 1
                u_value_new_1 = list_string(key)
                if u_value_new_1[idx_1] == "0":
                    u_value_new_1[idx_1] = "1"
                else:
                    u_value_new_1[idx_1] = "0"

                for idx_2 in range(idx_1,self.num_dims):
                    self.list_string_iter += 1
                    u_value_new_2 = list_string(u_value_new_1)
                    if u_value_new_2[idx_2] == "0":
                        u_value_new_2[idx_2] = "1"
                    else:
                        u_value_new_2[idx_2] = "0"
                    if u_value_new_2 in self.data:
                        v = self.data[u_value_new_2][0]
                        self.union_iter += 1
                        self.unionfind.union_if_unique(u,v)
            
        return self.unionfind.num_groups

            
base_path = "course3/test_assignment2/question2"
#fname = "input_random_5_4_4.txt"
fname = "input_random_4_4_6.txt"
hc = HammingCluster(os.path.join(base_path,fname),testing=True)

num_groups = hc.cluster()
print("expected {:4} Got {:4} error {:4}".format(hc.correct_solution,num_groups,hc.correct_solution-num_groups))



with open("output.csv",'w') as f:
    f.write("n,dims,keys,union,list_string\n")

for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    count_end = fname.rfind("_")
    count_start = fname[:count_end].rfind("_")+1
    
    if int(fname[count_start:count_end]) > 1024:
        continue
    print("{}".format(fname),end="")
    start_time = time.time()
    hc = HammingCluster(os.path.join(base_path,fname),testing=True)
    num_groups = hc.cluster()
    if hc.correct_solution != num_groups:
        print("\n\tExpected {:4} Got {:4} error {:4}".format(hc.correct_solution,num_groups,hc.correct_solution-num_groups))
        print("\tElapsed time: {:.1f}sec".format(time.time()-start_time))
        print("\tn: {} keys: {} union: {} list_string:{}\n".format(hc.num_nodes,hc.keys_iter,hc.union_iter,hc.list_string_iter))
    else:
        print("  Correct!")

    with open("output.csv",'a') as f:
        f.write("{},{},{},{},{}\n".format(hc.num_nodes,hc.num_dims,hc.keys_iter,hc.union_iter,hc.list_string_iter))


base_path = "course3/"
fname = "assignment2_q2.txt"
print("Starting assignment")
start_time = time.time()
hc = HammingCluster(os.path.join(base_path,fname),testing=False)
num_groups = hc.cluster()
print("\tGot {:4}".format(num_groups))
print("\tElapsed time: {:.1f}sec".format(time.time()-start_time))


