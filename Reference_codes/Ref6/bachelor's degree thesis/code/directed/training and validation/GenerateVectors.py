#Author: Kai Huang
#Date: 2015.04.07

import sys
sys.path.append("../tools")
import DataInfo
import pickle
import InitialData
import CalSubgraphAddress
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
	for i in sorted(path):
		s += str(i) + " "
	return hashlib.md5(s.encode("utf-8")).hexdigest()

def GenerateVectors(paths, nodesDict):
	pathSet = set()
	vector = {}
	for path in paths:
		if HashPath(path) not in pathSet:
			pathSet.add(HashPath(path))
			pathDict = CompleteGroup(path, nodesDict)
			nodeMapping = {path[0]:1, path[-1]:2}
			for i in xrange(1, len(path) - 1):
				nodeMapping[path[i]] = i + 2
			adjacencyMatrix = InitialData.InitialMatrix()
			for i in pathDict:
				for j in pathDict[i]:
					adjacencyMatrix[nodeMapping[i]][nodeMapping[j]] = 1
					adjacencyMatrix[nodeMapping[j]][nodeMapping[i]] = 1
			minAddress = CalSubgraphAddress.ArgMinAddress(adjacencyMatrix)
			vector[minAddress] = vector.get(minAddress, 0) + 1
	return vector

if __name__ == '__main__':
	pass
	# timeSpan = "1970_1979"
	# filesNames, fullFilesNames = InitialData.FileWalker("./temp data/PathsDict" + timeSpan + "")
	# for i in xrange(0, len(fullFilesNames)):
	# 	print filesNames[i]
	# 	print fullFilesNames[i]
	# 	pathsDictFile = open(fullFilesNames[i], "r")
	# 	pathsDict = pickle.load(pathsDictFile)
	# 	pathsDictFile.close()
	# 	nodesDict = InitialData.InitialNodesPairWeightDict(timeSpan)
	# 	vectors = GenerateVectors(pathsDict, nodesDict, int(filesNames[i]))
	# 	vectorsFile = open("./temp data/Vectors" + timeSpan + "/"+ filesNames[i], "w")
	# 	pickle.dump(vectors, vectorsFile)
	# 	vectorsFile.close()