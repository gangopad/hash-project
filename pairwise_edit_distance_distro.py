import math
import os 
import sys 
import numpy as np

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])
    return res

def dist(s, t): 
  cost = 0
  for _s, _t in zip(s, t):
    if _s != _t:
      cost += 1
  return cost 

string_path = sys.argv[1]
hashs = []
l_distances = []
distances = []

for filename in absoluteFilePaths(string_path):
  with open(filename, 'rb') as cur_file: 
    file_str = cur_file.read()
    hashs.append(file_str)

for s in hashs:
  for t in hashs:
    #l_distances.append(LD(s, t))
    distances.append(dist(s, t))

print("mean:      " + str(np.mean(l_distances)))
print("median:    " + str(np.median(l_distances)))
print("std dev:   " + str(np.std(l_distances)))

print("mean:      " + str(np.mean(distances)))
print("median:    " + str(np.median(distances)))
print("std dev:   " + str(np.std(distances)))




