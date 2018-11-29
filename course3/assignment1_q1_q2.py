'''
Course 3, Week1: INtro to greedy algorithms, Assignment 1: Q1 and Q2

Given a listing of positive weights and lengths for jobs, schedul the jobs using 2 different methods

Question 1: Schedule in decreasing order of weight-length
Question 2: Schedule in decreasing order of weight/length

Going to use the heap data structure from course 2 week 2

Go through and add jobs to heap bases on criteria, then extract them all off.
'''
import os
import sys
sys.path.append("/home/neil/Algorithms_specialization")
from helpers.Heap import Heap

def read_data(fname,testing=False):
    '''
    Read in fname, return 2 lists of weights,lengths
    if testing, return 2 additional parameters, the correct solution to q1, and q2
    '''

    with open(fname,'r') as f:
        data = f.readlines()
    weights = [int(x.strip().split(" ")[0]) for x in data[1:]]
    lengths = [int(x.strip().split(" ")[1]) for x in data[1:]]

    if testing:
        fname = fname.replace("input","output")
        with open(fname,'r') as f:
            q1 = int(f.readline())
            q2 = int(f.readline())
        return weights,lengths,q1,q2
    else:
        return weights,lengths

def q1_heap(weights,lengths):
    '''
    make and return the heap for question 1, ordered by -(weight-length)
    '''
    h = Heap(len(weights))
    for job,(w,l) in enumerate(zip(weights,lengths)):
        c = -(w-l) # want to extract max, so opposite
        h.insert(job,c)
        #print("job: {:2} weight:{:2} length:{:2} cost:{:3}".format(job,w,l,c))
    return h

def q2_heap(weights,lengths):
    '''
    make and return the heap for question 2, ordered by -(weight/length)
    '''
    h = Heap(len(weights))
    for job,(w,l) in enumerate(zip(weights,lengths)):
        c = -(w/l) # want to extract max, so opposite
        h.insert(job,c)
        #print("{} {} {}".format(job,w,l))
    return h

def get_sum_weighted_times(h,weights,lengths,elapsed_time=0):
    '''
    Get the sum of weighted completion times for a given heap.
    This handles the cases of matching costs in the heap by choosing the largest weight
    returns elapsed_time,weighted_times
    '''
    weighted_times = 0
    while (len(h) > 0):
        job,cost = h.extract_min()

        next_job,next_cost = h.view_min()
        if cost == next_cost:
            # the current cost matches the next cost
            # when costs match, choose by highest weight
            # create another heap for matching cost items, then get the min values for this new heap
            # it is not possible to have an incorrect order according to the parameters of the assignement because
            #   c=w-l or c=w/l so if c and w match, l is the same.
            matching_heap = Heap(h.max_heap_size)
            matching_heap.insert(job,-weights[job])

            while cost == next_cost:
                job,cost= h.extract_min()
                matching_heap.insert(job,-weights[job])
                next_job,next_cost = h.view_min()
                #print("\tjob:{:3} cost: {:4} weight: {:3} length: {:3} elapsed_time:{:5} weighted_times:{:8}".format(job,cost,weights[job],lengths[job],elapsed_time,weighted_times))
            
            while (len(matching_heap) > 0):
                job,cost = matching_heap.extract_min()
                elapsed_time += lengths[job]
                weighted_times += elapsed_time*weights[job]
        else:
            elapsed_time += lengths[job]
            weighted_times += elapsed_time*weights[job]
            #print("job:{:3} cost: {:4} weight: {:3} length: {:3} elapsed_time:{:5} weighted_times:{:8}".format(job,cost,weights[job],lengths[job],elapsed_time,weighted_times))
    return elapsed_time,weighted_times

    
base_path = "course3/test_assignment1/questions1And2"
fnames = [f for f in os.listdir(base_path) if "input" in f]

for fname in fnames:
    print("{}".format(fname))
    weights,lengths,q1,q2 = read_data(os.path.join(base_path,fname),testing=True)

    h = q1_heap(weights,lengths)
    elapsed_time,weighted_times = get_sum_weighted_times(h,weights,lengths)
    print("\tQ1 test: {} expected: {} got: {}".format(fname,q1,weighted_times))
    if q1 != weighted_times:
        print("ERROR on Q1")
        

    h = q2_heap(weights,lengths)
    elapsed_time,weighted_times = get_sum_weighted_times(h,weights,lengths)

    print("\tQ2 test: {} expected: {} got: {}".format(fnames[0],q2,weighted_times))
    if q2 != weighted_times:
        print("ERROR on Q2")


print("Staring assignment!")
base_path = "course3/"
fname = "assignment1_q1_q2_input.txt"
weights,lengths = read_data(os.path.join(base_path,fname),testing=False)

h = q1_heap(weights,lengths)
elapsed_time,weighted_times = get_sum_weighted_times(h,weights,lengths)
print("\tQ1 result: {} ".format(weighted_times))

h = q2_heap(weights,lengths)
elapsed_time,weighted_times = get_sum_weighted_times(h,weights,lengths)
print("\tQ2 result: {}".format(weighted_times))


