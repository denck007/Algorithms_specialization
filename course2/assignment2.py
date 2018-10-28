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
        self.null_cost = 1e5 # theoretical max value
        
        # the max number of items that we can ever see is the number of verticies in the graph
        # Add 1 to this so that we can deal with 1 based vertex numbers in vertex_heap
        # Add an additiona 1 to this so that when we bubble down and try to compare off the end of the heap, we can redirect them to the 
        #   a value that is gaurentteed to never have an associated vertex and thus never have a length less than null_cost
        self.max_heap_size = num_verticies+2 

        self.heap = [self.null_cost for n in range(self.max_heap_size)]
        self.heap_vertex = [-1 for n in range(self.max_heap_size)]
        self.vertex_heap = [-1 for n in range(self.max_heap_size)]
        self.end_of_heap = 0 # the index in self.heap of the first item not included, ie the index where an item can be inserted

    def extract_min(self):
        '''
        Remove the minimum key value from the heap, return (vertex,length)
        '''
        vertex = self.heap_vertex[0]
        length = self.delete(vertex)
        return (vertex,length)

    def insert(self,vertex,length):
        '''
        Add the length to vertex to the heap
        '''
        self.heap[self.end_of_heap] = length
        self.heap_vertex[self.end_of_heap] = vertex
        self.vertex_heap[vertex] = self.end_of_heap
        self._bubble_up(self.end_of_heap)
        self.end_of_heap += 1

    def delete(self,vertex):
        '''
        remove everything associated with vertex from the heap
        return the length for vertex
        '''
        heap_idx = self.vertex_heap[vertex]
        length = self.heap[heap_idx]
        self._swap(heap_idx,self.end_of_heap-1)
        self._bubble_down(heap_idx)
        self.heap[self.end_of_heap] = self.null_cost
        self.end_of_heap -= 1

        return length

    def _bubble_up(self,change_idx):
        '''
        maintain the invariant that all parents are >= children
        '''
        parent_idx = change_idx//2
        if self.heap[parent_idx] < self.heap[change_idx]:
            self._swap(parent_idx,change_idx)
            self._bubble_up(parent_idx)

    def _bubble_down(self,change_idx):
        '''
        maintain invariant that all parents are >= children
        '''
        # make sure we do not go off the end of the heap
        # -1 is for 0 based indexing in self.heap
        left_idx = min(2*change_idx,self.max_heap_size-1)
        right_idx = min(2*change_idx+1,self.max_heap_size-1)

        left_length = self.heap[left_idx]
        right_length = self.heap[right_idx]

        if left_length > right_length:
            left_length = self.null_cost
        else:
            right_length = self.null_cost

        if self.heap[change_idx] < left_length:
            self._swap(change_idx,left_idx)
            self._bubble_down(left_idx)
        elif self.heap[change_idx] < right_length:
            self._swap(change_idx,right_idx)
            self._bubble_down(right_idx)

    def _swap(self,source_idx,destination_idx):
        '''
        Utility function to swap 2 items in the heap
        updates all the corresponding arrays
        Does not validate that the swap maintains the invariants!
        '''
        tmp = self.heap[source_idx]
        self.heap[source_idx] = self.heap[destination_idx]
        self.heap[destination_idx] = tmp
        
        tmp = self.vertex_heap[source_idx]
        self.vertex_heap[source_idx] = self.vertex_heap[destination_idx]
        self.vertex_heap[destination_idx] = tmp
        
        tmp = self.heap_vertex[source_idx]
        self.heap_vertex[source_idx] = self.heap_vertex[destination_idx]
        self.heap_vertex[destination_idx] = tmp

G = Graph("course2/test_assignment2/input_random_1_4.txt",testing=True)
print(G.output)