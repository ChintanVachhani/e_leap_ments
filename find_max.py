from math import sqrt
import numpy as np
from calculate_score import calculate_score

'''Uses Breadth First Search across all nodes to
calculate the optimal value of the given table'''


def find_max(val_array):
    size = int(sqrt(val_array.size))
    max_value = 0
    for x in range(0, size):
        queue = [[x, x]]
        cur_value = 0
        counter = 0
        while (queue != 0) and (counter <= 3):
            val = queue[0]
            queue = queue[1:]
            counter += 1
            cur_value += val_array[val[0]][val[1]]
            for y in range(0, size):
                queue.append([val[1], y])
        if (cur_value > max_value):
            max_value = cur_value
    return (max_value)


def find_path_helper(val_array, str):
    if (str.size == int(sqrt(val_array.size))):
        real_max = find_max(val_array)
        cur_max = calculate_score(str, val_array)
        if (real_max == cur_max):
            return str
    find_path_helper(val_array, str + "A")
    find_path_helper(val_array, str + "B")
    find_path_helper(val_array, str + "C")
    find_path_helper(val_array, str + "D")


def find_path(val_array):
    str = ""
    return find_path_helper(val_array, str)
