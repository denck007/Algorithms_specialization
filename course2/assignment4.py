'''
Use a hash table to count the number distinct combinations of values in the input sum to t where t is [-10000,10000] inclusive
'''
import os


def read_data(fname,testing=False):
    with open(fname,'r') as f:
        values = [int(x) for x in f.readlines()]

    if testing:
        fname = fname.replace("input","output")
        with open(fname,'r') as f:
            target = int(f.read().strip("\n"))

        return values,target
    return values

def get_distinct_sum_count(fname,testing=False):
    if testing:
        values,target = read_data(fname,testing)
    else:
        values = read_data(fname)

    table = {}
    count = [0 for ii in range(20001)]

    for v in values:
        table[v] = 0

    for t in range(-10000,10001,1):
        if t == 0:
            continue
        for v in values:
            if (v-t) in table.keys():
                #table[v] = 1
                count[t] = 1
    distinct_count = 0
    #for item in table:
    #    distinct_count += table[item]
    for item in count:
        distinct_count += item

    if testing:
        if distinct_count == target:
            print("Predicted: {} Expected: {}".format(distinct_count,target))
        else:
            print("Failed Predicted: {} Expected: {} fname: {}".format(distinct_count,target,fname))
    else:
        print("found {} distinct sums".format(distinct_count))

base_path = "course2/test_assignment4"

fnames = [os.path.join(base_path,f) for f in os.listdir(base_path) if "input" in f]
#fnames = [os.path.join(base_path,"input_random_1_10.txt")]
for fname in fnames:
    if int(fname[fname.rfind("_")+1:-4]) >10:
        continue
    get_distinct_sum_count(fname,testing=True)

#get_distinct_sum_count("course2/assignment4_input.txt")

