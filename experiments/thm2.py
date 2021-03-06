"""
In this file, take in as input a set of {xs} and we train a pdf, 
pull an x_init and output a set x_adv that represent adversarial
examples
"""
import matplotlib
matplotlib.use('Agg')

import numpy as np 
import scipy.stats
import sys
import random
import pandas as pd 
import pickle
import matplotlib.pyplot as plt

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

MAX_INDEX = 1300

# For md5, state_ranges is [[0, 15], [16,31], [32,47], [48,63]]
def read_in_x(filepath, state_ranges, n): 

	X = []
	X_all = {}

	# Build data structure
	pdfs_by_b = []
	state_counts_by_b = []

	for pair in state_ranges:
		pdfs_by_b.append([{}, {}])
		state_counts_by_b.append({})

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
				offset = 0
			else: 
				X.append(input_block)

				z_i = line

				if input_block in X_all:
					z_list = X_all[input_block]
					z_list.append(z_i)
					X_all[input_block] = z_list
				else:					
					X_all[input_block] = [z_i]

				rnd = index_of_range(offset, state_ranges)
				if rnd is not None:
					# Add to state_counts list 
					if z_i in state_counts_by_b[rnd]:
						state_counts_by_b[rnd][z_i] = state_counts_by_b[rnd][z_i] + 1
					else:
						state_counts_by_b[rnd][z_i] = 1

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

	return pdfs_by_b, state_counts_by_b, X, x_init, X_all

def index_of_range(i, state_ranges):
	for n, sr in enumerate(state_ranges):
		if i >= sr[0] and i<= sr[1]:
			return n

def post_process_pdfs(pdf, state_counts, X):
		# Divide 'second' dict values by counts
	dic = {}
	for key in pdf[1]:
		value = pdf[1][key]
		dic[key] = value / float(X.count(key[1])) #x

	return dic

def compute_p_z(state_counts):
	dic = {}
	denom = 0
	for k in state_counts:
		denom += state_counts[k]

	for k in state_counts:
		dic[k] = state_counts[k] / float(denom)

	return dic


#computes the entropy given the list Z
def computeEntropy(Z, base):
	value,counts = np.unique(Z, return_counts=True)
  	return scipy.stats.entropy(counts, base=base)


#computes the number of collisions given Z
def computeCollisions(Z):
	seen = set()
	col = 0

	for z in Z:
		if z in seen:
			col = col + 1
		seen.add(z)

	return col


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
		if count > M:
			return top_x

#returns the list of Xs with values for x_new and p(x) over the set of inputted states
def getNewX(states_pdf, conditional_states_pdf, input_space, states):
	X_new = dict()

	for x in input_space:
		prob = 0.0
		for z in states:
			if (z, x) in conditional_states_pdf: 
				prob = prob + ((conditional_states_pdf[(z, x)] * (1.0/len(input_space))) / states_pdf[z])

		X_new[x] = prob
#		print "For " + str(x) + " the probability is " + str(prob)
	return X_new


#returns a list of entropy values per b
def getEntropy(res, b):
	M = res.keys()
	entropy = dict()

	for m in res:
		data_res = res[m]
		for ds in data_res:
			b_res = data_res[ds]
			top_states = b_res[b]
			ent = computeEntropy(top_states, 2)
			if ds in entropy:
				l = entropy[ds]
				l.append(ent)
				entropy[ds] = l
			else:
				entropy[ds] = [ent]

	return entropy


#returns a list of collisions per b
def getCollisions(res, b):
	M = res.keys()
	collisions = dict()

	for m in res:
		data_res = res[m]
		for ds in data_res:
			b_res = data_res[ds]
			top_states = b_res[b]
			#print(top_states)
			col = computeCollisions(top_states)
			
			if ds in collisions:
				l = collisions[ds]
				l.append(col)
				collisions[ds] = l
			else:
				collisions[ds] = [col]

	return collisions


#generates a line plot over values of epsilon 
def plot(M, fname, xlabel, ylabel, title, res):
	df=pd.DataFrame({'x': M, 'y1': res['seeded_0.txt'], 
		'y2': res['seeded_1.txt'], 'y3': res['seeded_2.txt'], 
		'y4': res['random_0.txt']
		,'y5': res['random_1.txt'], 'y6': res['random_2.txt'] 
		})
	fout = open(fname + ".pickle", "wb")
	pickle.dump(df, fout)

	# multiple line plot
	plt.plot( 'x', 'y1', data=df, marker='o', linewidth=1, linestyle='dotted', label="seeded 0")
	plt.plot( 'x', 'y2', data=df, marker='x', linewidth=1, linestyle='dotted', label="seeded 1")
	plt.plot( 'x', 'y3', data=df, marker='d', linewidth=1, linestyle='dotted', label="seeded 2")
	plt.plot( 'x', 'y4', data=df, marker='<', linewidth=1, linestyle='dashed', label="random 0")
	plt.plot( 'x', 'y5', data=df, marker='>', linewidth=1,  linestyle='dashed', label="random 1")
	plt.plot( 'x', 'y6', data=df, marker='_', linewidth=1, linestyle='dashed', label="random 2")
	
	plt.legend()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.savefig(fname + ".png")
	plt.clf()

if __name__ == "__main__":

	dataset_paths = ['seeded_0.txt','seeded_1.txt','seeded_2.txt', 'random_0.txt','random_1.txt','random_2.txt' ]
	#dataset_paths = ['seeded_0.txt', 'random_0.txt']

	state_ranges = [[0, 15], [16,31], [32,47], [48,63]]
	n = 100
	res = dict()
	data_res = dict()
	#M = [20, 200]#, 2000], 20000, 200000, 1999999]
	M = [1, 10, 100, 1000]
	#M = np.arange(100, 10000, step=1000) #Alter later

	for m in M:
		data_res = dict()
		for ds_path in dataset_paths:
			b_res = dict()
			pdfs_by_b, state_counts, X, X_init, X_all = read_in_x(ds_path, state_ranges, n)
			for i, b in enumerate(pdfs_by_b): 
				z_given_x = post_process_pdfs(b, state_counts[i], X)
				p_z = compute_p_z(state_counts[i])
				x_new = advAlg(M, p_z, z_given_x, X, X_init)
				top_x = getTopM(x_new, m)
				top_states = []

				for x in top_x:
					top_states.extend(X_all[x])
				print "Generating for m, ds, b" + str(m) + " " + str(ds_path) + " " + str(i)

				b_res[i] = top_states

			data_res[ds_path] = b_res
		res[m] = data_res

	
	for b in range(0, len(state_ranges)):
		entropy = getEntropy(res, b)
		plot(M, "entropy_" + str(b), "M", "Entropy", "Entropy values by M", entropy)
		collisions = getCollisions(res, b)
		plot(M, "collisions_" + str(b), "M", "Collisions", "Collision values by M", collisions)
	

# M 
# n (size of seed state)
# MAX_INDEX, apriori len(X_full)

