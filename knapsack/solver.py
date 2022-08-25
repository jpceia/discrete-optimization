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
    O_prev = np.zeros(capacity, dtype=np.int32)
    arr_prev = np.zeros((capacity, N), dtype=np.bool_)
    
    for i in range(N):
        v = values[i]
        w = weights[i]
        arr = arr_prev.copy()
        O = O_prev.copy()
        for k_index in range(capacity):
            k = k_index + 1
            #v / w <= O_prev[k_index] / k or
            if weights[i] > k or O_prev[k_index] > v + O_prev[k_index-w]:
                continue # do not add the items
            # add the items
            O[k_index] = v + O_prev[k_index-w]
            arr[k_index] = arr_prev[k_index-w]
            arr[k_index, i] = True
        O_prev = O
        arr_prev = arr
    
    taken = arr[-1, :]
    return (taken * 1).tolist(), (taken * values).sum(), (taken * weights).sum()

def solve_branch_and_bound(values, weights, value, room, estimate=None):
    if optimistic_estimate is None:
        # calculating new optimistic estimate
        optimistic_estimate = value
        current_room = room
        for k, (v, w) in enumerate(zip(values, weights)):
            if w <= current_room:
                optimistic_estimate += v
                current_room -= w
            else:
                optimistic_estimate += v * current_room / w
                current_room = 0
                break
    
    v, w = values[0], weights[0]    
    if len(values) == 1:
        if w <= capacity:
            return [1], v, w
        # else:
        return [0], 0, 0
    # else:
    
    value_left = 0
    value_right = 0
    if capacity >= w and optimistic_estimate > value + v:
        x_left, value_left = solve_branch_and_bound(values[1:], weights[1:], value + v, capacity - w, optimistic_estimate)
    if value_left < optimistic_estimate:
        x_right, value_right = solve_branch_and_bound(values[1:], weights[1:], value, capacity, optimistic_estimate)
    
    if value_left > value_right:
        return [1] + x_left, value_left
    # else
    return [0] + x_right, value_right
    
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
    if len(values) <= 1000:
        taken, value, weight = solve_branch_and_bound(values, weights, capacity)
        is_optimal = '1'
    else:
        taken, value, weight = solve_greedy(values, weights, capacity)
        is_optimal = '0'
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

