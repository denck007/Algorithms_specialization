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
        num_comparisions = n-1
        if n == 1:
            return num_comparisions
        else:
            pivot_idx = self.choose_pivot(start,stop)
            pivot_value = self.data[pivot_idx]

            split_idx = start
            for partition_idx in range(start,stop,1):
                if partition_idx == pivot_idx:
                    continue
                if self.data[partition_idx] < pivot_value:
                    # swap
                    tmp = self.data[partition_idx]
                    self.data[partition_idx] = self.data[split_idx]
                    self.data[split_idx] = tmp
                    split_idx += 1
            # final step is swap out pivot value
            self.data[pivot_idx] = self.data[split_idx]
            self.data[split_idx] = pivot_value

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


pt1 = quicksort(pivot_method="first",data_in=[1,0,2])
print(pt1.sort(0,-1))
print(pt1.data)