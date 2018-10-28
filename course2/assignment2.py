'''
Algorithms: Dijkstra's algorithm for shortest path between 1 vertex and every other vertex in a graph


'''
import os

class Graph():

    def __init__(self,fname,testing=False):
        '''
        read in the graph defined in fname
        if testing, read in the test results by subsituting 'output' for 'input' in fname

        fname structure:
        * Each line is a vertex
        * The number at the start of the line is the vertex number
        * On each line there are comma seperated tuples of (head_vertex,edge_lenght)
        * If there are more than 1 edge for each vertex, the additional edges are seperated by tabs
        '''

        self.vertex_edges = {}
        self.edge_verticies = {}
        self.edge_lengths = {}
        self.num_edges = 0

        self.output = None
        self.paths = {}

        with open(fname,'r') as f:
            for line in f.readlines():
                line_split = line.split("\t")

                vertex = int(line_split[0])
                self.vertex_edges.update({vertex:[]})
                for edge in line_split[1:]:
                    edge_split = edge.strip("\n").split(",")
                    self.num_edges+=1
                    self.vertex_edges[vertex].append(self.num_edges)

                    self.edge_verticies.update({self.num_edges:[vertex,int(edge_split[0])]})
                    self.edge_lengths.update({self.num_edges:int(edge_split[1])})

        if testing:
            result_fname = fname.replace("input","output")
            with open(result_fname,'r') as f:
                line = f.readline()
                self.output = [int(x) for x in line.strip("\n").split(",")]
            result_fname= fname.replace("input","paths")
            
            with open(result_fname,'r') as f:
                for line in f.readlines():
                    line_split = line.strip("\n").split(" => path => ")
                    end = int(line_split[0])
                    path_verticies = [int(x) for x in line_split[1].split(",")]
                    self.paths.update({end:path_verticies})
                    

class Heap():
    '''
    Implentation of heap data stucture for Dijkstra

    This is kind a weird to do in python. I want to manually implement everything about how the data is stored, so not using pop() or append()
    The underlying data is stored in python lists.
    There are 2 lists: the keys which are the distances from vertex s to w and the 
    '''

    def __init__(self,num_verticies,first_vertex=0):
        '''
        num_verticies are the total number of verticies in the graph
        first_vertex is the first vertex that the alogrithm is working on, it should be set to length=0
        '''

        # keys[idx] is the heap
        self.keys = [1e5 for n in range(num_verticies+1)]
        
        # keys[vertex_key[vertex]] gives the shortest length to vertex along an edge that crosses the frontier
        # vertex_key tracks the location of the key for a vertex in the heap
        # when ever the heap is modified vertex_key needs to be updated accordingly
        self.vertex_key = [-1 for n in range(num_verticies+1)]

        #initialize first_vertex
        self.keys[0] = 0
        self.vertex_key[first_vertex] = 0 # the index of first_vertex in keys (ie the length) is 0

    def extract_min(self):
        '''
        Remove the minimum key value from the heap, return (vertex,length)
        '''
        pass

    def insert(self,vertex,length):
        '''
        Add the length to vertex to the heap
        '''
        pass

    def delete(self,vertex):
        '''
        remove everything associated with vertex from the heap
        return the length for vertex
        '''
        pass

    def _bubble_up(self):
        pass
    def _bubble_down(self):
        pass


G = Graph("course2/test_assignment2/input_random_1_4.txt",testing=True)
print(G.output)