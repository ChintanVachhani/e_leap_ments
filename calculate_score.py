#inputs: 
	#1)a string of data (4 characters which can be A,B,C,or D in any combination)
	#2)the random_score_matrix for the game

#output: a score

#from e_leap_ments import * #to access the random_score_matrix from generate_random_table.py
import numpy as np 



def calculate_score(input_string,random_score_matrix):
	
	string_to_index= {
		"A":0,
		"B":1,
		"C":2,
		"D":3
	}


	if len(input_string)==1:
		i0=string_to_index[input_string[0]]
		answer= random_score_matrix[i0,i0]*.25
	elif len(input_string)==2:
		i0=string_to_index[input_string[0]]
		j0=string_to_index[input_string[1]]
		answer= random_score_matrix[i0,j0]
	elif len(input_string)==3: 
		i0=string_to_index[input_string[0]]
		j0=string_to_index[input_string[1]]
		i1=string_to_index[input_string[1]]
		answer= random_score_matrix[i0,j0] + random_score_matrix[i1, i1]*.5
	elif len(input_string)==4:
	 	i0=string_to_index[input_string[0]]
	 	j0=string_to_index[input_string[1]]

	 	i1=string_to_index[input_string[1]]
	 	j1=string_to_index[input_string[2]]

	 	i2=string_to_index[input_string[2]]
	 	j2=string_to_index[input_string[3]]

	 	answer= random_score_matrix[i0,j0] + random_score_matrix[i1, j1] +random_score_matrix[i2, j2]





	#convert input 
	# for i in np.arange(4):
	# 	i0=string_to_index[input_string[0]]
	# 	j0=string_to_index[input_string[1]]

	# 	i1=string_to_index[input_string[1]]
	# 	j1=string_to_index[input_string[2]]

	# 	i2=string_to_index[input_string[2]]
	# 	j2=string_to_index[input_string[3]]
	# 	answer= random_score_matrix[i0,j0] + random_score_matrix[i1, j1] +random_score_matrix[i2, j2]



	#sum the pairs of indicies to find the final score
	#print(random_score_matrix[i0,j0] + random_score_matrix[i1, j1])

	return answer






# def generate_random_table():
# 	a = np.random.normal(loc=1.0, scale=.8, size= (4,4))

# 	#turn negatives into positives and make overpowered numbers more rare
# 	for i in np.arange(4):
# 		for j in np.arange(4):
# 			if a[i,j] <0:
# 				a[i,j]*=-1.00
# 			if a[i,j] >1.5:
# 				a[i,j]-=.500
# 	print(a)
# 	return a

# rt=generate_random_table()


# a= calculate_score("ABCD", rt)

# print(a)
