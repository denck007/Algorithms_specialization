# Part 1: Divide and Conquer, Sorting and Searching, and Randomized Algorithms

## Week 1 Part 1: Introduction, 'big-O', and Asymptotic Analysis
Implement Karatsuba Multiplication for large integers and multiply 2 64 character integers together

## Week 2 Part 1: Divide-and-conquer basics
Implement an algorithm to count inversions in a large text file. 

## Week 3 Part 1: Quicksort
Implement quick sort using 3 different methods of choosing a pivot:

1) Always using the first element
2) Always using the last element
3) Median of 3 (first, middle, last) element

To do this a class is made that takes in the data and pivot method. It then moves the pivot to the first element of the current sorting area. In the case of median of 3 it actually creates another instance of quicksort to find the median value. This is then recursed on until the entire array is sorted. It is important to watch for pass by reference values in this assignment and it bit me a few times, python can be tricky with this and explicit copy() calls are sometimes needed. 




