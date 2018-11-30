'''
Course 3, Week1: Intro to greedy algorithms, Assignment 1: Q3 Prim's minimum spanning tree

Implement Prims MST algorithm on an undirected graph with integer cost (may be negative)

'''
import os
import sys
sys.path.append("/home/neil/Algorithms_specialization")
from helpers.Heap import Heap

class Graph():

    def __init__(self,fname,testing=False):
        '''
        read in the graph defined in fname
        if testing, read in the test results by subsituting 'output' for 'input' in fname

        fname structure:
        * Each line is a edge
        * order of each line is node1 node2 cost
        * the first line is number of nodes, number of edges
        '''

        self.vertex_edges = {}
        self.edge_verticies = {}
        self.edge_costs = {}
        self.num_edges = 0
        self.num_verticies = 0

        with open(fname,'r') as f:
            data = f.readlines()

        self.num_verticies,self.num_edges = [int(x) for x in data[0].strip().split()]
        for edge_id,line in enumerate(data[1:]):
            u,v,cost = [int(x) for x in line.strip().split()]
            
            self.edge_verticies[edge_id] = [u,v]
            self.edge_costs[edge_id] = cost

            if u in self.vertex_edges:
                self.vertex_edges[u].append(edge_id)
            else:
                self.vertex_edges[u] = [edge_id]
            if v in self.vertex_edges:
                self.vertex_edges[v].append(edge_id)
            else:
                self.vertex_edges[v] = [edge_id]
        
        if testing:
            result_fname = fname.replace("input","output")
            with open(result_fname,'r') as f:
                line = f.readline()
                self.true_output = int(line.strip())


def add_edge_from_vertex(source_vertex,h,g,seen):
    '''
    add all edges out of source_vertex to the heap,h. 
    The heap tracks by cost to a vertex, so need to identify which new vertex the edge is pointing towards
    Also need to verify that the potential new vertex is not already in the heap, and if it is make sure its value is correct

    returns the updated heap
    '''

    for edge in g.vertex_edges[source_vertex]:
        # the graph is undirected to need to look at both ends
        u,v = g.edge_verticies[edge]

        # flag which vertex of the edge has not been seen
        #   this is the vertex we want to add to the heap
        if not seen[u]:
            to_explore = u
        elif not seen[v]:
            to_explore = v
        else:
            continue
        
        if h.id_heap[to_explore] < h.null_cost:
            # if we have already found an edge to this vertex, we want to make sure we
            #    are only looking at the cheapest edge
            min_cost = h.delete(to_explore)
            min_cost = min(min_cost,g.edge_costs[edge])
        else:
            # if the vertex has never been added to the heap,
            #   the cheapest edge to the vertex is the current edge
            min_cost = g.edge_costs[edge]
        h.insert(to_explore,min_cost) # add the cheapest edge to the heap

    return h

def prims(fname,testing=False):
    '''
    Run Prim's Minimum Span Tree algorithom on graph a graph defined in fname
    returns the total cost and the graph
    '''
    # initialize structures
    g = Graph(fname,testing=testing)
    h = Heap(g.num_verticies)
    seen = [False for x in range(g.num_verticies+1)]

    # Start at any vertex, the provided graphs all start at node 1, so using that
    source_vertex = 1
    seen[source_vertex] = True
    h = add_edge_from_vertex(source_vertex,h,g,seen)
    
    total_cost = 0
    
    # keep extracting the minimum cost edge from the heap and 
    #  update/create the lowest cost edges to any vertex that is connected to an edge from
    #  the extracted vertex
    while len(h) > 0:
        vertex,cost = h.extract_min()
        seen[vertex] = True
        total_cost += cost
        h = add_edge_from_vertex(vertex,h,g,seen)

    return total_cost,g

base_path = "course3/test_assignment1/question3"
fnames = [f for f in os.listdir(base_path) if "input" in f]

for fname in fnames:
    testing = True
    total_cost,g = prims(os.path.join(base_path,fname),testing=testing)

    if testing:
        if g.true_output == total_cost:
            print("Correct: {} Got {}".format(fname,total_cost))
        else:
            print("Error: {} Got {} Expected {}".format(fname,total_cost,g.true_output))


print("Starting Final output:")

fname = "course3/assignment1_q3_input.txt"

total_cost,g = prims(fname)
print("Final solution to problem: {}".format(total_cost))


