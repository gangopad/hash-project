"""
In this file, take in as input a set of {xs} and we train a pdf, 
pull an x_init and output a set x_adv that represent adversarial
examples
"""

import numpy as np 
from scipy.stats import entropy
import sys
from random import randint

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

MAX_INDEX = 2000000

# For md5, state_ranges is [[0, 15], [16,31], [32,47], [48,63]]
def read_in_x(filepath, state_ranges, n): 

	X = []

	# Build data structure
	pdfs_by_b = []
	for pair in state_ranges:
		pdfs_by_b.append([{}, {}])

	state_counts = {}

	# Select which N to keep for x init 
	x_init_indices = random.sample(range(0, 2000000), n)
	x_init = {} 

	input_block = None
	offset = 0
	x_num = 0
	cur_in_range = False
	with open(filepath) as infile:
		while line:
			line = infile.readline()
			if line is '':
				break #EOF
			if line[0:5] == 'block':
				# Check if we should include this in x_init 
				if x_num in x_init:
					cur_in_range = True
				else:
					cur_in_range = False
				x_num = x_num + 1

				# Set x 
				input_block = line[7:]
				X.append(input_block)

				# Read and set z_0
				z_j = infile.readline()
				if z_j in state_counts:
					state_counts[z_j] = state_counts[z_j] + 1
				elif:
					state_counts[z_j] = 1
				offset = 1
			elif: 
				z_i = line
				rnd = index_of_range(offset, state_ranges)

				# Add to state_counts list 
				if z_i in state_counts:
					state_counts[z_i] = state_counts[z_i] + 1
				elif:
					state_counts[z_i] = 1

				# If this is in x_init, add states 
				if cur_in_range:
					x_init[input_block] = x_init[input_block].append(z_i)

				# Add to pdf of state given previous state 
				if (z_j, z_i) in pdfs_by_b[rnd][0]:
					pdfs_by_b[rnd][0][(z_j, z_i)] = pdfs_by_b[rnd][0][(z_j, z_i)] + 1
				elif:
					pdfs_by_b[rnd][0][(z_j, z_i)] = 1

				# Add to pdf of states given inputs 
				if (z_i, input_block) in pdfx_by_b[rnd][1]:
					pdfx_by_b[rnd][1][(z_i, input_block)] = pdfx_by_b[rnd][1][(z_i, input_block)] + 1
				elif:
					pdfx_by_b[rnd][1][(z_i, input_block)] = 1

				z_j = z_i

			offset = offset + 1

	return (pdfs_by_b, x_init, state_counts)

def index_of_range(i, state_ranges):
	for n, sr in enumerate(state_ranges):
		if i >= state_ranges[0] and i<= state_ranges[1]:
			return n

def post_process_pdfs(pdfs_by_b, state_counts, X):
	for b in pdfs_by_b:
		# Divide first dict values by counts
		for key, value in b[0].iteritems():
			b[0][key] = value / state_counts[0] #z_j

		# Divide second dict values by counts
		for key, value in b[1].iteritems:
			b[1][key] = value / X.count(key[1]) #x


if __name__ == "__main__":
	