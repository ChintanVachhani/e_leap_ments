def getScore(number_array, random_score_matrix):
	value = random_score_matrix[number_array[0]-1,number_array[1]-1]
	value = value + random_score_matrix[number_array[1]-1, number_array[2]-1]
	value = value + random_score_matrix[number_array[2]-1, number_array[3]-1]
	return value