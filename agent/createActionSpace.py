from itertools import product
from random import shuffle
import random


def createActionSpace(dimension):
    dim_sqr = pow(dimension, dimension)

    _list = []
    _list = [item for item in product([i for i in range(1, dimension + 1)], repeat=dimension)]

    idices = random.sample(range(dim_sqr), dim_sqr)

    res = []
    for i in range(len(_list)):
        res.append(_list[idices[i]])
    return res

# print(createActionSpace(4))
