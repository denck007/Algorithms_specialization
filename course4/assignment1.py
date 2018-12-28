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

class Graph():

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
        self.has_negative_edge = False # flag for if the graph contains a negative edge or not
        self.has_negative_cycle = None

        # initialize apsp distances to empty lists
        self.apsp_bellmanford = []
        self.apsp_fw = []
        self.apsp_johnson = []

        # initialize the shortest path between any 2 points in a graph to None        
        self.apsp_fw_shortest = None
        self.apsp_bellmanford_shortest = None
        self.apsp_johnson_shortest = None

        for e,line in enumerate(data[1:]):
            u,v,length = line.strip().split()
            u = int(u)
            v = int(v)
            length = int(length)

            self.longest_path += abs(length)
            self.edge_verticies.append([u,v])
            self.edge_length.append(length)
            self.vertex_edges[v].append(e)
                        
            if length < 0:
                self.has_negative_edge = True

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

    def add_vertex(self):
        '''
        Add a vertex to the graph, return the vertex number
        '''
        self.num_verticies += 1
        return self.num_verticies

    def add_edge(self,u,v,length):
        '''
        add an edge from u to v with length
        '''
        self.num_edges += 1
        self.edge_verticies.append([u,v])
        
        if v == len(self.vertex_edges): # there is not an index for an edge ending at this vertex yet
            self.vertex_edges.append([])
        self.vertex_edges[v].append(self.num_edges-1)

        self.edge_length.append(length)
        self.longest_path += abs(length)

    #@profile
    def FloydWarshall_apsp(self):
        '''
        Run the Floyd-Warshall algorithm to find shortest path between every vertex in the graph
        '''

        #Initialize with postitive infinity
        self.apsp_fw = [[[self.longest_path for k in range(self.num_verticies+1)] for j in range(self.num_verticies+1)] for i in range(self.num_verticies+1)]
        # self loops to 0
        for i in range(self.num_verticies+1):
            self.apsp_fw[i][i][0] = 0
        #edges in G to their corresponding weight
        for idx,length in enumerate(self.edge_length):
            u = self.edge_verticies[idx][0]
            v = self.edge_verticies[idx][1]
            self.apsp_fw[u][v][0] = min(length,self.apsp_fw[u][v][0])

        self.apsp_length = self.longest_path #the length of the shortest path from any s-t path in the graph

        for k in range(1,self.num_verticies+1):
            for i in range(1,self.num_verticies+1):
                for j in range(1,self.num_verticies+1):
                    case1 = self.apsp_fw[i][j][k-1]
                    case2 = self.apsp_fw[i][k][k-1] + self.apsp_fw[k][j][k-1]
                    self.apsp_fw[i][j][k] = min(case1,case2)
                    self.apsp_length = min(self.apsp_length,self.apsp_fw[i][j][k])

        self.vertices_in_negative_loop = []
        for i in range(self.num_verticies+1):
            if self.apsp_fw[i][i][-1] < 0:
                self.has_negative_cycle = True
                self.vertices_in_negative_loop.append(i)

        if self.has_negative_cycle:
            return "NULL"
        else:
            return self.apsp_length

    def BellmanFord(self,s):
        '''
        Runs the Bellman-Ford shortest path algorithm for 1 source vertex, s, to every other vertex in graph
        return the shortest paths from s to each of the other verticies in the graph
        If there is a negative cycle, return NULL
        '''
        #Initialize with postitive infinity
        shortest_path = [[self.longest_path for v in range(self.num_verticies+1)] for i in range(self.num_verticies+2)]
        shortest_path[0][s] = 0

        for i in range(1,len(shortest_path)): # only need to go to n-1 because of 1 based indexing on verticies, but do extra for negative cycle check
            for v in range(1,self.num_verticies+1):
                case1 = shortest_path[i-1][v]
                case2 = case1
                for edge in self.vertex_edges[v]:
                    w = self.edge_verticies[edge][0] # get the start vertex of edge into v
                    c_wv = self.edge_length[edge] # get length of w to v
                    to_w = shortest_path[i-1][w] # get length from s to w
                    case2 = min(case2,to_w+c_wv) # shortest path from s to v in case 2
                    _ = 0
                shortest_path[i][v] = min(case1,case2)

        # check for negative cycle
        # is negative cycle if there is a difference between the last 2 iterations
        self.has_negative_cycle = False
        for s in range(self.num_verticies):
            if shortest_path[-1][s] != shortest_path[-2][s]:
                self.has_negative_cycle = True
                return "NULL"

        return shortest_path[-1] # return the final iteration

    def BellmanFord_apsp(self):
        '''
        Run the Bellman-Ford algorithm for all pairs shortest path on the graph
        Sets the self.apsp_bellmanford array of arrays (distance from s to t)
            Sets to None if there is a negative cycle
        '''

        self.apsp_bellmanford = [] # ends up being nxn array
        shortest_path = self.longest_path

        for s in range(self.num_verticies+1):
            shortest_st = self.BellmanFord(s)
            if shortest_st is "NULL":
                self.apsp_bellmanford = "NULL"
                self.apsp_bellmanford_shortest = "NULL"
                return "NULL"
            else:
                self.apsp_bellmanford.append(shortest_st)
                for distance in shortest_st:
                    shortest_path = min(shortest_path,distance)

        self.apsp_bellmanford_shortest = shortest_path
        return self.apsp_bellmanford

    def Johnson_apsp(self):
        '''
        run Johnson's all pairs shortest path alogrithm on the graph
        This requires making a sub instance of the Graph object with an additional vertex

        If there is a negative cycle return NULL
        '''

        # if we have a negative edge length then need to update the edge lengths using bellman ford
        if self.has_negative_edge:
            # add vertex with edge to every node
            extended_graph = Graph(self.fname,testing=False)
            extended_graph.add_vertex()
            for v in range(self.num_verticies):
                extended_graph.add_edge(self.num_verticies,v,0) # from s to every other vertex
            
            # run bellman ford, the shortest path from s to each vertex is the additive
            #   weight for the corresponding node
            vertex_weights = extended_graph.BellmanFord(extended_graph.num_verticies)
            if vertex_weights is "NULL":
                self.apsp_johnson = "NULL"
                return "NULL"

            # update the edge lengths with the vertex_weights
            for edge in range(self.num_edges):
                u,v = self.edge_verticies[edge]
                self.edge_length[edge] = self.edge_length[edge] + vertex_weights[u] - vertex_weights[v]

        # To find All Pairs Shortest Path run Dijkstra's single source shortest path
        #   from every starting node. 
        # If we have gotten this far it is gaurenteed that there is not a negative cycle
        
        #initialize the storage for APSP distances using the sum(abs(edge_length)),every path is gaurentted to be shorter
        #self.apsp_johnson = [[self.longest_path for t in range(self.num_verticies+1)] for s in range(self.num_verticies+1)]
        self.apsp_johnson = []



        

    def APSP(self,algorithm):
        '''
        run all pairs shortest path alogirthm on the graph using the algorithm listed
        '''

        if algorithm.lower() == "floydwarshall":
            self.FloydWarshall_apsp()
            return self.apsp_fw
        elif algorithm.lower() == "johnson":
            self.Johnson_apsp()


