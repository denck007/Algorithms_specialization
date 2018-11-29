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
        u,v = g.vertex_edges[edge]

        # flag which vertex of the edge has not been seen
        #   this is the vertex we want to add to the heap
        if not seen[u]:
            to_explore = u
        elif not seen[v]:
            to_explore = v
        else:
            assert False, "invalid vertex to explore!"
        
        if to_explore in h:
            # if we have already found an edge to this vertex, we want to make sure we
            #    are only looking at the cheapest edge
            min_cost = h.delete(to_explore)
            min_cost = min(min_cost,g.edge_cost[edge])
        else:
            # if the vertex has never been added to the heap,
            #   the cheapest edge to the vertex is the current edge
            min_cost = g.edge_cost[edge]
        h.insert(to_explore,min_cost) # add the cheapest edge to the heap

    return h



