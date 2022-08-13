#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def solve_greedy(values, weights, capacity):

    density = values / weights
    idx = np.argsort(density)[::-1] # decresing value
    
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    ks_value = 0
    ks_weight = 0
    taken = np.zeros_like(values, dtype=np.int32)
    
    for i in idx:
        v = values[i]
        w = weights[i]
        if ks_weight + w <= capacity:
            taken[i] = 1
            ks_value += v
            ks_weight += w
            
    return taken, ks_value, ks_weight

def solve_dynamic(values, weights, capacity):
    N = len(values)
    O = np.zeros((capacity, N), dtype=np.int32)
    arr = np.zeros((capacity, N, N), dtype=np.bool_)
    
    for i in range(N):
        v = values[i]
        w = weights[i]
        for k_index in range(capacity):
            k = k_index + 1
            if weights[i] > k:
                O[k_index, i] = O[k_index, i-1]
                arr[k_index, i, :] = arr[k_index, i-1, :]
                continue
            if O[k_index, i-1] > v + O[k_index-w, i-1]:
                O[k_index, i] = O[k_index, i-1]
                arr[k_index, i, :] = arr[k_index, i-1, :]
            else:
                O[k_index, i] = v + O[k_index-w, i-1]
                arr[k_index, i, :] = arr[k_index-w, i-1, :]
                arr[k_index, i, i] = True
    
    taken = arr[-1, -1, :]
    return (taken * 1).tolist(), (taken * values).sum(), (taken * weights).sum()
    
    
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        values.append(int(parts[0]))
        weights.append(int(parts[1]))
    
    values = np.asarray(values)
    weights = np.asarray(weights)
    if len(values) <= 200:
        taken, value, weight = solve_dynamic(values, weights, capacity)
        is_optimal = '1'
    else:
        taken, value, weight = solve_greedy(values, weights, capacity)
        is_optimal = '1' if weight == capacity else '0'
    # prepare the solution in the specified output format

    output_data = str(value) + ' ' + is_optimal + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

