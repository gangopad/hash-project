"""
In this file we generate our set of states until H(Z) drops below 
epsilon for varying levels of epsilon. We analyze results over
various input sets. 
"""
import matplotlib
matplotlib.use('Agg')
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
	#print "Epsilon value: " + str(e)
	entropy = 0
	prev_entropy = 0
	N = len(X)
	Z = []
	m = 0

	z_actual = []
	for k in X:
		z_actual.extend(X[k])
	kappa = computeEntropy(z_actual, 2)

	while m < N:
		prev_entropy = entropy
		m = m + 1
		rand_index = randint(0, N - 1)
		inputs = X.keys()
		x = inputs[rand_index]
		z = X[x]
		Z.extend(z)
		entropy = computeEntropy(Z, 2)

		#print "Entropy: " + str(entropy)

		if entropy < e * kappa and entropy < prev_entropy:
			return m

	return m

"""
Given a block, computes the number of examples 
needed to get H(Z) < epsilon over datasets
"""
def computeBlock(b, i, epsilon, ds_path, X):
	return computeDataset(ds_path, b, epsilon, X)[ds_path]
	#res = computeDataset(ds_path, b, epsilon, X)
	#plot(res, epsilon, i)


"""
Given a dataset, computes the number of examples 
needed to get H(Z) < epsilon
"""
def computeDataset(ds_path, b, epsilon, X):
	res = dict()
	epsilon_res = []

	for e in epsilon: 
		#print "Tuple: " + str(b) + " epsilon: " + str(e)
		print "Computing for epsilon " + str(e)
		#X = read_in_x_b(ds_path, b)
		m = theorem_1_routine(e, X)
		epsilon_res.append(m)

		#print "For dataset " + str(ds_path) + " we have for epsilon value " + str(e) + " a value of m of " + str(m) + " such that H(Z) < e"

	res[ds_path] = epsilon_res

	return res

#generates a line plot over values of epsilon 
def plot(res, epsilon, i):
	df=pd.DataFrame({'x': M, 'y1': res['seeded_0.txt'], 
		'y2': res['seeded_1.txt'], 'y3': res['seeded_2.txt'], 
		'y4': res['random_0.txt']
		,'y5': res['random_1.txt'], 'y6': res['random_2.txt'] 
		})
	fout = open("thm1.pdf", "wb")
	pickle.dump(df, fout)

	# multiple line plot
	plt.plot( 'x', 'y1', data=df, marker='o', '''color='blue',''' linewidth=1, linestyle='dotted', label="seeded 0")
	plt.plot( 'x', 'y2', data=df, marker='x', '''color='red''', linewidth=1, linestyle='dotted', label="seeded 1")
	plt.plot( 'x', 'y3', data=df, marker='d', '''color='black''', linewidth=1, linestyle='dotted', label="seeded 2")
	plt.plot( 'x', 'y4', data=df, marker='<', '''color='blue''', linewidth=1, linestyle='dashed', label="random 0")
	plt.plot( 'x', 'y5', data=df, marker='>', '''color='red''', linewidth=1,  linestyle='dashed', label="random 1")
	plt.plot( 'x', 'y6', data=df, marker='_', '''color='black''', linewidth=1, linestyle='dashed', label="random 2")
	
	plt.legend()
	plt.xlabel("Epsilon")
	plt.ylabel("M")
	plt.title("Number of examples until H(Z) < epsilon for B " + str(i))
	plt.savefig( res.keys()[0] + "b_" + str(i) + ".png")
	plt.clf()

if __name__ == "__main__":
	epsilon = np.arange(0, 1, step=.05)
	blocks = [[0, 15], [16,31], [32,47], [48,63]]
	res = dict()
	for i, b in enumerate(blocks):
		res[i] = dict()

	dataset_paths = ['seeded_0.txt','seeded_1.txt','seeded_2.txt', 'random_0.txt','random_1.txt','random_2.txt' ]
	#dataset_paths = ['seeded_0.txt', 'random_0.txt']
	for ds_path in dataset_paths:
		X_all = read_in_x(ds_path, blocks)
		print "Finished reading in x for " + str(ds_path)
		for i, b in enumerate(blocks):
			print "Computing block " + str(i)
			res[i][ds_path] = computeBlock(b, i, epsilon, ds_path, X_all[i])
	for i, b in enumerate(blocks):
		print(res[i])
		plot(res[i], epsilon, i)

# None 
