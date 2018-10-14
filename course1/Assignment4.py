'''
Assignment 4 part 1
Minimum Cut algorithm using random contractions

Given a text file detailing a graph, what is the minimum cut of the graph?
The graph is assumed to be connected and undirected.
Return the number of edges crossed in the minumum cut

Input file is:
    - column1 in each row is the vertex id
    - the rest of the columns are verticies that it shares an edge with

The algorithm is random so it will need to be run a multiple times to get the minimum cut
Initially it is best to implement the contraction alorithm niavely by creating a new graph for each run 

'''

import random

def build_adjacency_list(input):
    '''
    input is a list of lists
    returns vertex_edges and edge_verticies dicts
    input: 
        First item in each row is the vertex id
        rest of items in each row are connected verticies
    output:
        vertex_edges:
            vertex_edges[n_ii] are the indicies of the edges that have an end at vertex n_ii
        edge_verticies:
            edge_verticies[m_jj] are the [start,end] verticies of edge m_jj
    '''
    num_verticies = input[-1][0]-1
    edge_verticies = build_edge_verticies(input)
    vertex_edges = build_vertex_edges(edge_verticies,num_verticies)

    return vertex_edges,edge_verticies

def build_edge_verticies(input):
    '''
    Given an input list build the edge to verticies dict
    Note that self loops are not filtered out here
    input: 
        First item in each row is the vertex id
        rest of items in each row are connected verticies
    output:
        edge_verticies:
            edge_verticies[m_jj] are the [start,end] verticies of edge m_jj
    '''
    edge_verticies = {}
    num_edges = 0
    for row in input:
        r = sorted(row[1:])
        for ii in r:
            if ii < row[0]: # already created edge in previous iteration
                continue
            num_edges += 1
            edge_verticies.update({num_edges:[row[0],ii]})
    return edge_verticies

def build_vertex_edges(edge_verticies,num_verticies):
    '''
    given a edge_verticies dict, return the corresponding vertex_edges dict
    note that self loops are not filtered out here
    input:
        edge_verticies:
            dict where edge_verticies[m_jj] is verticies [end_0,end_1] for edge m_jj
    output:
        vertex_edges:
            dict where vertex_edges[n_ii] are edges that have an end at vertex n_ii
    '''
    vertex_edges = {}
    for edge in edge_verticies.keys():
        for vertex in edge_verticies[edge]:
            if vertex in vertex_edges.keys():
                vertex_edges[vertex].append(edge)
            else:
                vertex_edges.update({vertex:[edge]})
    return vertex_edges

def remove_self_loops(vertex_edges,edge_verticies):
    '''
    Remove references to self loops in vertex_edges and edge_verticies
    This function removes self loops by removing the edge from the edge_verties dict and 
    Returns the lists
    '''
    self_loop_edges = [] # track which edges are self loops so we can remove them from vertex_edge
    keys = list(edge_verticies.keys())
    for edge in keys:
        if edge_verticies[edge][0] == edge_verticies[edge][1]:  #is self loop
            edge_verticies.pop(edge)
            self_loop_edges.append(edge)

    # remove the reference to edges in vertex_edges
    # remove any verticies that are not attached to an edge
    keys = list(vertex_edges.keys())
    for vertex in keys:
        for edge in self_loop_edges:
            while edge in vertex_edges[vertex]: # remove all instances of the vertex, multiples happen in self loops
                vertex_edges[vertex].remove(edge)
        if vertex_edges[vertex] == []:
            vertex_edges.pop(vertex)

    
    return vertex_edges,edge_verticies

