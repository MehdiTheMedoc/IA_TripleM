import os

def SeparateSong(LineNumber):

	f = open("YearPredictionMSD.txt","r")



	SeparateSong(5000)
	line = f.readline()

	for i in range (0,LineNumber):
		line = f.readline()
	print line

	tabStr = line.split(",")
	print tabStr

	tabFloat = []
	for i in range (0,len(tabStr)):
		tabFloat.append(float(tabStr[i]))
	print tabFloat

	f.close()

	return


	
if __name__ == "__main__":


	print "Hello Mehdi"