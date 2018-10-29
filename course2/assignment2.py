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
        * The number at the start of the line is added_to_heap_by[1] = the vertex number
        * On each line there are comma seperated tuples of (head_vertex,edge_lenght)
        * If there are more than 1 edge for each vertex, the additional edges are seperated by tabs
        '''

        self.vertex_edges = {}
        self.edge_verticies = {}
        self.edge_lengths = {}
        self.shortest_path = {}
        self.paths = {}
        self.num_edges = 0
        self.num_verticies = 0

        self.true_output = None
        self.true_paths = {}

        with open(fname,'r') as f:
            for line in f.readlines():
                if line[0] == "#":
                    continue
                line_split = line.split("\t")

                vertex = int(line_split[0])
                self.num_verticies += 1
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
                self.true_output = [int(x) for x in line.strip("\n").split(",")]
            result_fname= fname.replace("input","paths")
            
            with open(result_fname,'r') as f:
                for line in f.readlines():
                    line_split = line.strip("\n").split(" => path => ")
                    end = int(line_split[0])
                    path_verticies = [int(x) for x in line_split[1].split(",")]
                    self.true_paths.update({end:path_verticies})

    def initialize_shortest_path(self,start_vertex=1):
        '''
        initialize self.shortest_path dict by setting the length of start_vertex to 0
        '''            
        self.shortest_path.update({start_vertex:0})
        self.paths.update({start_vertex:[start_vertex]})

class Heap():
    '''
    Implentation of heap data stucture for Dijkstra

    This is kind a weird to do in python. I want to manually implement everything about how the data is stored, so not using pop() or append()
    The underlying data is stored in python lists.
    There are 2 lists: the keys which are the distances from vertex s to w and the 
    '''

    def __init__(self,num_verticies):
        '''
        num_verticies are the total number of verticies in the graph
        '''
        self.null_cost = int(1e5) # theoretical max value
        
        self.num_verticies = num_verticies
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
        
        self._swap(heap_idx,self.end_of_heap-1) #move value to be deleted to end of array
        self.end_of_heap -= 1 # move the end of the heap marker
        self.heap_vertex[self.end_of_heap] = -9 # remove all reference to it
        self.heap[self.end_of_heap] = self.null_cost+1
        self._bubble_down(heap_idx)

        return length

    def _bubble_up(self,change_idx):
        '''
        maintain the invariant that all parents are <= children
        '''
        parent_idx = change_idx//2
        if self.heap[parent_idx] > self.heap[change_idx]:
            self._swap(parent_idx,change_idx)
            self._bubble_up(parent_idx)

    def _bubble_down(self,change_idx):
        '''
        maintain invariant that all parents are <= children
        '''
        # make sure we do not go off the end of the heap
        # +1 and +2 is for 0 based indexing in self.heap
        left_idx = min(2*change_idx+1,self.end_of_heap)
        right_idx = min(2*change_idx+2,self.end_of_heap)

        left_length = self.heap[left_idx]
        right_length = self.heap[right_idx]

        # If the value is less than both left and right, we want to swap with the smaller of the 2
        # This makes it so there is only ever 1 child that is less than our value
        #   which makes it the code for comparision to our value not need multiple comparisions in each if statement
        if left_length > right_length:
            left_length = self.null_cost
        else:
            right_length = self.null_cost

        # the second comparision in each if statement is the base case, ie we hit the end of the heap
        if (self.heap[change_idx] < left_length) and (left_idx < self.end_of_heap): 
            self._swap(change_idx,left_idx)
            self._bubble_down(left_idx)
        elif (self.heap[change_idx] < right_length) and (right_idx < self.end_of_heap):
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
        
        tmp = self.vertex_heap[self.heap_vertex[source_idx]]
        self.vertex_heap[self.heap_vertex[source_idx]] = self.vertex_heap[self.heap_vertex[destination_idx]]
        self.vertex_heap[self.heap_vertex[destination_idx]] = tmp
        
        tmp = self.heap_vertex[source_idx]
        self.heap_vertex[source_idx] = self.heap_vertex[destination_idx]
        self.heap_vertex[destination_idx] = tmp

    def __len__(self):
        return self.end_of_heap

    def force_validate(self):
        '''
        Go through the tree vertex by vertex and verify that every child is greater or equal to its parent
        '''
        





def add_to_heap(h,g,tail,explored,added_to_heap_by):
    '''
    Add all the verticies connected to tail vertex by and edge to the heap
    h: Heap instance
    g: Graph instance
    tail: vertex number
    explored: array of bools indicating if we have explored the vertex before
    added_to_heap_by: array of integers indicating the tail that added this vertex to the heap

    returns an updated added_to_heap array
    '''

    for edge in g.vertex_edges[tail]:
        head = g.edge_verticies[edge][1]
        if not explored[head]:
            if head == 7:
                print("vertex7")
            length = g.edge_lengths[edge]

            # if the head is already on the heap, added_to_heap_by[head]==-1 means it has not been added yet
            if added_to_heap_by[head] >= 0:
                previous_length = h.delete(head)
                if length > previous_length:
                    length = previous_length
                    #added_to_heap_by[head] = added_to_heap_by[head] no need to update this
                else:
                    #length = length no need to update this
                    added_to_heap_by[head] = tail
            else:
                added_to_heap_by[head] = tail
            h.insert(head,length)

    return added_to_heap_by

verticies_to_check = [7,37,59,82,99,115,133,165,188,197]
G = Graph("course2/test_assignment2/input_random_1_4.txt",testing=True)
G.initialize_shortest_path(1)
explored = [False for n in range(G.num_verticies+1)]
added_to_heap_by = [-1 for n in range(G.num_verticies+1)]
explored[1] = True

h = Heap(num_verticies=G.num_verticies)
added_to_heap_by = add_to_heap(h,G,1,explored,added_to_heap_by)
while len(h) > 0:
    w,length = h.extract_min()
    G.shortest_path.update({w:G.shortest_path[added_to_heap_by[w]]+length})
    print("{}: {}".format(w,length))

    path_to_current = G.paths[added_to_heap_by[w]].copy()
    path_to_current.append(w)
    G.paths.update({w:path_to_current})

    explored[w] = True
    added_to_heap_by = add_to_heap(h,G,w,explored,added_to_heap_by)

for ii,vertex in enumerate(verticies_to_check):
    #assert G.shortest_path[vertex] == G.output[ii]
    print("Vertex {}: {} == {}".format(vertex,G.shortest_path[vertex], G.true_output[ii]))

for ii,vertex in enumerate(verticies_to_check):
    print("Vertex {}: {} == {}\n".format(vertex,G.paths[vertex], G.true_paths[vertex]))