import time

fw_time  = 0.
bf_time = 0.

base_path = "course4/test_assignment1"
fname = "input_random_2_2.txt"

for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    n = fname[fname.rfind("_")+1:-4]
    if int(n) > 100:
        continue
    print("{:25s} ".format(fname))
    graph = Graph(os.path.join(base_path,fname),testing=True)
    
    # Floyd Warshall
    start_time = time.time()
    shortest_path = graph.FloydWarshall_apsp()
    fw_time += time.time()-start_time
    print("\tFloyd-Warshall: ",end="")
    if shortest_path == graph.solution:
        print("Correct! Got {}".format(shortest_path))
    else:
        print("WRONG! Got {} expected {}".format(shortest_path,graph.solution))

    # Bellman-Ford
    start_time = time.time()
    graph.BellmanFord_apsp()
    bf_time += time.time()-start_time   
    shortest_path = graph.apsp_bellmanford_shortest
    print("\tBellman-Ford  : ",end="")
    if shortest_path == graph.solution:
        print("Correct! Got {}".format(shortest_path))
    else:
        print("WRONG! Got {} expected {}".format(shortest_path,graph.solution))
print("\nTiming Results:")
print("Floyd-Warshall: {:5.3f}   Bellmand-Ford: {:5.3f}".format(fw_time,bf_time))
'''
print("Starting Assignment!")
base_path = "course4/"
fnames = ["assignment1_input1.txt","assignment1_input2.txt","assignment1_input3.txt"]
shortest_path = [0 for _ in fnames]
for idx,fname in enumerate(fnames):
    graph = Graph(os.path.join(base_path,fname),testing=False)
    shortest_path[idx] = graph.FloydWarshall_apsp()

    print("{}: shortest path: {}".format(fname,shortest_path[idx]))

'''