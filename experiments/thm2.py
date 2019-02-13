"""
In this file, take in as input a set of {xs} and we train a pdf, 
pull an x_init and output a set x_adv that represent adversarial
examples
"""

import numpy as np 
from scipy.stats import entropy
import sys
import random

''' 
Compute 
(z_j, z_i) | (count(z_i,z_j)  / count (z_j))
(z_i, x_i) | (count(z_i, x_i) / count(x_i))

Get n Xs
- dict, where X is key and value is list of states
'''	

'''
@param filepath to dataset 
@param list [[0,a], [a+1,b]] of what the ranges are
@param n, z_init dict 
@return dicts (key is block) of dicts, each inner dict contains pdfs, x_init, state_counts
'''

MAX_INDEX = 15

# For md5, state_ranges is [[0, 15], [16,31], [32,47], [48,63]]
def read_in_x(filepath, state_ranges, n): 

	X = []

	# Build data structure
	pdfs_by_b = []

	for pair in state_ranges:
		pdfs_by_b.append([{}, {}])

	state_counts = {}

	# Select which N to keep for x init 
	x_init_indices = random.sample(range(0, MAX_INDEX), n)
	x_init = {} 

	input_block = None
	offset = 0
	x_num = 0
	cur_in_range = False
	with open(filepath) as infile:
		for line in infile:
			line = line.strip('\n')
			if line[0:5] == 'block':
				# Check if we should include this in x_init 
				if x_num in x_init_indices:
					cur_in_range = True
				else:
					cur_in_range = False
				x_num = x_num + 1

				# Set x 
				input_block = line[6:]
				X.append(input_block)
				offset = 0
			else: 
				z_i = line
				rnd = index_of_range(offset, state_ranges)
				if rnd is not None:
					# Add to state_counts list 
					if z_i in state_counts:
						state_counts[z_i] = state_counts[z_i] + 1
					else:
						state_counts[z_i] = 1

					# If this is in x_init, add states 
					if cur_in_range:
						if input_block in x_init:
							z_list = x_init[input_block]
							z_list.append(z_i)
							x_init[input_block] = z_list

						else:					
							x_init[input_block] = [z_i]

					# Add to pdf of states given inputs 
					if (z_i, input_block) in pdfs_by_b[rnd][1]:
						pdfs_by_b[rnd][1][(z_i, input_block)] = pdfs_by_b[rnd][1][(z_i, input_block)] + 1
					else:
						pdfs_by_b[rnd][1][(z_i, input_block)] = 1

			offset = offset + 1

	return pdfs_by_b, state_counts, X, x_init

def index_of_range(i, state_ranges):
	for n, sr in enumerate(state_ranges):
		if i >= sr[0] and i<= sr[1]:
			return n

def post_process_pdfs(pdf, state_counts, X):
		# Divide 'second' dict values by counts
	dic = {}
	for key in pdf[1]:
		value = pdf[1][key]
		print("VALUE " + str(value))
		print("DENOM " + str(X.count(key[1])))
		dic[key] = value / float(X.count(key[1])) #x
		#print(dic[key])

	return dic

def compute_p_z(state_counts):
	dic = {}
	denom = 0
	for k in state_counts:
		denom += state_counts[k]

	for k in state_counts:
		dic[k] = state_counts[k] / float(denom)

	return dic


"""
Returns a set of adversarial x's of size M. Takes in as input
the pdfs for p(z) and p(z_i | x_j) respectively, a set
of seeded bad inputs which contains a mapping from an input to a list of states
"""
def advAlg(M, states_pdf, conditional_states_pdf, input_space, X_init):
	X_adv = []
	states = set()

	for x in X_init:
		z = X_init[x]
		for z_cur in z:
			states.add(z_cur)

	x_new = getNewX(states_pdf, conditional_states_pdf, input_space, states)

	return x_new

#returns the top M adversarial examples by prob value
def getTopM(x_new, M):
	count = 0
	top_x = set()

	for key, value in sorted(x_new.iteritems(), key=lambda (k,v): (v,k)):
		count = count + 1
		top_x.add(key)

	return top_x


#returns the list of Xs with values for x_new and p(x) over the set of inputted states
def getNewX(states_pdf, conditional_states_pdf, input_space, states):
	X_new = dict()

	for x in input_space:
		prob = 0.0
		for z in states:
			if (z, x) in conditional_states_pdf: 
				# print(prob)
				print((1.0/len(input_space)))
				print(conditional_states_pdf[(z, x)])
				print(states_pdf[z])
				prob = prob + ((conditional_states_pdf[(z, x)] * (1.0/len(input_space))) / states_pdf[z])

		X_new[x] = prob
		print "For " + str(x) + " the probability is " + str(prob)
		return X_new


if __name__ == "__main__":

#	dataset_paths = ['data0.txt', 'data1.txt', 'data2.txt']
	dataset_paths = ['data0_short.txt']
	state_ranges = [[0, 15], [16,31], [32,47], [48,63]]
	n = 10

	for M in np.arange(100, 10000, step=1000): #Alter later
		for ds_path in dataset_paths:
			pdfs_by_b, state_counts, X, X_init = read_in_x(ds_path, state_ranges, n)
			for b in pdfs_by_b: 
				z_given_x = post_process_pdfs(b, state_counts, X)
				p_z = compute_p_z(state_counts)
				x_new = advAlg(M, p_z, z_given_x, X, X_init)
				print "X new is " + str(x_new)
				top_x = getTopM(x_new, M)
