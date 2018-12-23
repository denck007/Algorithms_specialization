'''
Course 4, Week1: The Bellman-Ford algorithm; all-pairs shortest paths


Given an input graph that has real valued edge lengths and potentially negative cycles, compute the all pairs shortest path in the graph.

The actual assignment gives 3 graphs, and we are to compute the APSP for each, and submit the shortest shortest path from the 3 graphs.
If they all have negative cycles then we submitt NULL

Input files have structure:
num_verticies num_edges
tail_vertex head_vertex edge_length


The solution will need to have mechanism for checking for negative cycles
    Running bellman-ford for 1 extra iteration and looking for a decrease in shortest path
    So floyd-warshall and check the diagonal for values < 0 would be viable


'''

import os

class APSP():

    def __init__(self,fname,testing=False):
        '''
        Read in a graph from fname and read in the solution if we are testing
        '''

        self.fname = fname
        self.testing = testing

        with open(fname,'r') as f:
            data = f.readlines()

        self.num_verticies = int(data[0].split()[0])
        self.num_edges = int(data[0].split()[1])
        
        
        self.edge_verticies = [] # the [tail,head] of the edge
        self.vertex_edges = [[] for _ in range(self.num_verticies+1)] # all of the edges that go into a vertex
        self.edge_length = []

        self.longest_path = 0 # the sum of absolute value of every length in the graph, used as infinity

        for e,line in enumerate(data[1:]):
            u,v,length = line.strip().split()
            u = int(u)
            v = int(v)
            length = int(length)
            self.longest_path += abs(length)
            self.edge_verticies.append([u,v])
            self.edge_length.append(length)
            self.vertex_edges[v].append(e)


        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                data = f.readlines()[0].strip()
            
            if data == "NULL":
                self.solution = "NULL"
            else:
                self.solution = int(data)
            
            fname = fname.replace("output","path")
            with open(fname,'r') as f:
                data = f.readlines()[0].strip()
            
            data = data.replace("[","").replace("]","")
            if data == "null":
                self.solution_path = "NULL"
            else:
                self.solution_path = [int(v) for v in data.split(",")]

    #@profile
    def FloydWarshall(self):
        '''
        Run the Floyd-Warshall algorithm to find shortest path between every vertex in the graph
        '''

        #Initialize with postitive infinity
        self.A = [[[self.longest_path for k in range(self.num_verticies+1)] for j in range(self.num_verticies+1)] for i in range(self.num_verticies+1)]
        # self loops to 0
        for i in range(self.num_verticies+1):
            self.A[i][i][0] = 0
        #edges in G to their corresponding weight
        for idx,length in enumerate(self.edge_length):
            u = self.edge_verticies[idx][0]
            v = self.edge_verticies[idx][1]
            self.A[u][v][0] = min(length,self.A[u][v][0])

        self.shortest_path = self.longest_path

        for k in range(1,self.num_verticies+1):
            for i in range(1,self.num_verticies+1):
                for j in range(1,self.num_verticies+1):
                    case1 = self.A[i][j][k-1]
                    case2 = self.A[i][k][k-1] + self.A[k][j][k-1]
                    self.A[i][j][k] = min(case1,case2)
                    self.shortest_path = min(self.shortest_path,self.A[i][j][k])

        self.found_negative_loop = False
        self.vertices_in_negative_loop = []
        for i in range(self.num_verticies+1):
            if self.A[i][i][-1] < 0:
                self.found_negative_loop = True
                self.vertices_in_negative_loop.append(i)

        if self.found_negative_loop:
            return "NULL"
        else:
            return self.shortest_path


    def BellmanFord(self,s):
        '''
        Runs the Bellman-Ford algorithm for 1 source vertex, s 
        '''
        #Initialize with postitive infinity
        self.A = [[self.longest_path for v in range(self.num_verticies+1)] for i in range(self.num_verticies+1)]
        self.A[0,s] = 0

        #for i in range(self.num_verticies):
            #for v in self.vertex_edges[]

base_path = "course4/test_assignment1"
fname = "input_random_2_2.txt"

for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    n = fname[fname.rfind("_")+1:-4]
    if int(n) > 100:
        continue
    print("{:25s} ".format(fname),end="")
    apsp = APSP(os.path.join(base_path,fname),testing=True)
    shortest_path = apsp.FloydWarshall()
    if shortest_path == apsp.solution:
        print("Correct! Got {}".format(shortest_path))
    else:
        print("WRONG! Got {} expected {}".format(shortest_path,apsp.solution))


print("Starting Assignment!")
base_path = "course4/"
fnames = ["assignment1_input1.txt","assignment1_input2.txt","assignment1_input3.txt"]
shortest_path = [0 for _ in fnames]
for idx,fname in enumerate(fnames):
    apsp = APSP(os.path.join(base_path,fname),testing=False)
    shortest_path[idx] = apsp.FloydWarshall()

    print("{}: shortest path: {}".format(fname,shortest_path[idx]))