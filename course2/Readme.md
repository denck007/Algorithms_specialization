# Course 2: Graph Search, Shortest Paths, and Data Structures

## Week 1 Assignment: Sizes of Strongly Connected Components (SCC)
Implementation of the recursive form of Kosaraju's 2 pass algorithm. Note that the python stack gets quite large and the algorithm has to be called in a thread with a large stack size. Overall the algorithm is somewhat slow, ~27.2 seconds to complete the assignment. The alogrithm itself takes about 8.9 seconds to run, the rest of the time is spent reading the file, and creating the vertex to edge list (which is done a few times).

## Week 2 Assignment: Dijkstra's Shortest Path algorithm:
Implement Dijkstra's alogrith for shortest path and run report the shortest distances to 5 verticies on a 200 verticex graph. This implenetation also returns the path that gives the shortest path. I had the most trouble with getting the heap implemented and working, once I wrote a function to check the heap for correctness after every operation I quickly found almost all of my issues. This algorithm is extremely fast, all the test cases and assignment take <1 second to run.