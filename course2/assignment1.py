'''
Graph Search, Shortest Paths, and Data Structures
Week 1 Assignment: Sizes of Strongly Connected Components (SCC)

In this assignment we are going to implement an alogorith to calculate the sizes of the 5 largest SCCs in a directed graph. The assignment input is quite large so memory management may be important

The input file is a listing of directed edges. The first column is the node the edge is leaving, and the second column is the node the edge is pointing to.


'''

import os
import sys
import threading
sys.setrecursionlimit(800000)
threading.stack_size(67108864)

class Graph():
    '''
    graph primitive to read in data structres from text files, support simple operations on graphs
    '''

    def __init__(self,fname,testing=False):
        '''
        create a graph from an edge listing filename
        testing is boolean that specifies weither to look for a ground truth file
        '''
        assert os.path.isfile(fname),"File {} does not exist!".format(fname)

        self.edge_verticies = {}
        self.num_nodes = 0
        self.num_edges = 0
        with open(fname,"r") as f:
            for jj,line in enumerate(f.readlines()):
                edge = [int(x) for x in line.strip("\n").split()]
                self.edge_verticies.update({jj:edge})
                self.num_edges += 1
                self.num_nodes = max([self.num_nodes,edge[0],edge[1]])
        self.build_vert_edges()

        if testing:
            with open(fname.replace("input","output"),'r') as f:
                groundtruth = f.readlines()
            self.groundtruth = [int(x) for x in groundtruth[0].split(",")]
    #@profile
    def build_vert_edges(self):
        '''
        Build the vert_edges dictionary from the edge_verticies dictionary
        '''    
        self.vert_edges = {}
        self.vertex_exist = [False for x in range(self.num_nodes+1)]
        for jj in self.edge_verticies.keys():
            node0 = self.edge_verticies[jj][0]
            if node0 is None:
                continue

            if self.vertex_exist[node0]:
                self.vert_edges[node0].append(jj)
            else:
                self.vert_edges.update({node0:[jj]})
                self.vertex_exist[node0] = True

    def reverse_edges(self):
        '''
        reverse all of the edges in the graph
        Note that we are not going to save the original ordering, as we can just call this again to get the original graph
        '''

        for edge in self.edge_verticies.keys():
            self.edge_verticies[edge] = self.edge_verticies[edge][::-1]
        self.build_vert_edges()

    def renumber_nodes(self,new_numbers):
        '''
        renumber the nodes in the graph with the list passed in as new_numbers
        new_numbers is a list where the value at each index is the new node number
        ie: if [2,1,0] is passed in, the node with the original idx of 0, will now be number 2

        note that not all nodes in the new_numbers list have to exist
        '''

        for jj in self.edge_verticies.keys():
            self.edge_verticies[jj][0] = new_numbers[self.edge_verticies[jj][0]]
            self.edge_verticies[jj][1] = new_numbers[self.edge_verticies[jj][1]]
        
        self.build_vert_edges() # recreate the verticies to edges list


