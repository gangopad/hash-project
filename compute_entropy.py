# This script will compute the entropy of a set of hex-strings in a directory. 
# python compute_entropy.py /path/to/dir/of/hex/strings 

import math
import os 
import sys 
from decimal import * 

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

string_path = sys.argv[1]
hex_strings = {}
total_strs = 0

# Iterate over all files in dir 
# Read each file into dictionary 
for filename in absoluteFilePaths(string_path):
  total_strs += 1
  with open(filename, 'rb') as cur_file: 
    file_str = cur_file.read()
    #hex_str = hex(int(file_str, 16))[2:]
    hex_str = file_str
    if hex_str not in hex_strings: 
      hex_strings[hex_str] = 1
    else:
      hex_strings[hex_str] = hex_strings[hex_str] + 1

# Iterate over dict (k,v) to compute entropy 
num_uniq_strs = len(hex_strings)
entropy = Decimal(0)

for k, v in hex_strings.items():
  if v > 1:
    print(str(hash(k)) + "      " + str(v))
  p_x = getcontext().divide(Decimal(v), Decimal(num_uniq_strs))
  entropy = getcontext().add(entropy, getcontext().multiply(p_x, p_x.ln()))

entropy = getcontext().multiply(-1, entropy) 
print("Entropy:     " + str(entropy))

max_prob = Decimal(1) / Decimal(total_strs)
max_entropy = getcontext().multiply(-1, getcontext().multiply(total_strs, getcontext().multiply(max_prob, max_prob.ln())))
print("Max Entropy: " + str(max_entropy))

print("Delta:       " + str(getcontext().subtract(max_entropy,entropy)))
