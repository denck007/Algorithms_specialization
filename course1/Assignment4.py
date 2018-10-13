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


def build_adjacency_list(input):
    '''
    input is a list of lists
    returns vertex_edge and edge_vertex lists
    input: 
        First item in each row is the vertex id
        rest of items in each row are connected verticies
    output:
        vertex_edges:
            vertex_edges[n_ii] are the indicies of the edges that have an end at vertex n_ii
        edge_verticies:
            edge_verticies[m_jj] are the [start,end] verticies of edge m_jj
    '''
    num_verticies = input[-1][0] +1
    edge_verticies = build_edge_verticies(input)
    vertex_edges = build_vertex_edges(edge_verticies,num_verticies)

    return edge_verticies,vertex_edges

def build_edge_verticies(input):
    '''
    Given an input list build the edge to verticies list
    Note that self loops are not filtered out here
    input: 
        First item in each row is the vertex id
        rest of items in each row are connected verticies
    output:
        edge_verticies:
            edge_verticies[m_jj] are the [start,end] verticies of edge m_jj
    '''
    edge_verticies = [[]]
    for row in input:
        r = sorted(row[1:])
        for ii in r:
            if ii < row[0]: # already created edge in previous iteration
                continue
            edge_verticies.append([row[0],ii])
    return edge_verticies

def build_vertex_edges(edge_verticies,num_verticies):
    '''
    given a edge_verticies list, return the corresponding vertex_edges list
    note that self loops are not filtered out here
    input:
        edge_verticies:
            list where edge_verticies[m_jj] is verticies [end_0,end_1] for edge m_jj
        num_verticies: number of verticies in the graph
    output:
        vertex_edges:
            list where vertex_edges[n_ii] are edges that have an end at vertex n_ii
    '''
    vertex_edges = [[] for x in range(num_verticies)]
    for jj,edge in enumerate(edge_verticies):
        for vertex in edge:
            vertex_edges[vertex].append(jj)
    return vertex_edges

input = [[1,2,3,4],
        [2,1,4],
        [3,1,4],
        [4,1,2,3]]
vertex_edges_true = [
                [],
                [1,2,3],
                [1,4],
                [2,5],
                [3,4,5]]
edge_verticies_true = [[],
                    [1,2],
                    [1,3],
                    [1,4],
                    [2,4],
                    [3,4]]
edge_verticies,vertex_edges = build_adjacency_list(input)
assert edge_verticies == edge_verticies_true,"Failed edge_verticies\n\t{}\n\t{}".format(edge_verticies,edge_verticies_true)
assert vertex_edges == vertex_edges_true, "Failed vertex_edges\n\t{}\n\t{}".format(vertex_edges,vertex_edges_true)



input = [[1,1,2,3,4,5,6],
        [2,1,3,5],
        [3,1,2,6],
        [4,1,6],
        [5,1,2],
        [6,1,3,6]]
vertex_edges_true = [
                [],
                [1,1,2,3,4,5,6],
                [2,7,8],
                [3,7,9],
                [4,10],
                [5,8],
                [6,9,10,11,11]]
edge_verticies_true = [[],
                    [1,1],
                    [1,2],
                    [1,3],
                    [1,4],
                    [1,5],
                    [1,6],
                    [2,3],
                    [2,5],
                    [3,6],
                    [4,6],
                    [6,6]]
edge_verticies,vertex_edges = build_adjacency_list(input)
assert edge_verticies == edge_verticies_true,"Failed edge_verticies\n\t{}\n\t{}".format(edge_verticies,edge_verticies_true)
assert vertex_edges == vertex_edges_true, "Failed vertex_edges\n\t{}\n\t{}".format(vertex_edges,vertex_edges_true)


print("Passed test")
