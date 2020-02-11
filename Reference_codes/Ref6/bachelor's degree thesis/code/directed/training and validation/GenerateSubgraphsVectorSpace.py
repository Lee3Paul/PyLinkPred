#Author: Kai Huang
#Date: 2015.04.06
#Just for undirected graph

import pickle
from CalSubgraphAddress import ArgMinAddress
from InitialData import InitialMatrix

AddressDict = {0:1}

def GenerateSubgraphVectorSpace(lastI, lastJ, adjacencyMatrix):#Excluding the matrix full of 0
	for i in xrange(lastI, 8):
		for j in xrange(i + 1, 8):
			if (i == 1 and  j == 2) or (i == lastI and j <= lastJ):
				continue
			adjacencyMatrix[i][j] = 1
			adjacencyMatrix[j][i] = 1
			address = ArgMinAddress(adjacencyMatrix)
			AddressDict[address] = AddressDict.get(address, 0) + 1
			GenerateSubgraphVectorSpace(i, j, adjacencyMatrix)
			adjacencyMatrix[i][j] = 0
			adjacencyMatrix[j][i] = 0

if __name__ == '__main__':
	adjacencyMatrix = InitialMatrix()
	GenerateSubgraphVectorSpace(1, 1, adjacencyMatrix)
	addressDictFile = open("./temp data/VectorSpace", "w")
	pickle.dump(AddressDict, addressDictFile)
	addressDictFile.close()