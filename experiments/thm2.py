"""
In this file, take in as input a set of {xs} and we train a pdf, 
pull an x_init and output a set x_adv that represent adversarial
examples
"""

import numpy as np 
from scipy.stats import entropy
import sys
from random import randint


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
		states.add(z)

	x_new = getNewX(input_pdf, input_space, states)

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
			prob = prob + (conditional_states_pdf[(z, x)] * (1.0/len(input_space)))/states_pdf[z]

		X_new[x] = prob


if __name__ == "__main__":
	M = 10
	x_new = advAlg()
	top_x = getTopM(x_new, M)