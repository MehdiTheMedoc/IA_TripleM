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

def fitnessMean(weights, musicList, function):
	summ = 0
	for i in range(len(musicList)):
		summ += abs(musicList[i][0] - function(weights, musicList[i]))
	return summ/len(musicList)

def fitnessMax(weights, musicList, function):
	val = 0
	for i in range(len(musicList)):
		val = max(abs(musicList[i][0] - function(weights, musicList[i])), val)
	return val
	
def trainRandom(weights, musicList, fonction, fitness, precision):
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


def trainPlusMinus(weights, musicList, fonction, fitness, precision):
	fit = fitness(weights, musicList, fonction)
	for i in range(len(weights)):
		tempw = weights[i]
		delta = precision

		weights[i] += delta
		tempf = fitness(weights, musicList, fonction)
		if(tempf>fit):
			weights[i] -= 2*delta
			tempf = fitness(weights, musicList, fonction)
			if(tempf>fit):
				tempf = fit
				weights[i] = tempw
		fit = tempf
	return weights


w = randomWeights(90)
trainIterations = 50

il = []
for i in range (5):
	il.append(read.SeparateSong(i))

#print(len(read.SeparateSong(0)))



print(str(fitnessMax(w, il, compute_unicouche)))
for i in range (trainIterations):
	print(str(fitnessMax(w, il, compute_unicouche)))
	if(i%2 == 0):
		trainPlusMinus(w,il,compute_unicouche, fitnessMax, 1.0/(i+1.0))
	else:
		trainRandom(w,il,compute_unicouche, fitnessMax, 1.0/(i+1.0))
	print("training : " + str((float(i)/float(trainIterations))*100)+"%")
print(str(fitnessMax(w, il, compute_unicouche)))
