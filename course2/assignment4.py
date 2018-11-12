'''
Use a hash table to count the number distinct combinations of values in the input sum to t where t is [-10000,10000] inclusive
'''
import os
import time

def read_data(fname,testing=False):
    with open(fname,'r') as f:
        values = [int(x) for x in f.readlines()]

    if testing:
        fname = fname.replace("input","output")
        with open(fname,'r') as f:
            target = int(f.read().strip("\n"))
        return values,target
    return values


def brute_force_method(fname,testing):
    if testing:
        values,target = read_data(fname,testing)
    else:
        values = read_data(fname)
    for x in values:
        for y in values:
            t = x + y
            if (t >= -10000) and (t <= 10000):
                print("\t{} + {} = {}".format(x,y,t))

#@profile 
def get_distinct_sum_count(fname,testing=False):
    if testing:
        values,target = read_data(fname,testing)
    else:
        values = read_data(fname)
    start_time = time.time()
    table = {}
    values = sorted(values)

    for v in values:
        table[v] = 0
    for t in range(-10000,10001,1):
        print("t: {}          \r".format(t),end = "")
        if t == 0:
            continue
        for x in table.keys():
            if (t-x) in table.keys():
                table[x] += 1
                break
            elif 2*x > 10000:
                break

    distinct_count = 0
    for item in table:
        distinct_count += table[item]

    total_time = time.time()-start_time
    if testing:
        if distinct_count == target:
            print("\tPredicted: {} Expected: {} time: {:3e}".format(distinct_count,target,total_time))
        else:
            print("\t!!!Failed Predicted: {} Expected: {} fname: {} time: {:3e}".format(distinct_count,target,fname,total_time))
    else:
        print("found {} distinct sums in {:.3e} seconds".format(distinct_count,total_time))
base_path = "course2/test_assignment4"

fnames = [os.path.join(base_path,f) for f in os.listdir(base_path) if "input" in f]
for fname in fnames:
    print("Working on {}".format(fname))
    get_distinct_sum_count(fname,testing=True)

print("Starting final problem...")
get_distinct_sum_count("course2/assignment4_input.txt")
