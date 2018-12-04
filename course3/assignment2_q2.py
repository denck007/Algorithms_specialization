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


# useful tool to compute n choose r which will be used to allocate an array
#https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
import operator as op
from functools import reduce
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer//denom

class HammingCluster():
    def __init__(self,fname,testing=False):
        '''
        Load the dataset and convert it to booleans
        '''
        self.fname = fname
        self.testing = testing

        with open(fname,'r') as f:
            data = f.readlines()
        self.num_nodes = int(data[0].strip().split()[0]) # number of nodes in the graph
        self.num_dims = int(data[0].strip().split()[1]) # number of dimensions the node has, number of values it has
        self.data = []
        for line in data[1:]:
            vals = []
            for val in line.strip().split():
                if val == '1':
                    vals.append(True)
                else:
                    vals.append(False)
            self.data.append(vals)

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                self.correct_solution = int(f.read())

    def sum_dims_at_nodes(self):
        '''
        Go over all the nodes and sum up the number of 1's or Trues at each node
        Create a hashtable/dictionary of sum:[node_numbers]
        '''
        # initialize the hash table
        self.sums = {}
        for d in range(self.num_dims+1): # 0 and num_dims are both valid
            self.sums[d] = []

        for idx,node in enumerate(self.data):
            s = sum(node)
            self.sums[s].append(idx)
    @profile
    def cluster(self,min_distance):
        '''
        Create clusters of nodes with a minimum distance between 2 nodes in seperate clusters
        '''

        # create a heap for the distances
        # first estimate max possible heap size
        # this computes n choose r for each set of differences
        heap_size = 1
        for ii in range(min_distance+1):
            heap_size += ncr(self.num_dims,ii)
        heap_size *= self.num_nodes
        
        self.heap = Heap(heap_size)

        # need a way to link the id that is passed to the heap to the pair of matches
        self.heap_to_matches = [] # list of lists that contain the u,v node ids
        match_id = 0

        for sum_start in self.sums:
            if self.sums[sum_start] == []: # skip empty counts
                continue
            for sum_end in range(sum_start,min(self.num_dims+1,sum_start+min_distance+1)):
                if self.sums[sum_end] == []: # skip empty counts
                    continue
                # now have the starting nodes with same sum and end nodes within min_distance of the starting node
                for u in self.sums[sum_start]:
                    for v in self.sums[sum_end]:
                        if u == v: # skip itself
                            continue

                        #distance1 = 0
                        #for idx in range(self.num_dims):
                        #    if self.data[u][idx] == self.data[v][idx]:
                        #        distance1 += 1
                        # this method works but is expensive!
                        distance = sum([abs(x-y) for x,y in zip(self.data[u],self.data[v]) ])
                        assert distance == distance
                        
                        if distance <= min_distance:
                            self.heap.insert(match_id,distance)
                            self.heap_to_matches.append([u,v])
                            match_id += 1

        # create the union find data structure
        self.unionfind = UnionFind(self.num_nodes)

        id,distance = self.heap.extract_min()
        while len(self.heap) > 0:
            ##if len(self.heap)%100==0:
            #    print("\tOn {}/{}\r".format(match_id-len(self.heap),len(self.heap)),end="")
            self.unionfind.union_if_unique(self.heap_to_matches[id][0],self.heap_to_matches[id][1])
            id,distance = self.heap.extract_min()
        #print()

        # must account for when the last 2 values are in the same cluster
        if self.unionfind.same_parents(self.heap_to_matches[id][0],self.heap_to_matches[id][1]):
            self.unionfind.num_groups += 1
        self.unionfind.num_groups -= 1
        return self.unionfind.num_groups
            
base_path = "course3/test_assignment2/question2"
#fname = "input_random_1_4_14.txt"
fname = "input_random_52_1024_24.txt"
hc = HammingCluster(os.path.join(base_path,fname),testing=True)
hc.sum_dims_at_nodes()
num_groups = hc.cluster(min_distance=2)
print("expected {:4} Got {:4} error {:4}".format(hc.correct_solution,num_groups,hc.correct_solution-num_groups))


for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    count_end = fname.rfind("_")
    count_start = fname[:count_end].rfind("_")+1
    
    if int(fname[count_start:count_end]) > 1500:
        continue
    print(fname)
    hc = HammingCluster(os.path.join(base_path,fname),testing=True)
    hc.sum_dims_at_nodes()
    num_groups = hc.cluster(min_distance=2)
    print("\tExpected {:4} Got {:4} error {:4}".format(hc.correct_solution,num_groups,hc.correct_solution-num_groups))