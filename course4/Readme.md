# Course 4: Shortest Paths Revisited, NP-Complete Problems and What To Do About Them

## Week 1 Assignment: Negative length shortest path and all pairs shortest path. Bellman-Ford, Floyd-Warshall, Johnson's
In this assignment we are tasked with solving the all pairs shortest path distance for arbitary graphs. This means that we have to deal with potential negative length edges. One way of doing this is using Floyd-Warshall which looks for the shortest distance between 2 verticies that is at most "i" hops away. This leads to a simple but O(n^3) solution. I found that python just crashed after trying to run the test cases that were 512 verticies. 

Bellman-Ford has the same O(n^3) bound for sparse graphs, but can get upto O(n^4) for dense graphs, so it obviously would not work. This left Johnson's. 

Johnson's is interesting because it takes the generic case and converts it to the special case of no negative edge lengths. It does this by finding the shortest path from some ficticious vertex to every node in the graph which can be used as vertex weights on the edge lengths. When we have no negative edge lengths Dijkstra's can be used and just called for each vertex in the graph.

The result is that the 1 iteration of Bellman-Ford takes longer than running Dijkstra's on all of the verticies combined! This is absolutely nuts! Running time for the assignment ended up being ~150 seconds total for all 3 assignments. The 2048 node test cases take around 150 seconds each to run. 

What is really cool about this algorithm is how it shows to never be satisfied by the obvious and that it might be possible to turn generic cases into special cases which run faster.