class DFS():
    '''
    Depth first search algorith 
    '''
    def __init__(self,graph):
        '''
        initialize the DFS with the graph
        '''
        self.G = graph

        # need something to track if we have explored a paricitular node in a graph yet
        self.explored_node = [False for x in range(self.G.num_nodes+1)] # +1 is for 1 based indexing if used
        self.finishing_time = [None for x in range(self.G.num_nodes+1)] # finishing time for each node, for first pass of SCC
        self.leaders = [None for x in range(self.G.num_nodes+1)] # the leader for each node, for second pass of SCC
    #@profile
    def loop(self):
        self.t = 0 # 'global', number of nodes processed so far, is finishing time for the 1st pass of
        self.s = None # 'global', current source node, leader number in 2nd pass
        for ii in range(self.G.num_nodes,0,-1):
            if not self.explored_node[ii]:
                self.s = ii
                self.DFS(ii)
    #@profile
    def DFS(self,ii):
        '''
        run DFS on graph G starting at node ii
        '''
        self.explored_node[ii] = True
        self.leaders[ii] = self.s

        if not self.G.vertex_exist[ii]:
            return 

        for jj in self.G.vert_edges[ii]:
            end_node = self.G.edge_verticies[jj][1] # end node of edge
            if not self.explored_node[end_node]:
                self.DFS(end_node)

        self.t += 1
        self.finishing_time[ii] = self.t

    def calculate_leader_sizes(self):
        '''
        go over the leader list and count the number of nodes that each leader has
        '''
        self.leader_sizes = {}
        for ii in self.leaders:
            if ii in self.leader_sizes.keys():
                self.leader_sizes[ii] += 1
            elif ii is None:
                continue
            else:
                self.leader_sizes.update({ii:1})
        # if nodes do not have any edges this algorith will tag the node with itself as a leader, and no other items have that same leader
        keys = list(self.leader_sizes.keys())
        for ii in keys:
            if self.leader_sizes[ii] == 1 and self.leaders[ii] == ii:
                self.leader_sizes.pop(ii)

    def get_k_largest_leaders(self,k):
        '''
        get the number of nodes that share the the k most common leaders
        '''
        self.calculate_leader_sizes()
        sorted_values = sorted(self.leader_sizes.items(),key=lambda kv:kv[1],reverse=True)
        k_largest_leaders = [0 for x in range(k)]
        for x in range(k):
            if x >= len(sorted_values):
                break


            if sorted_values[x][0] is None:
                k_largest_leaders[x] = 0
            else:
                k_largest_leaders[x] = sorted_values[x][1]

        return k_largest_leaders

class SCC_sizes():
    '''
    Calculate the sizes of the k largest SCC groups in a graph
    '''
    def __init__(self,graph,k=5):
        '''
        Initialize the object instance
        graph is an instance of a Graph object
        k is the number of largest SCCs to report the size of
        '''
        self.G = graph
        self.k = k

    def run(self):
        '''
        Run the DFS algorithm on the graph to find the sizes of the k largest SCCs

        Step1:
            * reverse the graph
            * run DFS loop on the reveresed graph to get the ideal ordering
        Step2: 
            * Update the graph node numbering, remembering the original ordering
        Step3:
            * run DFS loop on the forward graph with new numbering
            * Get the leader numbers for each node
            * Calculate the size of each of the leader groups
        '''
        # Step 1:
        self.G.reverse_edges()
        pass1 = DFS(self.G)
        pass1.loop()
        
        # Step 2: renumber the forward direction graph
        self.G.reverse_edges()
        self.G.renumber_nodes(pass1.finishing_time)
        #for ii in range(len(pass1.finishing_time)):
        #    print("{}: {}".format(ii,pass1.finishing_time[ii]))

        # Step 3: run DFS on forward with new numbers
        pass2 = DFS(self.G)
        pass2.loop()

        k_largest_leaders = pass2.get_k_largest_leaders(self.k)
        #print(pass2.leader_sizes)

        return k_largest_leaders

import time
def main():
    
    starttime = time.time()

    source_dir = "course2/test_assignment1/"
    input_files = [f for f in os.listdir(source_dir) if "input" in f]
    for input_file in input_files:
       #print("Starting {}".format(input_file))
        f = os.path.join(source_dir,input_file)
        G = Graph(f,testing=True)
        s = SCC_sizes(G,k=5)
        k_largest = s.run()
        #print("\tCalculated: {} Truth: {}".format(k_largest,G.groundtruth))
        assert k_largest == G.groundtruth

    print("Starting final input for assignment:")
    input_file = "assignment1_input.txt"
    source_dir = "course2/"
    f = os.path.join(source_dir,input_file)
    G = Graph(f,testing=False)
    s = SCC_sizes(G,k=5)
    k_largest = s.run()
    print("\tCalculated: {}".format(k_largest))

    print("Elapsed time: {}".format(time.time()-starttime))
    
thread = threading.Thread(target=main)
thread.start()