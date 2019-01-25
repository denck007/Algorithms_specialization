'''
Course 4, Week4: 2 SAT

Given an input of constraints, is it possible to satisfy all of the constraints at the same time?

Input:
<number of clauses and number of literals> # number of clauses == number of literals in this assignment
<clause 1 part 1> <clause 1 part 2> 
<clause 2 part 1> <clause 2 part 2> 
...
<clause n part 1> <clause n part 2> 

Output: True or false of if the constraints are satisfiable


Going to use the hint and reduce the problem to that of computing SCCs of a directed graph
For each literal there are  + and - nodes. When the clause (A or B) is read in, edges are created from (not(A) to B) and (not(B) to A)
The SCCs of this graph are computed
If both X and not(X) are in the same SCC then the set of clauses is not satisfiable
See https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/ for more info

This leverages some code from the SCC assignment in course 2, but I had to rewrite some of it because that did not get the correct vertex numbers, just the number of items in each group.
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
        self.fname = fname
        self.edge_verticies = {}
        self.num_nodes = 0
        self.num_edges = -1
        with open(fname,"r") as f:
            data = f.readlines()

        self.num_literals = int(data[0])+1
        self.num_clauses = int(data[0])
        self.num_nodes = 2*self.num_literals

        for jj,line in enumerate(data[1:]):
            edge = [int(x) for x in line.strip("\n").split()]

            node1 = edge[0]
            node2 = edge[1]

            self.num_edges += 1
            self.edge_verticies[self.num_edges] = [-node1+ self.num_literals,node2+ self.num_literals]
            self.num_edges += 1
            self.edge_verticies[self.num_edges] = [-node2+ self.num_literals,node1+ self.num_literals]

        self.build_vert_edges()

        if testing:
            with open(fname.replace("input","output"),'r') as f:
                solution = f.readlines()
            self.solution = int(solution[0])
    #@profile
    def build_vert_edges(self):
        '''
        Build the vert_edges dictionary from the edge_verticies dictionary
        '''    
        self.vert_edges = {}
        #self.vertex_exist = [False for x in range(self.num_nodes+1)]
        for jj in self.edge_verticies:
            node0 = self.edge_verticies[jj][0]
            node1 = self.edge_verticies[jj][1]
            if node0 is None:
                continue
            if node1 is None:
                continue

            if node0 in self.vert_edges:
                self.vert_edges[node0].append(jj)
            else:
                self.vert_edges[node0] = [jj]
            
            #if node1 not in self.vert_edges:
            #    self.vert_edges[node1] = []


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
        self.groups = {}
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

        if ii not in self.G.vert_edges:
            return 

        if self.s in self.groups:
            self.groups[self.s].append(ii)
        else:
            self.groups[self.s] = [ii]

        for edge in self.G.vert_edges[ii]:
            end_node = self.G.edge_verticies[edge][1] # end node of edge
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
            if ii in self.leader_sizes:
                self.leader_sizes[ii] += 1
            elif ii is None:
                continue
            else:
                self.leader_sizes.update({ii:1})
        # if nodes do not have any edges this algorith will tag the node with itself as a leader, and no other items have that same leader
        keys = list(self.leader_sizes)
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


class SCC():
    '''
    Calculate the SCC of the input graph
    '''
    def __init__(self,graph):
        '''
        Initialize the object instance
        graph is an instance of a Graph object
        '''
        self.G = graph

    def Compute_SCC(self):
        '''
        Run the DFS algorithm on the graph to find the sizes of the k largest SCCs

        Step1:
            * reverse the graph
            * run DFS loop on the reveresed graph to get the ideal ordering
        Step2: 
            * Update the graph node numbering, remembering the original ordering
        Step3:
            * run DFS loop on the forward graph with new numbering
        '''

        # Step 1:
        self.G.reverse_edges()
        pass1 = DFS(self.G)
        pass1.loop()
        
        # Step 2: renumber the forward direction graph
        self.G.reverse_edges()
        self.G.renumber_nodes(pass1.finishing_time)

        # When renumbering the nodes with the finishing time we mess up the numbering system
        # Need to be able to convert from the finishing time node numbers back to the original node numbers
        inverse_renumber = [None for x in range(self.G.num_nodes+1)]
        for original_number,renumbered in enumerate(pass1.finishing_time):
            if renumbered is None:
                inverse_renumber.append(None)
            else:
                inverse_renumber[renumbered] = original_number

        # Step 3: run DFS on forward with new numbers
        dfs = DFS(self.G)
        dfs.loop()
        
        # convert the ids in the groups from the finishing time numbers to actual node numbers
        self.groups = {}
        for leader in dfs.groups:
            self.groups[inverse_renumber[leader]] = [inverse_renumber[x] for x in dfs.groups[leader] if x is not None]

    def Identify_Inverse_In_Same_Group(self):
        '''
        Go over all of the groups in the SCCs. Find if any of the nodes have their inverse (negative value) in the same SCC.
        If they are in the same SCC then the solution is not viable, return False
        '''

        for leader in self.groups:
            # get all of the nodes with their actual positive or negative id
            nodes = [node - self.G.num_literals for node in self.groups[leader]]

            for node in nodes:
                if -node in nodes:
                    return 0 # No need to keep going if we find a failure

        # if we make it all the way through without finding a match then the combination is valid
        return 1

import time
def main():
    
    starttime = time.time()

    base_path = "course4/test_assignment4/"

    for fname in os.listdir(base_path):
        if "input" not in fname:
            continue
        #if int(fname[fname.rfind("_")+1:-4]) > 60: # only test on short problems
        #    continue
        
        #if "input_beaunus_2_2.txt" not in fname:
        #    continue

        print("Starting {}".format(fname))
        f = os.path.join(base_path,fname)
        G = Graph(f,testing=True)

        s = SCC(G)
        s.Compute_SCC()
        result = s.Identify_Inverse_In_Same_Group()
        if result == s.G.solution:
            print("\tCalculated: {} Truth: {}".format(result,G.solution))
        else:
            print("! Incorrect solution!\nCalculated: {} Truth: {}\n".format(result,G.solution))

    print("\n\nStarting final input for assignment:")
    base_fname = "assignment4_input"
    base_path = "course4/"
    for idx in range(1,7):
        fname = base_fname + str(idx) + ".txt"
        f = os.path.join(base_path,fname)
        G = Graph(f,testing=False)
        s = SCC(G)
        s.Compute_SCC()
        result = s.Identify_Inverse_In_Same_Group()
        print("\tCalculated: {}".format(result))

    print("Elapsed time: {}".format(time.time()-starttime))
thread = threading.Thread(target=main)
thread.start()