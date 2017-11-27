import random
import read

def randomWeights(input_number):
	weights = []
	for i in range(input_number):
		weights.append(random.random())
	return weights

def compute_unicouche(weights, music):
	res = 0
	for i in range(0,len(weights)):
		res += weights[i] * music[i+1]
	return res

def fitness(weights, musicList, function):
	summ = 0
	for i in range(len(musicList)):
		summ += abs(musicList[i][0] - function(weights, musicList[i]))
	return summ/len(musicList)
	
def trainRandom(weights, musicList, fonction, precision):
	fit = fitness(weights, musicList, fonction)
	for i in range(len(weights)):
		tempw = weights[i]
		
		weights[i] += (random.random()-0.5)*precision * weights[i]*0.1
		f = fitness(weights, musicList, fonction)
		counter = 0
		while(f>fit and counter < 10):
			counter += 1
			weights[i] = tempw + (random.random()-0.5)*precision * weights[i]*0.1
			f = fitness(weights, musicList, fonction)
		if(counter >= 10):
			weights[i] = tempw
		fit = fitness(weights, musicList, fonction)
		
	return weights


def trainPlusMinus(weights, musicList, fonction, precision):
	fit = fitness(weights, musicList, fonction)
	for i in range(len(weights)):
		tempw = weights[i]
		delta = precision

		weights[i] += delta
		f = fitness(weights, musicList, fonction)
		if(f>fit):
			weights[i] -= 2*delta
			f = fitness(weights, musicList, fonction)
			if(f>fit):
				weights[i] = tempw
		
		fit = fitness(weights, musicList, fonction)
		
	return weights


w = randomWeights(90)

il = []
for i in range (100):
	il.append(read.SeparateSong(i))

#print(len(read.SeparateSong(0)))



print(str(fitness(w, il, compute_unicouche)))
for i in range (50):
	trainRandom(w,il,compute_unicouche, 1.0/(i+1.0))
print(str(fitness(w, il, compute_unicouche)))
print(str(compute_unicouche(w, il[0])))
print(str(compute_unicouche(w, il[1])))
print(str(compute_unicouche(w, il[2])))
print(str(compute_unicouche(w, read.SeparateSong(39))))
