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
import os
import random
import time

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

#@profile
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
    edges = list(edge_verticies.keys())
    for jj in edges:
        if edge_verticies[jj][0] == vertex2:
            edge_verticies[jj][0] = vertex1
        if edge_verticies[jj][1] == vertex2:
            edge_verticies[jj][1] = vertex1
        if edge_verticies[jj][0] == edge_verticies[jj][1]: # remove any self loops that are created
            edge_verticies.pop(jj)

    # finally delete the edge if it still exists
    if edge in edge_verticies:
        edge_verticies.pop(edge)

    return vertex_edges,edge_verticies
#@profile
def min_cut_random_contraction_iteration(vertex_edges,edge_verticies):
    '''
    Given a graph defined by vertex_edges and edge_verticies compute minimum cut size of a random sequence of contractions
    This is unlikely to return the actual minimum cut of the graph in running this function 1 time
    Run this multiple times on the same graph to get a different sequence of cuts and be more likely to get the actual min cut
    '''
    while len(vertex_edges) > 2:
        edge = random.choice(list(edge_verticies.keys()))
        vertex_edges,edge_verticies = contract_graph(vertex_edges,edge_verticies,edge)
    return len(edge_verticies)

def min_cut_random_contraction(input):
    '''

    Given a graph defined by vertex_edges and edge_verticies compute minimum cut size of a random sequence of contractions
    This runs the min_cut_random_contraction_iteration function n**2 times to get a high probability that we find the correct min cut
    '''
    
    num_iterations = len(input)**2
    min_cut = len(input)**2 #this is an overestimate of the max possible number of edges
    start_time = time.time()
    for ii in range(num_iterations):
        vertex_edges,edge_verticies = build_adjacency_list(input)
        new_estimate = min_cut_random_contraction_iteration(vertex_edges,edge_verticies)
        min_cut = min(new_estimate,min_cut)
        elasped_time = time.time() - start_time
        average_time = elasped_time/(ii+1)*1000
        print("\riteration {}/{} new estimate: {} min_cut: {} total time: {:.1f}s avg time: {:.1f}ms".format(ii,num_iterations,new_estimate,min_cut,elasped_time,average_time),end="")

    print()
    return min_cut

def read_input_text_file(fname,testing=False):
    '''
    Read in a text file and return the array of arrays needed to generate the graph
    if testing then we know the ground truth, so read it in and return it as well
    '''
    data = []
    with open(fname,'r') as f:
        for line in f.readlines():
            data.append([int(x) for x in line.strip("\n").split()])
    
    if testing:
        with open(fname.replace("input","output"),'r') as f:
            groundtruth = f.readlines()
        groundtruth = int(groundtruth[0].strip("\n"))
        return data,groundtruth
    else:
        return data

base_path = "course1/test_assignment4"
test_files = [f for f in os.listdir(base_path) if "input" in f]
for f in test_files:
    if int(f[f.rfind("_")+1:-4]) > 9: # skip the big ones
        continue
    print("Starting on file {}".format(f))
    input,truth = read_input_text_file(os.path.join(base_path,f),testing=True)
    min_cut = min_cut_random_contraction(input)
    if min_cut == truth:
        print("Correct min_cut for {} of {}".format(f,min_cut))
    else:
        print("Failed to get correct min cut for {} predicted: {} truth: {}".format(f,min_cut,truth))

print("Starting final input")
input = read_input_text_file("course1/assignment4_input.txt",testing=False)
min_cut = min_cut_random_contraction(input)
print("Minimum cut for assignment is {}".format(min_cut))
