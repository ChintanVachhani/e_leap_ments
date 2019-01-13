from math import sqrt
import numpy as np
from calculate_score import calculate_score

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

#uses recursive DFS to find optimal combinations
def find_path_helper(val_array, str, o_sol):
	if (len(str) == int(sqrt(val_array.size))):
		cur_max = calculate_score(str, val_array)
		u_max = calculate_score(o_sol[0], val_array)
		if (u_max < cur_max):
			o_sol[0] = str
	else:
		find_path_helper(val_array, str+"A", o_sol)
		find_path_helper(val_array, str+"B", o_sol)
		find_path_helper(val_array, str+"C", o_sol)
		find_path_helper(val_array, str+"D", o_sol)

def find_path(val_array):
	str = ""
	o_sol = ["AAAA"]
	find_path_helper(val_array, str, o_sol)
	return o_sol