# Course 2: Graph Search, Shortest Paths, and Data Structures

## Week 1 Assignment: Sizes of Strongly Connected Components (SCC)
Implementation of the recursive form of Kosaraju's 2 pass algorithm. Note that the python stack gets quite large and the algorithm has to be called in a thread with a large stack size. Overall the algorithm is somewhat slow, ~27.2 seconds to complete the assignment. The alogrithm itself takes about 8.9 seconds to run, the rest of the time is spent reading the file, and creating the vertex to edge list (which is done a few times).

## Week 2 Assignment: Dijkstra's Shortest Path algorithm:
Implement Dijkstra's alogrith for shortest path and run report the shortest distances to 5 verticies on a 200 verticex graph. This implenetation also returns the path that gives the shortest path. I had the most trouble with getting the heap implemented and working, once I wrote a function to check the heap for correctness after every operation I quickly found almost all of my issues. This algorithm is extremely fast, all the test cases and assignment take <1 second to run.

## Week 3 Assignment: Median Maintenance
Implement median maintenance using 2 heaps. I implemented this using the same heap data structure as last week using a dummy value for the vertex and multipling the values in the lower heap by -1. This meant that I only had to write the logic of what heap to add to. I made it so that the medain value is always the max value on the lower heap which made it very easy to handle. Overall I only had to add 1 method to the heap function, read_min(). This was purely to make the code faster as it did not have to do O(log(n)) for delete() and O(log(n)) for insert() whenever we just need to read/compare to the minimum value of the heap.