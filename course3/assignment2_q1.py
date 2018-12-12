'''
Course 3 Week 2:Greedy Algorithms, Minimum Spanning Trees, and Dynamic Programming
Question 1: Clustering using Kruskal's Algorithm 

Given a graph, cluster the items in to 4 clusters. What is the maximum spacing of a 4 cluster?

There is 1 edge (i,j) for each choice of 1 <= i <= j <= n

Input is of the form:
[number of nodes]
[edge 1 node 1] [edge1 node 2] [edge 1 cost]
[edge 2 node 1] [edge2 node 2] [edge 2 cost]
'''
import os
import sys
sys.path.append("/home/neil/Algorithms_specialization")
from helpers.Heap import Heap
from helpers.UnionFind import UnionFind

class Graph():
    '''
    Graph structure
    '''
    def __init__(self,fname,testing=True):
        '''
        Read in the file in fname and create the graph
        if testing then also read in the correct solution by swapping in 'output' for 'input' in fname
        '''

        with open(fname,'r') as f:
            data = f.readlines()
        
        self.num_verticies = int(data[0].strip())
        self.num_edges = 0
        self.edge_verticies = [[] for e in range(len(data))]
        self.vertex_edges = [[] for v in range(self.num_verticies+1)]
        self.costs = []
        
        edge_id = -1
        for line in data[1:]:
            edge_id += 1
            u,v,cost = line.strip().split()
            u = int(u)
            v = int(v)
            cost = int(cost)

            self.edge_verticies[edge_id] = [u,v]
            self.vertex_edges[u].append(edge_id)
            self.vertex_edges[v].append(edge_id)
            self.costs.append(cost)
        self.num_edges = edge_id

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                self.solution = int(f.read())

class Kruskal():
    '''
    Run Kruskal's Minimum Spanning Tree algorithm with early stopping to do clustering

    '''
    def __init__(self,fname,num_clusters,testing=False):
        '''
        initialize the algorithm by:
            loading the data
            creating graph, heap, and union find data structures
        '''
        self.fname = fname
        self.num_clusters=num_clusters
        self.testing = testing
        self.g = Graph(fname,testing=testing)
        self.h = Heap(self.g.num_edges)
        self.uf = UnionFind(self.g.num_verticies)

        if testing:
            self.ground_truth = self.g.solution

    def __call__(self):
        '''
        When the object is called run the clustering algorithm
        Returns the max spacing between clusters
        '''        
        for edge in range(len(self.g.costs)):
            self.h.insert(edge,self.g.costs[edge])

        iteration = -1
        while self.uf.num_groups > self.num_clusters:
            iteration += 1
            #print("iteration {}".format(iteration))
            edge,cost = self.h.extract_min()
            u,v = self.g.edge_verticies[edge]
            #print("\t u,v,c: {} {} {}".format(u,v,cost))
            self.uf.union_if_unique(u,v)
            _ = 1
            
        # want the max distances between clusters, so need to find the next largest
        #   distance for edges not in same cluster
        edge,cost = self.h.extract_min()
        u,v = self.g.edge_verticies[edge]
        while self.uf.same_parents(u,v):
            edge,cost = self.h.extract_min()
            u,v = self.g.edge_verticies[edge]
        
        self.max_spacing = cost
        return self.max_spacing

    def evaluate_solution(self):
        '''
        If object is flagged as testing, then compare the computed solution to the ground truth
        '''
        if self.testing:
            if self.max_spacing == self.ground_truth:
                print("{} correct: {}".format(self.fname,self.ground_truth))
            else:
                print("Incorrect solution for {}\n\tGot {} Expected {}".format(self.fname,self.max_spacing,self.ground_truth))
        else:
            print("Predicted solution: {}".format(self.max_spacing))

base_path = "course3/test_assignment2/question1"
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    kruskal = Kruskal(os.path.join(base_path,fname),num_clusters=4,testing=True)
    solution = kruskal()
    kruskal.evaluate_solution()

print("Staring final problem:")
base_path = "course3/"
fname = "assignment2_q1.txt"

kruskal = Kruskal(os.path.join(base_path,fname),num_clusters=4,testing=False)
solution = kruskal()
kruskal.evaluate_solution()


    
    







