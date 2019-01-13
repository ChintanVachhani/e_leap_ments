def getScore(number_array, random_score_matrix):
    # print('narray: ', number_array)
    # print('rsm: ', random_score_matrix)
    random_score_matrix = random_score_matrix.tolist()
    # print(random_score_matrix)
    value = random_score_matrix[number_array[0] - 1][number_array[1] - 1]
    value = value + random_score_matrix[number_array[1] - 1][number_array[2] - 1]
    value = value + random_score_matrix[number_array[2] - 1][number_array[3] - 1]
    return value
