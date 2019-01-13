from random import randint

def generate_random(n):
	generated = []
	for x in range(0, n):
		generated.append(randint(1, 4))
	return generated
