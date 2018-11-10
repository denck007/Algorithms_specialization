'''
Use a hash table to count the number distinct combinations of values in the input sum to t where t is [-10000,10000] inclusive
'''
import os

table = {}
count = [0 for ii in range(20001)]

def read_data(fname,testing=False):
    with open(fname,'r') as f:
        values = [int(x) for x in f.readlines()]

    if testing:
        fname = fname.replace("input","output")
        with open(fname,'r') as f:
            target = int(f.read().strip("\n"))

        return values,target
    return target

def get_distinct_sum_count(fname,testing=False):
    if testing:
        values,target = read_data(fname,testing)
    else:
        values = read_data(fname)

    for v in values:
        table[v] = 1

    for t in range(-10000,10001,1):
        for v in values:
            if v-t in table.keys():
                count[t+10000] += 1

    distinct_count = 0
    for t in count:
        if t == 1:
            distinct_count += 1
    
    if testing:
        print("Predicted: {} Expected: {}".format(distinct_count,target))
        if distinct_count != target:
            print("FAILED on {}".format(fname))
    else:
        print("found {} distinct sums".format(distinct_count))

base_path = "course2/test_assignment4"

fnames = [os.path.join(base_path,f) for f in os.listdir(base_path) if "input" in f]

for fname in fnames:
    get_distinct_sum_count(fname,testing=True)

get_distinct_sum_count("course2/assignment4_input.txt")

