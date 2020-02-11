#Author: Kai Huang
#Date: 2015.04.06
#Just for undirected graph

import pickle
from Address import Address
from InitialData import InitialMatrix

def WriteAddressDictToFile():
	adjacencyMatrix = InitialMatrix()
	addressInstance = Address()
	addressInstance.GenerateSubgraphAddressDict(1, 1, adjacencyMatrix)
	addressDict = addressInstance.GetAddressDict()
	for i in addressDict:
		break
	addressDictFile = open("./temp data/AddressDict", "w")
	pickle.dump(addressDict, addressDictFile)
	addressDictFile.close()

def ReadAddressDictFromFile():
	addressDictFile = open("./temp data/AddressDict", "r")
	addressDict = pickle.load(addressDictFile)
	return addressDict

if __name__ == '__main__':
	WriteAddressDictToFile()