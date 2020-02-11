
import community
import InitialData
import networkx as nx
import pickle

def CommunityDetection(timeSpan):
	G=nx.Graph()
	nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(timeSpan)
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
	CommunityDetection("1970_1985")