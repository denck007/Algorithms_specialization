# Course 2: Greedy Algorithms, Minimum Spanning Trees, and Dynamic Programming
I have found that it is really useful to keep a few data structures around, so I am starting to build up a little 'helpers' library.

## Week 1 Assignment: Greedy algorithms. Scheduling, minimum spanning trees, and Prim's algorithm
Implemented a greedy algorithm for scheduling jobs. Used 2 different cost functions, weight-length and weight/length. The weight/length is gaurenteed to be correct, but supprisingly the weight-length method did better than I expected it to and was only off by 2.6%. Obviously this error will not transfer to other problems, but iteresting that they are so similar on a random data set.

Implemented Prim's algorithm to find a minimum spanning tree. I actually thought this was pretty straight forward and really does not take much code to create. The main loop is really tight, and the loop over all the edges connected to a vertex is really straight forward. I ended up making some minor changes to my Heap data structure, to make comparisions simpler but it really only changed what the lists are initialized to.


## Week 2 Assignment: Kruskal's MST algorithm and applications to clustering
Question 1 is to implement Kruskals algorithm using union find. This was realitivly simple and mostly involved getting the uion find data structure to work properly.

Question 2 of this week was the hardest assignement yet, dealing with hamming distance between verticies. It is fairly easy to develop a working and correct solution, but the simple and obvious one is very slow. It ends up that flipping the problem and instead of looking for locations within a specified distance, modifiying the locations and seeing if the modified location exists is far more efficient. Bit fiddling would have been really helpful here, but I ran out of time. I extended the list object to be able to be hashed by creating a string of the data in the list. This works but is slow-ish, strings are immutable and we have to loop over every dimiension in the location. This ends up adding some large constants to the algorithm. 
