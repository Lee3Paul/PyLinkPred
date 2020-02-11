#Author: Kai Huang
#Date: 2015.04.07

import sys
sys.path.append("../tools")
import copy
import DataInfo
import InitialData
import pickle
import networkx as nx

def FindAllPaths(start, end, nodesDict):
	path = []
	paths = []
	path.append(start)
	FindAllPathsImpl(path, paths, end, nodesDict)
	return paths
def FindAllPathsImpl(path, paths, end, nodesDict):
	if path[-1] == end:
		paths.append(copy.copy(path))
		return
	elif len(path) >= DataInfo.PathLengthLimit:
		return
	else:
		for neighbor in nodesDict[path[-1]]:
			if neighbor not in path:
				path.append(neighbor)
				FindAllPathsImpl(path, paths, end, nodesDict)
				path.pop()

def IfActiveYearsOverlap(first, second, activeYearsDict):
	firstActiveYears = list(activeYearsDict[first])
	secondActiveYears = list(activeYearsDict[second])
	firstActiveYears.sort()
	secondActiveYears.sort()
	if firstActiveYears[-1] < secondActiveYears[0] or secondActiveYears[-1] < firstActiveYears[0]:
		return False
	else:
		return True

def IsNodeActiveRecently(node, activeYearsDict, currentYear):
	activeYears = list(activeYearsDict[node])
	activeYears.sort()
	return currentYear - activeYears[-1] < DataInfo.ActiveYearsLimit

# if __name__ == '__main__':
# 	#nodesDict = {1:[3, 4, 5, 6, 7], 2:[3, 4, 5, 6, 7], 3:[1, 2, 4, 5, 6, 7], 4:[1, 2, 3, 5, 6, 7], 5:[1, 2, 3, 4, 6, 7], 6:[1, 2, 3, 4, 5, 7], 7:[1, 2, 3, 4, 5, 6]}
# 	firstTimeSpan = "1970_1979"
# 	secondTimeSpan = "1980_1984"
# 	firstEnd = 1979
# 	nodesDict = InitialData.InitialNodesPairWeightDict(firstTimeSpan)
# 	nodesInPart1 = InitialData.InitialNodesList(firstTimeSpan)
# 	nodesInPart2 = InitialData.InitialNodesList(secondTimeSpan)
# 	effectiveNodes = set(nodesInPart1).intersection(set(nodesInPart2))
# 	communities = CommunityDetectionByUsingLouvain.ReadCommunitiesFromFile(firstTimeSpan)
# 	#activeYearsDict = InitialData.InitialNodesActiveYearsDict(firstTimeSpan)
# 	print "Read"
# 	for community in communities:
# 		nodes = list(effectiveNodes.intersection(community))

# 		G = nx.Graph()
# 		communityNodesDict = {}
# 		for i in community:
# 			if i not in communityNodesDict:
# 				communityNodesDict[i] = []
# 			for j in nodesDict[i]:
# 				if j in community:
# 					communityNodesDict[i].append(j)
# 					G.add_edge(i, j)

# 		for i in xrange(0, len(nodes)):
# 			#if IsNodeActiveRecently(nodes[i], activeYearsDict, 1979):
# 			pathsDict = {}
# 			for j in xrange(0, len(nodes)):
# 				if i != j and nodes[j] not in communityNodesDict[nodes[i]]:# and IsNodeActiveRecently(nodes[j], activeYearsDict, 1979) and IfActiveYearsOverlap(nodes[i], nodes[j], activeYearsDict):
# 					paths = list(nx.all_simple_paths(G, source = nodes[i], target = nodes[j], cutoff = 6))
# 					if len(paths) != 0:
# 						pathsDict[nodes[j]] = paths
# 			pathsDictFile = open("./temp data/PathsDict" + firstTimeSpan + "/" + str(nodes[i]), "w")
# 			pickle.dump(pathsDict, pathsDictFile)
# 			pathsDictFile.close()


# 	