def contract_graph(vertex_edges,edge_verticies,edge):
    '''
    Contract a graph by removing the specified edge via merging the corresponding verticies
    '''
    # remove reference to edge in vertex_edges
    vertex1 = edge_verticies[edge][0]
    vertex2 = edge_verticies[edge][1]

    vertex_edges[vertex1].remove(edge) # removed edge from vertex1
    vertex_edges[vertex2].remove(edge) # remove the edge from 2nd vertex
    vertex_edges[vertex1].extend(vertex_edges[vertex2]) # move all edges attached to vertex2 to vertex1
    vertex_edges.pop(vertex2) # delete the 2nd vertex
    
    # go over all the edges, replace references to 2nd vertex with 1st vertex
    for jj in edge_verticies.keys():
        if edge_verticies[jj][0] == vertex2:
            edge_verticies[jj][0] = vertex1
        if edge_verticies[jj][1] == vertex2:
            edge_verticies[jj][1] = vertex1

        #for vertex_idx in range(len(edge_verticies[jj])):
        #    if edge_verticies[jj][vertex_idx] == vertex2:
        #        edge_verticies[jj][vertex_idx] = vertex1
    
    # finally delete the edge
    edge_verticies.pop(edge)

    return vertex_edges,edge_verticies

def min_cut_random_contraction(vertex_edges,edge_verticies):
    '''
    Given a graph defined by vertex_edges and edge_verticies compute minimum cut size of a random sequence of contractions
    This is unlikely to return the actual minimum cut of the graph in running this function 1 time
    Run this multiple times on the same graph to get a different sequence of cuts and be more likely to get the actual min cut
    '''
    #edges_deterministic = list(edge_verticies.keys())
    while len(vertex_edges) > 2:
        #
        #edge = edges_deterministic.pop()
        
        vertex_edges,edge_verticies = remove_self_loops(vertex_edges,edge_verticies)
        edge = random.choice(list(edge_verticies.keys()))
        print("working on edge {}".format(edge))
        vertex_edges,edge_verticies = contract_graph(vertex_edges,edge_verticies,edge)
        
    return len(edge_verticies)
'''
input = [[1,2,3,4],
        [2,1,4],
        [3,1,4],
        [4,1,2,3]]
vertex_edges_true = {
                    1:[1,2,3],
                    2:[1,4],
                    3:[2,5],
                    4:[3,4,5]}
edge_verticies_true = {
                    1:[1,2],
                    2:[1,3],
                    3:[1,4],
                    4:[2,4],
                    5:[3,4]}
min_cut_true = 2
vertex_edges,edge_verticies = build_adjacency_list(input)
assert edge_verticies == edge_verticies_true,"Failed edge_verticies\n\t{}\n\t{}".format(edge_verticies,edge_verticies_true)
assert vertex_edges == vertex_edges_true, "Failed vertex_edges\n\t{}\n\t{}".format(vertex_edges,vertex_edges_true)
min_cut = len(edge_verticies)
for ii in range(10):
    vertex_edges,edge_verticies = build_adjacency_list(input)
    new_estimate = min_cut_random_contraction(vertex_edges.copy(),edge_verticies.copy())
    min_cut = min(new_estimate,min_cut)
    print("iteration {} min_cut: {}".format(ii,min_cut))

'''
input = [[1,1,2,3,4,5,6],
        [2,1,3,5],
        [3,1,2,6],
        [4,1,6],
        [5,1,2],
        [6,1,3,6]]
vertex_edges_true = {
                1:[1,1,2,3,4,5,6],
                2:[2,7,8],
                3:[3,7,9],
                4:[4,10],
                5:[5,8],
                6:[6,9,10,11,11]}
edge_verticies_true = {
                    1:[1,1],
                    2:[1,2],
                    3:[1,3],
                    4:[1,4],
                    5:[1,5],
                    6:[1,6],
                    7:[2,3],
                    8:[2,5],
                    9:[3,6],
                    10:[4,6],
                    11:[6,6]}
vertex_edges,edge_verticies = build_adjacency_list(input)
assert edge_verticies == edge_verticies_true,"Failed edge_verticies\n\t{}\n\t{}".format(edge_verticies,edge_verticies_true)
assert vertex_edges == vertex_edges_true, "Failed vertex_edges\n\t{}\n\t{}".format(vertex_edges,vertex_edges_true)
min_cut = len(edge_verticies)
for ii in range(20):
    vertex_edges,edge_verticies = build_adjacency_list(input)
    new_estimate = min_cut_random_contraction(vertex_edges.copy(),edge_verticies.copy())
    min_cut = min(new_estimate,min_cut)
    print("iteration {} min_cut: {}".format(ii,min_cut))
    
print("Passed test")
