'''
Course 4, Week2: NP Completeness and the traveling salesman problem


Given the (x,y) coordinates to points in cartesian coordinates, find the shortest cycle between all the points that visits each point only once.
The distance between 2 points is the Euclidean distance between their coordinates.

Output the length of the shortest tour rounded DOWN to the nearest integer

The input file is:
<number of points>
x1 y1
x2 y2
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

        self.num_vertices = int(data[0])
        self.locations = [[float(x) for x in line.split(" ")] for line in data[1:]]

        self.distance = [[((loc1[0]-loc2[0])**2+(loc1[1]-loc2[1])**2)**.5 for loc2 in self.locations] for loc1 in self.locations]

        # a simple way to encode 'infinity'
        # the (impossible) worst case distance is the distance between every node and it's furthest neighbor.
        self.max_distance = 0
        for dist in self.distance:
            self.max_distance += max(dist)

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                data = f.readlines()

            self.soultion = float(data[0])
    
    def plot_locations(self):
        '''
        plot the locations using matplotlib
        '''
        import matplotlib.pyplot as plt

        x = [loc[0] for loc in self.locations]
        y = [loc[1] for loc in self.locations]

        plt.plot(x,y,'*')
        plt.show()

    def _create_subproblem_set_list(self):
        '''
        At the outter level of the algorithm we are growing the number of vertices that are in the the subproblem set
        This function build up a list lists for the integers that represent the sub problems
        We are using the bits of an integer to indicate which vertices are in the set
        This creates lists of integers (subproblem sets) that are indexed by the number of vertices in the set
            ie the number of '1' bits in the int
        EX:
            5 = b'0101' indicates vertice 1 and 3 are in the solution set
        For this problem we also only care about solutions that have vertex 1 in them, so only want odd integers
        '''
        self.subproblem_sets = [[] for _ in range(self.num_vertices+1)]
        for ii in range(1,2**self.num_vertices,2): # only care about sets that have first item in them
            if ii%10000 == 1:
                print("\tMaking subproblem set list, on item {}/{}".format(ii,2**self.num_vertices),end="\r",flush=True)
            number_of_vertice_in_subproblem= "{:0{prec}b}".format(ii,prec=self.num_vertices).count("1")
            self.subproblem_sets[number_of_vertice_in_subproblem].append(ii)
            #print("{:2d}: {:0{prec}b} {}".format(ii,ii,number_of_vertice_in_subproblem,prec=self.num_vertices))

    def tsp(self):
        '''
        solve the traveling salesman problem
        '''
        self._create_subproblem_set_list()
        self.A = [[self.max_distance for _ in range(self.num_vertices)] for _ in range(2**(self.num_vertices))]
        self.A[1][0] = 0
        
        total_number_of_problems = (2**self.num_vertices)/2
        current_problem = 0 # only used for display
        start_time = time.time()
        for m,subproblem_sets in enumerate(self.subproblem_sets[2:]):
            for S_idx,S in enumerate(subproblem_sets):
                # update problem counter and display progress if needed
                current_problem += 1
                if S_idx%2000 == 1:
                    complete = current_problem/total_number_of_problems*100
                    remaining_time = (time.time()-start_time)/(complete/100) - (time.time()-start_time)
                    print("\tCompleted{:5.1f}% of overall problems. Completed {:5.1f}% subproblems of size {:2d}. {:.1f}s remaining".format(complete,S_idx/len(subproblem_sets)*100,m+2,remaining_time),end="\r",flush=True)

                for j_power in range(1,self.num_vertices): # j!=1
                    j = 2**j_power

                    # test to see if j is in this set
                    # j will only have 1 bit set to 1.
                    # if S and j have no bits in common then j is not in S and the value will be 0
                    if (S&j) == 0: 
                        continue
                    S_no_j = S-j # onyl works when j has only 1 bit on
                    for k in range(self.num_vertices):
                        if j_power == k:
                            continue
                        c_jk = self.distance[j_power][k]
                        new_value = self.A[S_no_j][k] + c_jk
                        self.A[S][j_power] = min(self.A[S][j_power],new_value)

        S = 2**self.num_vertices-1
        min_distance = self.max_distance
        for j in range(1,self.num_vertices):
            min_distance = min(min_distance,self.A[S][j]+self.distance[j][0])

        print()
        return min_distance
        

base_path = "course4/test_assignment2"
for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    if "float" not in fname: #ignore the integer test cases
        continue
    if int(fname[fname.rfind("_")+1:-4]) > 6: # only test on short problems
        continue

    print("{}".format(fname),flush=True)
    start_time = time.time()
    tsp = TSP(os.path.join(base_path,fname),testing=True)
    #tsp.plot_locations()
    min_distance = tsp.tsp()
    elapsed_time = time.time()-start_time
    time_per_vert = elapsed_time/tsp.num_vertices
    if tsp.soultion == math.floor(min_distance):
        print("\tCorrect, min_distance is {:5.0f}\n\telapsed: {:.3f} time/vert: {:.3f}".format(tsp.soultion,elapsed_time,time_per_vert))
    else:
        print("! ! ! Incorrect Got: {:.3f} expected {:.3f}\n\telapsed: {:.3f} time/vert: {:.3f}".format(min_distance,tsp.soultion,elapsed_time,time_per_vert))

print("\n\nStarting on assignment\n")
base_path = "course4"
fname = "assignment2_input.txt"
start_time = time.time()
tsp = TSP(os.path.join(base_path,fname),testing=False)
min_distance = math.floor(tsp.tsp())
elapsed_time = time.time()-start_time
time_per_vert = elapsed_time/tsp.num_vertices
print("Assignment min_distance is {:5.0f} elapsed: {:.3f} time/vert: {:.3f}".format(min_distance,elapsed_time,time_per_vert))


