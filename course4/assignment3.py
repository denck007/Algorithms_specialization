'''
Course 4, Week3: NP Completeness and the traveling salesman problem using greed hueristic


Given the (x,y) coordinates to points in cartesian coordinates, find the shortest cycle between all the points that visits each point only once.
The distance between 2 points is the Euclidean distance between their coordinates.

Output the length of the shortest tour rounded DOWN to the nearest integer

Use the greedy nearest-neighbor criteria for selecting the next city in the tour:
1. Start the tour at the first city.
2. Repeatedly visit the closest city that the tour hasn't visited yet. In case of a tie, go to the closest city with the lowest index. For example, if both the third and fifth cities have the same distance from the first city (and are closer than any other city), then the tour should begin by going from the first city to the third city.
3. Once every city has been visited exactly once, return to the first city to complete the tour.

The input file is:
<number of points>
city_number x1 y1
city_number x2 y2
...

'''
import os
import math # only used for floor function
import time
import sys

class TSP():
    '''
    Class for solving traveling salesman problems
    '''
    def __init__(self,fname,testing=False):
        '''
        Read in the x,y coordinates listed in fname. Read in the correct solution if testing
        '''
        self.fname = fname
        self.testing = testing

        self.locations = []
        with open(fname,'r') as f:
            data = f.readlines()

        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0

        self.num_verticies = int(data[0])
        self.locations = {}
        for line in data[1:]:
            vertex_data = line.split(" ")
            vertex = int(vertex_data[0])
            x = float(vertex_data[1])
            y = float(vertex_data[2])
            self.locations[vertex] = [x,y]
            min_x = min(min_x,x)
            max_x = max(max_x,x)
            min_y = min(min_y,y)
            max_y = max(max_y,y)

        # simple way to encode infinity
        # the maximum distance between 2 verticies is the minx,miny vertex to maxx,maxy vertex
        #    This is an over estimate of the largest possible distance, but is very simple to compute and gaurenteed upper bound
        #    This is acutally the largest bounding rectangle for the dataset, ie all vertices are inside these points
        # so the maximum distance of a path through the graph must be less than the number of nodes * this distance
        self.max_distance = self.num_verticies*(((min_x-max_x)**2+(min_y+max_y)**2)**.5)

        # get the verticies in order of increasing x value
        # this will let us easily iterate over closest locations
        self.sorted_x = sorted(self.locations,key=lambda loc: self.locations[loc][0])

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                data = f.readlines()
            self.soultion = float(data[0])

    def tsp_nn(self):
        '''
        Solve the TSP problem using the nearest neighbor greedy criterion
        Idea is to only calculate the distance for the closest possible verticies.
        Iterate through by the sorted_x_locations
        '''
        self.path = {1:0.0} #keys are nodes, values are distance to node, in python 3.5+ addition order is gaurenteed
        self.cumulative_distance = 0.0
        x = self.locations[1][0]
        y = self.locations[1][1]
        

        # current_sorted_x_location =  location of node 1 in sorted_x
        for idx,key in enumerate(self.sorted_x):
            if key == 1:
                current_end_in_sorted_x_location = idx


        # next_ variables hold the current best choice for the next addition to the path
        # prospect_ variables are what we are currently testing to see if they should be moved to next_

        # Go over all of the verticies
        current_end_vertex = 1
        next_end = None
        while len(self.path) < self.num_verticies:
            next_distance = self.max_distance
            current_x = self.locations[current_end_vertex][0]
            current_y = self.locations[current_end_vertex][1]

            for proposed_end_in_sorted_x_location in range(current_end_in_sorted_x_location-1,-1,-1):
                proposed_vertex = self.sorted_x[proposed_end_in_sorted_x_location]
                
                # if we have already visited the path, skip to next possible value
                if proposed_vertex in self.path:
                    continue

                proposed_x = self.locations[proposed_vertex][0]
                proposed_y = self.locations[proposed_vertex][1]
                proposed_distance = ((current_x-proposed_x)**2 + (current_y-proposed_y)**2)**0.5

                if abs(current_x-proposed_x) > next_distance:
                    # have moved far enough away from current that no value of y could give a better solution than next_distance
                    break
                elif proposed_distance == next_distance:
                    # if the distances are the same use the city with the lower id
                    if proposed_vertex < next_end:
                        next_distance = proposed_distance
                        next_end = proposed_vertex
                        next_end_in_sorted_x_location = proposed_end_in_sorted_x_location
                elif proposed_distance < next_distance:
                    next_distance = proposed_distance
                    next_end = proposed_vertex
                    next_end_in_sorted_x_location = proposed_end_in_sorted_x_location

            for proposed_end_in_sorted_x_location in range(current_end_in_sorted_x_location+1,self.num_verticies,1):
                proposed_vertex = self.sorted_x[proposed_end_in_sorted_x_location]

                # if we have already visited the path, skip to next possible value
                if proposed_vertex in self.path:
                    continue

                proposed_x = self.locations[proposed_vertex][0]
                proposed_y = self.locations[proposed_vertex][1]
                proposed_distance = ((current_x-proposed_x)**2 + (current_y-proposed_y)**2)**0.5

                if abs(current_x-proposed_x) > next_distance:
                    # have moved far enough away from current that no value of y could give a better solution than next_distance
                    break
                elif proposed_distance == next_distance:
                    # if the distances are the same use the city with the lower id
                    if proposed_vertex < next_end:
                        next_distance = proposed_distance
                        next_end = proposed_vertex
                        next_end_in_sorted_x_location = proposed_end_in_sorted_x_location
                elif proposed_distance < next_distance:
                    next_distance = proposed_distance
                    next_end = proposed_vertex
                    next_end_in_sorted_x_location = proposed_end_in_sorted_x_location
            
            self.path[next_end] = next_distance
            self.cumulative_distance += next_distance
            current_end_vertex = next_end
            current_end_in_sorted_x_location = next_end_in_sorted_x_location

        back_to_start = ((self.locations[current_end_vertex][0]-self.locations[1][0])**2 + (self.locations[current_end_vertex][1]-self.locations[1][1])**2)**0.5
        self.path["back_to_start"] = back_to_start
        self.cumulative_distance += back_to_start

        return self.cumulative_distance


