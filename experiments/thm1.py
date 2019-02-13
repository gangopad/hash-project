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
			line = line.strip('\n')
			if line[0:5] == 'block':
				input_block = line[6:]
				offset = 0
			else:
				rnd = index_of_range(offset, blocks)
				if rnd is not None:
					if input_block in X_all[rnd]:
						new_list = X_all[rnd][input_block]
						new_list.append(line)
						X_all[rnd][input_block] = new_list
					else:
						X_all[rnd][input_block] = [line]

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
	entropy = 0
	prev_entropy = 0
	N = len(X)
	Z = []
	m = 0

	z_actual = []
	for k in X:
		z_actual.extend(X[k])
	kappa = computeEntropy(z_actual, 2)
	print("Kappa: " + str(kappa))

	while m < N:
		prev_entropy = entropy
		m = m + 1
		rand_index = randint(0, N - 1)
		inputs = X.keys()
		x = inputs[rand_index]
		z = X[x]
		Z.extend(z)
		entropy = computeEntropy(Z, 2)

		print "Entropy: " + str(entropy)

		if entropy < e * kappa and entropy < prev_entropy:
			return m

	return m

"""
Given a block, computes the number of examples 
needed to get H(Z) < epsilon over datasets
"""
def computeBlock(b, i, epsilon, ds_path, X):
	res = computeDataset(ds_path, b, epsilon, X)
	plot(res, epsilon, i)


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
		m = theorem_1_routine(e, X)
		epsilon_res.append(m)

		print "For dataset " + str(ds_path) + " we have for epsilon value " + str(e) + " a value of m of " + str(m) + " such that H(Z) < e"

	res[ds_path] = epsilon_res

	return res

#generates a line plot over values of epsilon 
def plot(res, epsilon, i):
	df=pd.DataFrame({'x': epsilon, 'y1': res['data0_short.txt'], 'y2': res['data0_short.txt'], 'y3': res['data0_short.txt'] })
	fout = open("thm1.pdf", "wb")
	pickle.dump(df, fout)


	# multiple line plot
	plt.plot( 'x', 'y1', data=df, marker='o', color='blue', linewidth=2, label="data0.txt")
	plt.plot( 'x', 'y2', data=df, marker='x', color='red', linewidth=2, label="data1.txt")
	plt.plot( 'x', 'y3', data=df, marker='d', color='black', linewidth=2, linestyle='dashed', label="data2.txt")
	plt.legend()
	plt.xlabel("Epsilon")
	plt.ylabel("M")
	plt.title("Number of examples until H(Z) < epsilon for B " + str(i))
	plt.savefig("b_" + str(i) + ".png")
	plt.clf()

if __name__ == "__main__":
	epsilon = np.arange(0, 1, step=.05)
	blocks = [[0, 15], [16,31], [32,47], [48,63]]

	dataset_paths = ['data0_short.txt']
	for ds_path in dataset_paths:
		X_all = read_in_x(ds_path, blocks)

		for i, b in enumerate(blocks):
			computeBlock(b, i, epsilon, ds_path, X_all[i])
