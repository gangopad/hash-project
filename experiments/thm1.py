# Routine to read in DS from data.txt file 
import numpy as np 

# @params filepath of structured data
# @return X. X is a dictoinary key'd by x valued by a list of states 
def read_in_x(filepath, start, end): 
	X = {}

	offset = 0
	states = []
	with open(filepath) as infile:
    for line in infile:
        if line[0:5] == 'block':
        	X[input_block] = states

        	states = []
        	input_block = line[7:]
        	offset = 0
        else if offset >= start and offset <= end: 
        	states.append(line)
        
        offset = offset + 1

	return X


def read_in_x_b0(filepath):
	return read_in_x(0,15)

def read_in_x_b1(filepath):
	return read_in_x(16,31)

def read_in_x_b2(filepath):
	return read_in_x(32,47)

def read_in_x_b3(filepath):
	return read_in_x(48,63)

def theorem_1_routine(e, X):
	return e #filler 


epsilon = np.arange(0, 1, step=.05)
dataset_paths = ['data0.txt', 'data1.txt', 'data2.txt']

for ds_path in dataset_paths:
	for e in epsilon: 
		X = read_in_x_b0(ds_path)
		m = theorem_1_routine(e, X)

		X = read_in_x_b1(ds_path)
		m = theorem_1_routine(e, X)

		X = read_in_x_b2(ds_path)
		m = theorem_1_routine(e, X)

		X = read_in_x_b3(ds_path)
		m = theorem_1_routine(e, X)










