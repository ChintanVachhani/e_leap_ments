# inputs:
# 1)a string of data (4 characters which can be A,B,C,or D in any combination)
# 2)the random_score_matrix for the game

# output: a score

from generate_random_table import *  # to access the random_score_matrix from generate_random_table.py
import numpy as np


def calculate_score(input_string, random_score_matrix):
    string_to_index = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4
    }

    # convert input
    for i in np.arange(4):
        i0 = string_to_index[input_string[0]]
        j0 = string_to_index[input_string[1]]

        i1 = string_to_index[input_string[1]]
        j1 = string_to_index[input_string[2]]

        i2 = string_to_index[input_string[2]]
        j2 = string_to_index[input_string[3]]

    # sum the pairs of indicies to find the final score
    # print(random_score_matrix[i0,j0] + random_score_matrix[i1, j1])
    return random_score_matrix[i0, j0] + random_score_matrix[i1, j1] + random_score_matrix[i2, j2]
