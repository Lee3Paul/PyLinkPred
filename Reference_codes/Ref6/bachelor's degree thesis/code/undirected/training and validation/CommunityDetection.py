#Author: Kai Huang
#Date: 2015.04.20

import sys
sys.path.append("../tools")
import community
import InitialData
import StringProcessing
import networkx as nx
import pickle

def CommunityDetection(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	G=nx.Graph()
	nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(startTime, endTime)
	for i in nodesPairWeightDict:
		for j in nodesPairWeightDict[i]:
			G.add_edge(i, j, weight = nodesPairWeightDict[i][j])
	partition = community.best_partition(G)

	partitionDict = {}
	for i in partition:
		if partition[i] not in partitionDict:
			partitionDict[partition[i]] = []
		partitionDict[partition[i]].append(i)

	partitionSets = partitionDict.values()
	partitionSetsFile = open("./temp data/Communities" + timeSpan, "w")
	pickle.dump(partitionSets, partitionSetsFile)
	partitionSetsFile.close()

def ReadCommunitiesFromFile(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	partitionSetsFile = open("./temp data/Communities" + timeSpan, "r")
	partitionSets = pickle.load(partitionSetsFile)
	partitionSetsFile.close()
	return partitionSets
