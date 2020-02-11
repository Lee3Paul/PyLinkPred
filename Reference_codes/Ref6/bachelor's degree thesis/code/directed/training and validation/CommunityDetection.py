#Author: Kai Huang
#Date: 2015.04.10

import InitialData
import pickle
import ConnectedComponents

def GetNodesWeight(nodesPairWeightDict):
	nodesWeightDict = {}
	m = 0.0
	for i in nodesPairWeightDict:
		for j in nodesPairWeightDict[i]:
			m += nodesPairWeightDict[i][j]
			nodesWeightDict[i] = nodesWeightDict.get(i, 0) + nodesPairWeightDict[i][j]
	m = 0.5 * m
	return m, nodesWeightDict

def GetModularity(nodesWeightDict, nodesPairWeightDict, m, c):
	cMap = {}
	for i in c:
		if c[i] not in cMap:
			cMap[c[i]] = []
		cMap[c[i]].append(i)
	q = 0.0
	for i in cMap:
		sigmaIn = 0.0
		sigmaTot = 0.0
		for j in cMap[i]:
			sigmaTot += nodesWeightDict[j]
			for k in nodesPairWeightDict[j]:
				if k in cMap[i]:
					sigmaIn += nodesPairWeightDict[j][k]
		q += sigmaIn / 2 / m - pow(sigmaTot / 2 / m, 2)
	return q

def  GetModularityGain(nodesWeightDict, nodesPairWeightDict, m, c, node, newCommunity):

	sigmaTot = 0.0
	for i in c:
		if c[i] == newCommunity and i != node:
			sigmaTot += nodesWeightDict[i]

	kiIn = 0.0
	for neighbor in nodesPairWeightDict[node]:
		if newCommunity == c[neighbor] or neighbor == node:
			kiIn += nodesPairWeightDict[node][neighbor]

	qGain = kiIn / m - sigmaTot * nodesWeightDict[node] / 2 / m / m
	return qGain

def CommunityDetection(timeSpan):
	#nodesPairWeightDict = {0:{2:1, 4:1, 5:1, 3:1}, 1:{2:1, 4:1, 7:1}, 2:{0:1, 1:1, 4:1, 5:1, 6:1}, 3:{0:1, 7:1}, 4:{0:1, 1:1, 2:1, 10:1}, 5:{0:1, 2:1, 7:1, 11:1}, 6:{2:1, 7:1, 11:1}, 7:{1:1, 3:1, 5:1, 6:1}, 8:{15:1, 14:1, 10:1, 9:1, 11:1}, 9:{8:1, 14:1, 12:1}, 10:{12:1, 14:1, 4:1, 8:1, 11:1, 13:1}, 11:{13:1, 10:1, 8:1, 5:1, 6:1}, 12:{9:1, 10:1}, 13:{10:1, 11:1}, 14:{8:1, 9:1, 10:1}, 15:{8:1}}
	threshold = 0.000001	
	connectedComponents = ConnectedComponents.ReadAllConnectedComponentsFromFile(timeSpan)
	allNodesPairWeightDict = InitialData.InitialNodesPairWeightDict(timeSpan)
	partitionSets = []
	for connectedComponent in connectedComponents:
		print "connectedComponent size = ", len(connectedComponent)
		
		nodesPairWeightDict = {}
		for i in connectedComponent:
			nodesPairWeightDict[i] = allNodesPairWeightDict[i]

		nodesPartitionDict = {}
		for i in nodesPairWeightDict:
			nodesPartitionDict[i] = set()
			nodesPartitionDict[i].add(i)

		c = {}
		for i in nodesPairWeightDict:
			c[i] = i

		while True:
			(m, nodesWeightDict) = GetNodesWeight(nodesPairWeightDict)
			qGlobal = GetModularity(nodesWeightDict, nodesPairWeightDict, m, c)
			while True:
				isChanged = False
				for i in nodesPairWeightDict:
					gainMax = 0.0
					cMax = None
					for j in nodesPairWeightDict[i]:
						qGain = GetModularityGain(nodesWeightDict, nodesPairWeightDict, m, c, i, c[j])
						if qGain > gainMax:
							gainMax = qGain
							cMax = c[j]
					if cMax != None:
						if c[i] != cMax:
							c[i] = cMax
							isChanged = True
				if not isChanged:
					break

			newNodesPairWeightDict = {}
			for i in nodesPairWeightDict.keys():
				if c[i] not in newNodesPairWeightDict: 
					newNodesPairWeightDict[c[i]] = {}
				for j in nodesPairWeightDict[i].keys():
					newNodesPairWeightDict[c[i]][c[j]] = newNodesPairWeightDict[c[i]].get(c[j], 0) + nodesPairWeightDict[i][j]
			nodesPairWeightDict = newNodesPairWeightDict
			(m, nodesWeightDict) = GetNodesWeight(nodesPairWeightDict)

			newNodesPartitionDict = {}
			for i in c:
				if c[i] not in newNodesPartitionDict:
					newNodesPartitionDict[c[i]] = []
				newNodesPartitionDict[c[i]] = list(set(newNodesPartitionDict[c[i]]).union(set(nodesPartitionDict[i])))
			nodesPartitionDict = newNodesPartitionDict

			c = {}
			for i in nodesPairWeightDict:
				c[i] = i

			qNew = GetModularity(nodesWeightDict, nodesPairWeightDict, m, c)
			if qNew - qGlobal < threshold:
				break
			qGlobal = qNew
		partitionSets += nodesPartitionDict.values()
	partitionSetsFile = open("./temp data/PartitionSets" + timeSpan, "w")
	pickle.dump(partitionSets, partitionSetsFile)
	partitionSetsFile.close()

def ReadCommunitiesFromFile(timeSpan):
	partitionSetsFile = open("./temp data/PartitionSets" + timeSpan, "r")
	partitionSets = pickle.load(partitionSetsFile)
	partitionSetsFile.close()
	return partitionSets
if __name__ == '__main__':
	CommunityDetection("1970_1979")