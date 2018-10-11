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
import os
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
        self.data = [int(x.strip("\n")) for x in data]

    def sort(self,start,stop):
        '''
        do an iteration of quicksort on self.data from index start to stop
        returns the number of comparisions done between array elements
        '''
        n = stop - start
        if (n==0) or (n == 1): # no comparisions possible
            return
        else:
            self.num_comparisions += n-1 # add in the number of comparisions
            self.choose_pivot(start,stop)
            pivot_value = self.data[start]

            split_idx = start
            for partition_idx in range(start,stop,1):
                if self.data[partition_idx] < pivot_value:
                    split_idx += 1
                    self.swap(partition_idx, split_idx)
                    
            # final step is swap out pivot value
            self.swap(start,split_idx)

            self.sort(start,split_idx)
            self.sort(split_idx+1,stop)

    def choose_pivot(self,start,stop):
        '''
        Select the pivot based on self.pivot_method
        Swaps the selected pivot and the first element to turn all pivot locations into the simple 'first' case
        '''
        if self.pivot_method == "first":
            return
        elif self.pivot_method == "last":
            self.swap(start, stop-1)
            return
        elif self.pivot_method == "median3":
            return None
        else:
            assert False, "Invalid pivot method {}".format(self.pivot_method)

    def swap(self, position1,position2):
        '''
        Swap the values in position1 and position2
        '''
        tmp = self.data[position1]
        self.data[position1] = self.data[position2]
        self.data[position2] = tmp

test_dir = "course1/test_assignment3/"
input_files = [x[6:] for x in os.listdir(test_dir) if x[:5] =="input"]
output_files = [x[7:] for x in os.listdir(test_dir) if x[:6] =="output"]

pivot_methods = ["first","last"]
for fname in input_files:
    #if int(fname[fname.rfind("_")+1:-4]) > 1000:
    #    continue
    print("Starting {}".format(fname))
    with open("{}input_{}".format(test_dir,fname),'r') as f:
        data = [int(x.strip("\n")) for x in f.readlines()]
    with open("{}output_{}".format(test_dir,fname),'r') as f:
        results = [int(x.strip("\n")) for x in f.readlines()]

    for ii,pivot_method in enumerate(pivot_methods):
        
        #if ii==0:
        #    continue
        print("\tStarting {} ".format(pivot_method),end="")
        sorter = quicksort(pivot_method=pivot_method,data_in=data.copy())
        sorter.sort(0,len(data))
        print("Got: {} Expected: {}".format(sorter.num_comparisions,results[ii]))
        #assert sorter.num_comparisions == results[ii],"Failed with pivot_method=={} on file {}\nGot: {} Expected: {}".format(pivot_method,fname,sorter.num_comparisions,results[ii])
        if sorter.num_comparisions != results[ii]:
            print("\tFailed with pivot_method=={} on file {}\n\tGot: {} Expected: {}".format(pivot_method,fname,sorter.num_comparisions,results[ii]))
