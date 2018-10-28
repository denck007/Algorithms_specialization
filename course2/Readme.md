# Course 2: Graph Search, Shortest Paths, and Data Structures

## Week 1 Assignment: Sizes of Strongly Connected Components (SCC)
Implementation of the recursive form of Kosaraju's 2 pass algorithm. Note that the python stack gets quite large and the algorithm has to be called in a thread with a large stack size. Overall the algorithm is somewhat slow, ~27.2 seconds to complete the assignment. The alogrithm itself takes about 8.9 seconds to run, the rest of the time is spent reading the file, and creating the vertex to edge list (which is done a few times).