#Author: Kai Huang
#Date: 2015.04.07

import sys
sys.path.append("../tools")
import DataInfo
import pickle
import InitialData
from Address import Address
import hashlib

def CompleteGroup(path, nodesDict):
	pathDict = {}
	for i in path:
		for j in path:
			if j in nodesDict[i]:
				if i not in pathDict:
					pathDict[i] = {}
				pathDict[i][j] = 1
	return pathDict
def HashPath(path):
	s = ""
	for i in path:
		s += str(i) + " "
	return hashlib.md5(s.encode("utf-8")).hexdigest()

def GenerateVector(paths, nodesDict, addressDict):
	pathSet = set()
	vector = {}
	for path in paths:
		hashValue = HashPath(path)
		if hashValue not in pathSet:
			pathSet.add(hashValue)
			pathDict = CompleteGroup(path, nodesDict)
			nodeMapping = {path[0]:1, path[-1]:2}
			for i in xrange(1, len(path) - 1):
				nodeMapping[path[i]] = i + 2
			adjacencyMatrix = InitialData.InitialMatrix()
			for i in pathDict:
				for j in pathDict[i]:
					adjacencyMatrix[nodeMapping[i]][nodeMapping[j]] = 1
					#adjacencyMatrix[nodeMapping[j]][nodeMapping[i]] = 1
			adjacencyMatrixAddress = Address().GetAddress(adjacencyMatrix)
			subAddress = addressDict[adjacencyMatrixAddress]
			vector[subAddress] = vector.get(subAddress, 0) + 1
	return vector