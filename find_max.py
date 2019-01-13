from math import sqrt
import numpy as np

'''Uses Breadth First Search across all nodes to
calculate the optimal value of the given table'''

def find_max(val_array):
	size = int(sqrt(val_array.size))
	max_value = 0;
	for x in range(0, size):
		queue = [[x, x]]
		cur_value = 0;
		counter = 0;
		while ((queue != 0) and (counter<=3)):
			val = queue[0]
			queue = queue[1:]
			counter += 1
			cur_value += val_array[val[0]][val[1]]
			for y in range(0, size):
				queue.append([val[1], y])
		if (cur_value > max_value):
			max_value = cur_value
	return (max_value)
