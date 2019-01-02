# This script will compute the entropy of a set of hex-strings in a directory. 
# python compute_entropy.py /path/to/dir/of/hex/strings 

import math
import os 
import sys 

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

string_path = sys.argv[1]
hex_strings = {}

# Iterate over all files in dir 
# Read each file into dictionary 
for filename in absoluteFilePaths(string_path):
  with open(filename, 'r') as cur_file: 
    file_str = cur_file.read()
    hex_str = hex(int(file_str, 16))[2:]
    if hex_str not in hex_strings: 
      hex_strings[hex_str] = 1
    else:
      hex_strings[hex_str] = hex_strings[hex_str] + 1

# Iterate over dict (k,v) to compute entropy 
num_uniq_strs = len(hex_strings)
entropy = 0

for k, v in hex_strings.items():
  p_x = v / num_uniq_strs
  entropy += p_x * math.log(p_x)

entropy *= -1 
print("Entropy: " + str(entropy))