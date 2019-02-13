"""
In this file we generate our set of states until H(Z) drops below 
epsilon for varying levels of epsilon. We analyze results over
various input sets. 
"""

import numpy as np 
from scipy.stats import entropy
import sys
from random import randint
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import decimal

# Routine to read in DS from data.txt file 
# @params filepath of structured data
# @return X. X is a dictoinary key'd by x valued by a list of states 
def read_in_x(filepath, blocks): 
	X_all = []
	for b in blocks:
		X_all.append({})

	offset = 0
	states = []
	input_block = None
	print "Reading in X..."
	with open(filepath, 'r') as infile:
		for line in infile:
			if line[0:5] == 'block':
				if input_block is not None:	
					X[input_block] = states

				states = []
				input_block = line[6:]
				offset = 0
			else:
				rnd = index_of_range(offset, blocks)
				if rnd is not None:
					new_list = X_all[rnd]
					new_list.append(line)
					X_all[rnd] = new_list
        
			offset = offset + 1
    
	return X_all

def index_of_range(i, state_ranges):
	for n, sr in enumerate(state_ranges):
		if i >= sr[0] and i<= sr[1]:
			return n


#computes the entropy given the list Z
def computeEntropy(Z, base):
	value,counts = np.unique(Z, return_counts=True)
  	return entropy(counts, base=base)

def theorem_1_routine(e, X):
	print "Epsilon value: " + str(e)
	entropy = sys.maxsize
	N = len(X)
	Z = []
	m = 0

	while entropy > e:
		m = m + 1
		rand_index = randint(0, N)
		inputs = X.keys()
		x = inputs[rand_index]
		z = X[x]
		Z.extend(z)
		entropy = computeEntropy(Z, 2)

		print "Entropy: " + str(entropy)

	return m

"""
Given a block, computes the number of examples 
needed to get H(Z) < epsilon over datasets
"""
def computeBlock(b, epsilon, ds_path):
	res = computeDataset(ds_path, b, epsilon)
	plot(res)

def computeEntropy(X):
	states_dict = {} 
	states_list = []
	for s in X:
		states_list.extend(X[s])

	for s in states_list:
		states_dict[s] = states_list.count(s)

	for k, v in hex_strings.items():
  		p_x = getcontext().divide(Decimal(v), Decimal(num_uniq_strs))
  		return getcontext().add(entropy, getcontext().multiply(p_x, p_x.ln()))

"""
Given a dataset, computes the number of examples 
needed to get H(Z) < epsilon
"""
def computeDataset(ds_path, b, epsilon, X):
	res = dict()
	epsilon_res = []

	for e in epsilon: 
		print "Tuple: " + str(b) + " epsilon: " + str(e)
		#X = read_in_x_b(ds_path, b)
		print("Real Entropy: " + str(computeEntropy(X)))
		m = theorem_1_routine(e, X)
		epsilon_res.append(m)

		print "For dataset " + str(ds_path) + " we have for epsilon value " + str(e) + " a value of m of " + str(m) + " such that H(Z) < e"

	res[ds_path] = epsilon_res

	return res

#generates a line plot over values of epsilon 
def plot(res, epsilon):
	df=pd.DataFrame({'x': epsilon, 'y1': res['data0.txt'], 'y2': res['data1.txt'], 'y3': res['data2.txt'] })
	fout = open("thm1.pdf", "wb")
	pickle.dump(df, fout)


	# multiple line plot
	plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label="data0.txt")
	plt.plot( 'x', 'y2', data=df, marker='', color='olive', linewidth=2, label="data1.txt")
	plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="data2.txt")
	plt.legend()
	f = plt.figure()
	f.savefig("t1_plot.pdf")

if __name__ == "__main__":
	epsilon = np.arange(0, 1, step=.05)
	blocks = [[0, 15], [16,31], [32,47], [48,63]]

	dataset_paths = ['data0_short.txt']
	for ds_path in dataset_paths:
		X_all = read_in_x(ds_path, blocks)

		for i, b in enumerate(blocks):
			computeBlock(b, epsilon, X_all[i], ds_path)
