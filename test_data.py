#!/usr/bin/env python3.9

import pickle
import numpy as np
import sys

"""
The original script is written for Python2.
This script is re-written for Python3 from original one.
"""
print("\n===== test script =====\n")

hoc_path = sys.argv[1]
print("Loading hoc_data from ", hoc_path)
hoc_data = np.loadtxt(hoc_path, skiprows=1)

python_path = sys.argv[2]
print("Loading python_data from ", python_path)
with open(python_path, 'rb') as f:
    python_data = pickle.load(f)

p_data = np.array(python_data).T


def print_comparison(i):
    print("hoc_data: \t", hoc_data[i])
    print("python_data: \t", p_data[i])
    
print("\n")

max_diff = np.max(p_data - hoc_data)
max_diff_idx = np.where((p_data - hoc_data) == max_diff)

print("max diff: {}, time: {}".format(max_diff, max_diff_idx[0]))
if max_diff < 0.001:
    print("TEST PASSED")
else:
    print("FAILED")

k = np.random.randint(0, len(python_data[0]))
print("\nRandom pair (k=%d):" % k)
print_comparison(k)

print("\n")