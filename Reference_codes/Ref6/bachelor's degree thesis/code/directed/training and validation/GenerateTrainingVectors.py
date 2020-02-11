from FindAllPaths import *
import CommunityDetectionByUsingLouvain
import GenerateVectors

#nodesDict = {1:[3, 4, 5, 6, 7], 2:[3, 4, 5, 6, 7], 3:[1, 2, 4, 5, 6, 7], 4:[1, 2, 3, 5, 6, 7], 5:[1, 2, 3, 4, 6, 7], 6:[1, 2, 3, 4, 5, 7], 7:[1, 2, 3, 4, 5, 6]}
firstTimeSpan = "1970_1979"
secondTimeSpan = "1980_1984"
firstEnd = 1979
nodesDict = InitialData.InitialNodesPairWeightDict(firstTimeSpan)
nodesInPart1 = InitialData.InitialNodesList(firstTimeSpan)
nodesInPart2 = InitialData.InitialNodesList(secondTimeSpan)
effectiveNodes = set(nodesInPart1).intersection(set(nodesInPart2))
communities = CommunityDetectionByUsingLouvain.ReadCommunitiesFromFile(firstTimeSpan)
#activeYearsDict = InitialData.InitialNodesActiveYearsDict(firstTimeSpan)
print "Read"

vectorsDict = {}
for community in communities:
	nodes = list(effectiveNodes.intersection(community))

	G = nx.Graph()
	communityNodesDict = {}
	for i in community:
		if i not in communityNodesDict:
			communityNodesDict[i] = []
		for j in nodesDict[i]:
			if j in community:
				communityNodesDict[i].append(j)
				G.add_edge(i, j)

	for i in xrange(0, len(nodes)):
		#if IsNodeActiveRecently(nodes[i], activeYearsDict, 1979):
		for j in xrange(0, len(nodes)):
			if i != j and nodes[j] not in communityNodesDict[nodes[i]]:# and IsNodeActiveRecently(nodes[j], activeYearsDict, 1979) and IfActiveYearsOverlap(nodes[i], nodes[j], activeYearsDict):
				paths = list(nx.all_simple_paths(G, source = nodes[i], target = nodes[j], cutoff = 6))
				if len(paths) != 0:
					vector = GenerateVectors.GenerateVectors(paths, nodesDict)
					if nodes[i] not in vectorsDict:
						vectorsDict[nodes[i]] = {}
					vectorsDict[nodes[i]][nodes[j]] = vector

vectorsDictFile = open("./temp data/Vectors" + firstTimeSpan, "w")
pickle.dump(vectorsDict, vectorsDictFile)
vectorsDictFile.close()

