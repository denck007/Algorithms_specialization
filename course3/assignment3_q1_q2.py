'''
Course 3, Week3: Huffman codes and Intro to Dynamic Programming, Assignment 1: Q1 and Q2

Given a listing of symbol weights (counts, probabilities), create a huffman encoding.

The solutions to the questions are the min and max codeword length

Input:
[number_of_symbols]
[weight of symbol #1]
[weight of symbol #2]
...


'''
import os
import sys
sys.path.append("/home/neil/Algorithms_specialization")
from helpers.Heap import Heap

class Huffman():
    '''
    Basic implementation to generate Huffman codes
    '''

    def __init__(self,fname,testing=False):
        '''
        read in the input and optional solution data (if testing)
        '''

        self.fname = fname
        self.testing = testing

        with open(fname,'r') as f:
            data = f.readlines()

        self.num_symbols = int(data[0])
        self.weights = [int(x) for x in data[1:]]
        self.parents = [x for x in range(self.num_symbols)]

        if testing:
            fname = fname.replace("input","output")
            with open(fname,'r') as f:
                data = f.readlines()

            self.solution_1 = int(data[0])
            self.solution_2 = int(data[1])
        
    def generate_code(self):
        '''
        Generate the Huffman code for the dataset
        '''
        self.heap = Heap(self.num_symbols**2) # way overkill and excessive allocation
        for idx,weight in enumerate(self.weights):
            self.heap.insert(idx,weight)
        
        while len(self.heap) > 2:
            p,_ = self.heap.extract_min()
            q,_ = self.heap.extract_min()
            w = self.weights[p] + self.weights[q]

            # add the new node to tracking
            parent_idx = len(self.parents) # note 0 based indexing here
            self.weights.append(w)
            self.parents.append(parent_idx)
            self.parents[p] = parent_idx
            self.parents[q] = parent_idx
            self.heap.insert(parent_idx,w)

    def get_codeword_lengths_range(self):
        '''
        return a tuple of the min and max lengths of the codewords
        '''
        def _get_parent_count(self,idx):
            '''
            return the count to the root node 
            '''
            # basecase is root node
            if idx == self.parents[idx]:
                self.codeword_lengths[idx] = 1
                return 1
            elif self.codeword_lengths[idx] >= 0: # cached value
                return self.codeword_lengths[idx] 
            else:
                count = _get_parent_count(self,self.parents[idx])
            
            self.codeword_lengths[idx] = count +1
            
            return self.codeword_lengths[idx]           


        self.codeword_lengths = [-1 for _ in range(len(self.parents))]

        for idx in range(self.num_symbols):
            self.codeword_lengths[idx] = _get_parent_count(self,idx)

        min_len = self.num_symbols
        max_len = 0

        for idx in range(self.num_symbols):
            min_len = min(min_len,self.codeword_lengths[idx])
            max_len = max(max_len,self.codeword_lengths[idx])          

        return (min_len,max_len)




base_path = "course3/test_assignment3/question1And2"
fname = "input_random_2_10.txt"

for fname in os.listdir(base_path):
    if "input" not in fname:
        continue
    print(fname,end="")
    huffman = Huffman(os.path.join(base_path,fname),testing=True)
    huffman.generate_code()
    min_len,max_len = huffman.get_codeword_lengths_range()
    if (min_len == huffman.solution_2) and (max_len == huffman.solution_1):
        print(" Correct! Min: {} Max: {}".format(min_len,max_len))
    else:
        print("\n\tMin Got {} expected {}\n\tMax got {} expected {}".format(min_len,huffman.solution_2,max_len,huffman.solution_1))
