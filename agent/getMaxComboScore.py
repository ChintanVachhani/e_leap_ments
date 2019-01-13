import sys
sys.path.append("../")
from find_max import find_max

#val_array is the matrix of weights for the combinations
def getMaxComboScore(val_array):
	return find_max(val_array)
