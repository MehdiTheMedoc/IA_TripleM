import os


def SeparateSong(FileName,LigneNumber):

	for i in range (0,LigneNumber):
		ligne = FileName.readLigne()

	print(ligne)

	return



if __name__ == "__main__":


	print "Hello Mehdi"

	ficher = open("YearPredictionMSD.txt","r")

	SeparateSong(fichier,0)
