# Course 2: Greedy Algorithms, Minimum Spanning Trees, and Dynamic Programming
I have found that it is really useful to keep a few data structures around, so I am starting to build up a little 'helpers' library.

## Week 1 Assignment: Greedy algorithms. Scheduling, minimum spanning trees, and Prim's algorithm
Implemented a greedy algorithm for scheduling jobs. Used 2 different cost functions, weight-length and weight/length. The weight/length is gaurenteed to be correct, but supprisingly the weight-length method did better than I expected it to and was only off by 2.6%. Obviously this error will not transfer to other problems, but iteresting that they are so similar on a random data set.

Implemented Prim's algorithm to find a minimum spanning tree. I actually thought this was pretty straight forward and really does not take much code to create. The main loop is really tight, and the loop over all the edges connected to a vertex is really straight forward. I ended up making some minor changes to my Heap data structure, to make comparisions simpler but it really only changed what the lists are initialized to.