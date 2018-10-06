'''
Algorithms Divide and Conquer
Week 3
Programming assignment 3
Quicksort

Track the number of comparisions (m-1 for each recursion) for various methods of choosing a pivot value
Part1: Always choose first element
Part2: Always choose last element
Part3: Use median of 3 rule, ie for {8 2 4 5 7 1}, evaluate on set {8,4,1} and use 4 as the pivot

Input is assignment3_input.txt

Going to implement a generic load and sort function that calls different choose pivot values

Todo:
[ ]: Load data in
[ ]: Recurse over all data 
[ ]: Choose first element as pivot
[ ]: Choose last element
[ ]: Meidan of 3 rule
'''

class quicksort(object):
    def __init__(self,pivot_method,data_in="part1/assignment3_input.txt"):
        '''
        pivot method is string that specifies how to choose the pivot:
            - first
            - last
            - median3
        '''
        self.pivot_method = pivot_method

        if type(data_in) is str:
            self.load_data(data_in)
        elif type(data_in) is list:
            self.data = data_in
        else:
            assert False, "Invalid input data type!"
        
        self.num_comparisions = 0

    def load_data(self,fname):
        '''
        load the data into the instances data list as ints
        '''
        with open(fname,'r') as f:
            data = f.readlines()
        self.data = [int(x) for x in data]

    def sort(self,start,stop):
        '''
        do an iteration of quicksort on self.data from index start to stop
        returns the number of comparisions done between array elements
        '''
        n = stop - start
        if (n==0) or (n == 1): # no comparisions to add
            return
        else:
            self.num_comparisions += n-1 # add in the number of comparisions
            pivot_idx = self.choose_pivot(start,stop)
            pivot_value = self.data[pivot_idx]

            split_idx = start
            for partition_idx in range(start,stop,1):
                #if partition_idx == split_idx:
                #    continue
                if self.data[partition_idx] < pivot_value:
                    # swap
                    tmp = self.data[partition_idx]
                    self.data[partition_idx] = self.data[split_idx]
                    self.data[split_idx] = tmp
                    split_idx += 1
            # final step is swap out pivot value
            self.data[pivot_idx] = self.data[split_idx-1]
            self.data[split_idx] = pivot_value

            self.sort(start,split_idx)
            self.sort(split_idx+1,stop)

    def choose_pivot(self,start,stop):
        '''
        return the index of the pivot in the list self.data
        '''
        if self.pivot_method == "first":
            return start
        elif self.pivot_method == "last":
            return stop
        elif self.pivot_method == "median3":
            return None
        else:
            assert False, "Invalid pivot method {}".format(self.pivot_method)


data = [1,0,2]
s = [0,1,2]
comp = 2
pt1 = quicksort(pivot_method="first",data_in=data)
print(pt1.sort(0,len(data)))
print(pt1.data)
print(pt1.num_comparisions)
assert pt1.data == s, "Failed to sort"
assert pt1.num_comparisions == comp, "Failed to get right number of comparisions"

data = [0,1,2]
s = [0,1,2]
comp = 3
pt1 = quicksort(pivot_method="first",data_in=data)
print(pt1.sort(0,len(data)))
print(pt1.data)
print(pt1.num_comparisions)
assert pt1.data == s, "Failed to sort"
assert pt1.num_comparisions == comp, "Failed to get right number of comparisions"

data = [2,1,0]
s = [0,1,2]
comp = 2
pt1 = quicksort(pivot_method="first",data_in=data)
print(pt1.sort(0,len(data)))
print(pt1.data)
print(pt1.num_comparisions)
assert pt1.data == s, "Failed to sort"
assert pt1.num_comparisions == comp, "Failed to get right number of comparisions"