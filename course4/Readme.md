# Course 4: Shortest Paths Revisited, NP-Complete Problems and What To Do About Them

## Week 1 Assignment: Negative length shortest path and all pairs shortest path. Bellman-Ford, Floyd-Warshall, Johnson's
In this assignment we are tasked with solving the all pairs shortest path distance for arbitary graphs. This means that we have to deal with potential negative length edges. One way of doing this is using Floyd-Warshall which looks for the shortest distance between 2 verticies that is at most "i" hops away. This leads to a simple but O(n^3) solution. I found that python just crashed after trying to run the test cases that were 512 verticies. 

Bellman-Ford has the same O(n^3) bound for sparse graphs, but can get upto O(n^4) for dense graphs, so it obviously would not work. This left Johnson's. 

Johnson's is interesting because it takes the generic case and converts it to the special case of no negative edge lengths. It does this by finding the shortest path from some ficticious vertex to every node in the graph which can be used as vertex weights on the edge lengths. When we have no negative edge lengths Dijkstra's can be used and just called for each vertex in the graph.

The result is that the 1 iteration of Bellman-Ford takes longer than running Dijkstra's on all of the verticies combined! This is absolutely nuts! Running time for the assignment ended up being ~150 seconds total for all 3 assignments. The 2048 node test cases take around 150 seconds each to run. 

I did a comparision between Floyd-Warshall, Bellman-Ford, and Johnson using the test cases with 128 and less verticies. The compute time for each was: Floyd-Warshall 7.9s, Bellman-Ford 15.0s, Johnson 0.5s. Running a profiler on the code shows that in Johnson's on the test cases the 1 iteration of Bellman-Ford takes 50%+ of the solve time and running all iterations of Dijkstra's takes ~43%. 

What is really cool about this algorithm is how it shows to never be satisfied by the obvious and that it might be possible to turn generic cases into special cases which run faster.


## Week2 Assignment: Traveling Salesman
This assignment solves the classic traveling salesman problem. We are given cartesian coordinates for 25 cities and asked to compute the shortest path between all the cities that forms a loop and never visits the same city twice. I took a fairly naive approach to coding this up, and as a result it is fairly slow and uses tons of memory. Total solve time on the 25 city version is 2262seconds, with ~16seconds of pre-processing to generate the codes for tracking what cities have been visited. total memory useage was on the order of 13gigs.

To track all the combinations of visited cities I used integers where each bit of the integer represents a city. so the lowest bit being 1 means we visted city 1. As we start from city 1, and the algorithm explicitly ignores all visits to city 1 (for each j in set S where j!=1) we do not need to do any searching on subsets where bit 1 is 0, so we can ignore all even numbers. We need to go through the subproblems in increasing size, so we create a list of lists where the outer index is the subproblem size, and the inner lists are the integers with the number of 1 bits == subproblem size.

Then we create a 2D array of size 2**num_cities x num_cities. Iterate over the subproblem sets (in increasing order of cities included) looking for shorter distances between the group of cites (less 1 city) and every other city. Here we could easily use ~ 1/2 as much memory. The 2D array that stores the minimum distance between a set of cities includes even numbers. Because we are starting from city 1, rows with even IDs are never updated. 

