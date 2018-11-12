'''
Instead of using using a hash table, is there a better way to solve this?

What if we sort the values and iterate from each end? 
* Iterate x + y =t while t >= -10000
* This leads to a bunch of recomputed values. ie when x_idx == 1, we have to re compute all the values of y that are greater than t
* Well this ends up being ~O(n**2) time.

What if we iterate from x in order, but once t <-10000, start to increment the y_idx value back up until values[x_idx+1] + values[y_idx] > 10000?
* If the data is spread out, ie the average value between neighboring value in values is on the same order of magnitude as our range of t
    this will mean that in ~10 increases of y_idx the value of t is > 10000

y_idx = num items in values
for x_idx,idx in enumerate(value): O(n)

    The first time this loop runs, it has the potential to be O(n) or so
    But, if the average 
    while y_idx > x_idx: # eliminate double compute and x==y
        t = values[x_idx] + values[y_idx]
        if t <= 10000 and t >= -10000:
            t_values[t] = 1 # do not increment it

            if (sign of x is negative and t < -10001) or (sign of x is positive and t > 10001):
                while values[x_idx+1] +values[y_idx+1] < 10001:
                    y_idx += 1




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
    values = sorted(values)

    num_values = len(values)-1
    t_count = [0 for ii in range(20001)]

    y_idx = num_values
    for x_idx,x in enumerate(values): # O(n)
        y_idx = min(y_idx,num_values) # O(1)

        # The first loop of this, the running time could be really bad, on order of O(n)
        # But if we assume that the difference between any 2 values in the sorted array is dv and the size of the range of t is dt,
        #   Then on average the following iterations of the loop will run on the order of O(dt/dv). So instead of a double loop over 
        #   value with O(n**2) we end up with small loop in the main loop that gives us O(dt/dv*n). So if dt/dv is quite small, then 
        #   this running time is linear! But if the t range is huge, and the values are close together, we get O(n**2)
        while y_idx > x_idx: # first iteration can be on order of O(n), with same argmunet as below, O(<10) on average
            t = x + values[y_idx] # O(1)
            if (t >= -10000) and (t <= 10000): #O(1)
                t_count[t+10000] = 1 #O(1)
            if (x < 0) and (t < -10001): #O(1)

                # Using the same logic as above, this loop will run ~dt/dv times
                while (values[x_idx+1] + values[y_idx]) <10001: 
                    y_idx += 1
                    if y_idx >= num_values:
                        break
                break
            elif (x>0) and (t > 10001):
                while (values[x_idx+1] + values[y_idx]) <10001:
                    y_idx += 1
                    if y_idx >= num_values:
                        break
                break
            y_idx -= 1

    distinct_count = sum(t_count)

    total_time = time.time()-start_time
    predicted_time_linear = total_time/num_values*1e6
    if testing:
        if distinct_count == target:
            print("\tPredicted: {} Expected: {} time: {:3e},predicted time: {:.1f} seconds".format(distinct_count,target,total_time,predicted_time_linear))
        else:
            print("\t!!!Failed Predicted: {} Expected: {} fname: {} time: {:.3e},predicted time: {:.1f} seconds".format(distinct_count,target,fname,total_time,predicted_time_linear))
    else:
        print("found {} distinct sums in {:.3e} seconds".format(distinct_count,total_time))
base_path = "course2/test_assignment4"

fnames = [os.path.join(base_path,f) for f in os.listdir(base_path) if "input" in f]
for fname in fnames:
    print("Working on {}".format(fname))
    get_distinct_sum_count(fname,testing=True)


print("Starting final problem...")
get_distinct_sum_count("course2/assignment4_input.txt")