base_path = "course4/test_assignment3"
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    #if int(fname[fname.rfind("_")+1:-4]) > 6: # only test on short problems
    #    continue
    #if fname != "input_simple_5_4.txt":
    #    continue

    print("{}".format(fname),flush=True)
    start_time = time.time()
    tsp = TSP(os.path.join(base_path,fname),testing=True)
    min_distance = tsp.tsp_nn()
    elapsed_time = time.time()-start_time
    time_per_vert = elapsed_time/tsp.num_verticies
    if tsp.soultion == math.floor(min_distance):
        print("\tCorrect, min_distance is {:5.0f}\n\telapsed: {:.3f} time/vert: {:.3f}".format(tsp.soultion,elapsed_time,time_per_vert))
    else:
        print("------\n! ! ! Incorrect Got: {:.3f} expected {:.3f}\n\telapsed: {:.3f} time/vert: {:.3f}\n------".format(min_distance,tsp.soultion,elapsed_time,time_per_vert))

print("\n\nStarting assignment!")
base_path = "course4"
fname = "assignment3_input.txt"
start_time = time.time()
tsp = TSP(os.path.join(base_path,fname),testing=False)
min_distance = tsp.tsp_nn()
elapsed_time = time.time()-start_time
time_per_vert = elapsed_time/tsp.num_verticies
print("\tPredicted distance is {:5.3f}\n\telapsed: {:.3f} time/vert: {:.3f}".format(min_distance,elapsed_time,time_per_vert))

print("First 50 cities:")
cumulative = 0.0

to_show = list(range(0,51))
to_show.extend([999,1000,1001,33707,33708])

for idx,key in enumerate(tsp.path):
    cumulative += tsp.path[key]
    if idx in to_show:
        print("idx: {:5d} City: {:5} Previous to Current: {:10.3f} Cumulative: {:10.3f}".format(idx,key,tsp.path[key],cumulative))


