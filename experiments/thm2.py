"""
In this file, take in as input a set of {xs} and we train a pdf, 
pull an x_init and output a set x_adv that represent adversarial
examples
"""

import numpy as np 
from scipy.stats import entropy
import sys
from random import randint



if __name__ == "__main__":
	dhhd