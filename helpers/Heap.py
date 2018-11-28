class Heap():
    '''
    The underlying data is stored in python lists.
    There are 2 lists: the keys which are the distances from id s to w and the 
    '''

    def __init__(self,num_ids):
        '''
        num_verticies are the total number of ids to track
        '''
        self.null_cost = int(1e10) # theoretical max value
        
        self.num_ids = num_ids
        # the max number of items that we can ever see is the number of ids to track
        # Add 1 to this so that we can deal with 1 based id numbers in id_heap
        # Add an additional 1 to this so that when we bubble down and try to compare off the end of the heap, we can redirect them to the 
        #   a value that is gaurentteed to never have an associated id and thus never have a length less than null_cost
        self.max_heap_size = num_ids+2 

        self.heap = [self.null_cost for n in range(self.max_heap_size)]
        self.heap_id = [-1 for n in range(self.max_heap_size)]
        self.id_heap = [-1 for n in range(self.max_heap_size)]
        self.end_of_heap = 0 # the index in self.heap of the first item not included, ie the index where an item can be inserted

    def extract_min(self):
        '''
        Remove the minimum key value from the heap, return (id,length)
        '''
        id = self.heap_id[0]
        length = self.delete(id)
        #self.check_heap("extract_min")
        return (id,length)

    def insert(self,id,length):
        '''
        Add the length to id to the heap
        '''
        self.heap[self.end_of_heap] = length
        self.heap_id[self.end_of_heap] = id
        self.id_heap[id] = self.end_of_heap
        if self.end_of_heap > 0:
            self._bubble_up(self.end_of_heap)
        self.end_of_heap += 1
        #self.check_heap("insert")

    def delete(self,id):
        '''
        remove everything associated with id from the heap
        return the length for id
        '''
        heap_idx = self.id_heap[id]
        length = self.heap[heap_idx]

        self._swap(heap_idx,self.end_of_heap-1) #move value to be deleted to end of array
        self.end_of_heap -= 1 # move the end of the heap marker
        self.heap[self.end_of_heap] = self.null_cost+3
        self._bubble_down(heap_idx)
        self._bubble_up(heap_idx)
        #self.check_heap("delete")

        return length

    def view_min(self):
        '''
        return the (id,length) for the minimum value on the heap
        This does not remove the id from the heap
        '''
        id = self.heap_id[0]
        length = self.heap[0]
        return (id,length)

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
        
        tmp = self.id_heap[self.heap_id[source_idx]]
        self.id_heap[self.heap_id[source_idx]] = self.id_heap[self.heap_id[destination_idx]]
        self.id_heap[self.heap_id[destination_idx]] = tmp
        
        tmp = self.heap_id[source_idx]
        self.heap_id[source_idx] = self.heap_id[destination_idx]
        self.heap_id[destination_idx] = tmp

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
