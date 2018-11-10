'''
Course 2 Week 3 Assignment: Median Maintenance
Given a stream of numbers track the median value using heaps.

In this case the stream of numbers is a text file being read line by line.
The output of this program is: sum(all median values) mod 10000

Going to leverage the heap data structure from last weeks assignment. 
'''

import os

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
        self.null_cost = int(1e10) # theoretical max value
        
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
        #self.check_heap("extract_min")
        return (vertex,length)

    def read_min(self):
        '''
        Return the min value key from the heap. Do not modify the heap
        '''
        return self.heap[0]

    def insert(self,vertex,length):
        '''
        Add the length to vertex to the heap
        '''
        self.heap[self.end_of_heap] = length
        self.heap_vertex[self.end_of_heap] = vertex
        self.vertex_heap[vertex] = self.end_of_heap
        if self.end_of_heap > 0:
            self._bubble_up(self.end_of_heap)
        self.end_of_heap += 1
        #self.check_heap("insert")

    def delete(self,vertex):
        '''
        remove everything associated with vertex from the heap
        return the length for vertex
        '''
        heap_idx = self.vertex_heap[vertex]
        length = self.heap[heap_idx]

        self._swap(heap_idx,self.end_of_heap-1) #move value to be deleted to end of array
        self.end_of_heap -= 1 # move the end of the heap marker
        self.heap[self.end_of_heap] = self.null_cost+3
        self._bubble_down(heap_idx)
        self._bubble_up(heap_idx)
        #self.check_heap("delete")

        return length

    def _bubble_up(self,change_idx):
        '''
        maintain the invariant that all parents are <= children
        '''
        parent_idx = (change_idx+1)//2 - 1# +1 is for 0 based indexing in self.heap
        if (self.heap[parent_idx] > self.heap[change_idx]) and (change_idx > 0):
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
        if (self.heap[change_idx] > left_length) and (left_idx < self.end_of_heap): 
            self._swap(change_idx,left_idx)
            self._bubble_down(left_idx)
        elif (self.heap[change_idx] > right_length) and (right_idx < self.end_of_heap):
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
        '''
        return how many items are on the heap
        '''
        return self.end_of_heap

    def check_heap(self,call_from):
        '''
        Go through the whole graph and make sure all children are >= parents
        '''
        for ii in range(self.end_of_heap):
            left_idx = ii*2+1
            right_idx = ii*2+2
            if left_idx < self.end_of_heap:
                assert self.heap[left_idx] >= self.heap[ii],'{} Left failed at idx {} with {} and {}'.format(call_from,ii,self.heap[left_idx],self.heap[ii])
            if right_idx < self.end_of_heap:
                assert self.heap[right_idx] >= self.heap[ii],'{} Right failed at idx {} with {} and {}'.format(call_from,ii,self.heap[right_idx],self.heap[ii])
        print("{} heap test passed".format(call_from))


def read_input(fname,testing=False):
    '''
    Read an input file, if testing also read output file

    if not testing expected result is None

    return (list of values, expected result)
    '''

    output = None

    with open(fname,'r') as f:
        input = [int(l) for l in f.readlines()]

    if testing:
        fname = fname.replace("input","output")
        with open(fname,'r') as f:
            output = int(f.readline())

        return (input,output)
    else:
        return (input,output)

def median_maintenance(input):
    '''
    Run the median maintenance algorith using the input as a data stream
    returns the sum(all medians over time)%10000
    '''
    median = None
    median_history = 0
    H1 = Heap(len(input))
    H2 = Heap(len(input))

    counter = -1
    while len(input) > 0:
        counter += 1
        new_value = input.pop(0)

        if new_value > -H1.read_min():
            H2.insert(counter,new_value)
        else:
            H1.insert(counter,-new_value)
        
        if len(H1) > len(H2) +1:
            c,value = H1.extract_min()
            H2.insert(c,-value)
        elif len(H2) > len(H1):
            c,value = H2.extract_min()
            H1.insert(c,-value)
        
        median = -H1.read_min()
        median_history += median
    return median_history%10000
    

base_path = "course2/test_assignment3"
test_cases = [x for x in os.listdir(base_path) if "input" in x]

for fname in test_cases:
    (input,output) = read_input(os.path.join(base_path,fname),testing=True)
    solution = median_maintenance(input)
    print("Solution: {} Expected: {}".format(solution,output))


base_path = "course2"
(input,output) = read_input(os.path.join(base_path,"assignment3_input.txt"),testing=False)
solution = median_maintenance(input)
print("Assignemnt solution: {}".format(solution))
    
