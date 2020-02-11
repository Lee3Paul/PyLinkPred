#Author: Kai Huang
#Date: 2015.04.20

import ConnectedComponents
import GenerateVector
import time
import InitialData
import networkx as nx
import pickle
import sys
sys.path.append("../tools")
import StringProcessing
import CommunityDetection
import LinkClustering
import AddressDictGenerator
import DataInfo

def GenerateVectors(startTime, endTime, partitionMethod = "ConnectedComponents"):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	nodesDict = InitialData.InitialNodesPairWeightDict(startTime, endTime)
	addressDict = AddressDictGenerator.ReadAddressDictFromFile() 
	if partitionMethod == "ConnectedComponents":
		connectedComponents = ConnectedComponents.ReadAllConnectedComponentsFromFile(startTime, endTime)
	elif partitionMethod == "CommunityDetection":
		connectedComponents = CommunityDetection.ReadCommunitiesFromFile(startTime, endTime)
	else:
		connectedComponents = LinkClustering.ReadAllConnectedComponentsFromFile(startTime, endTime)
	print "Read"

	vectorsDict = {}
	for nodes in connectedComponents:
		print("Components size = %d"%len(nodes))
		
		G = nx.Graph()
		componentNodesDict = {}
		for i in nodes:
			if i not in componentNodesDict:
				componentNodesDict[i] = []
			for j in nodesDict[i]:
				if j in nodes:
					componentNodesDict[i].append(j)
					G.add_edge(i, j)

		for i in xrange(0, len(nodes)):
			startTime = time.time()
			for j in xrange(i + 1, len(nodes)):
				if nodes[j] not in componentNodesDict[nodes[i]]:
					# startTime = time.time()
					paths = list(nx.all_simple_paths(G, source = nodes[i], target = nodes[j], cutoff = 6))
					# endTime = time.time()
					# print("find paths time:%f"%(endTime - startTime))
					if len(paths) != 0:
						# startTime = time.time()
						vector = GenerateVector.GenerateVector(paths, nodesDict, addressDict)
						if nodes[i] not in vectorsDict:
							vectorsDict[nodes[i]] = {}
						if nodes[j] not in vectorsDict:
							vectorsDict[nodes[j]] = {}
						vectorsDict[nodes[i]][nodes[j]] = vector
						vectorsDict[nodes[j]][nodes[i]] = vector
						# endTime = time.time()
						# print("generate vector time:%f"%(endTime - startTime))
			endTime = time.time()
			print("nodes[%s] generated, finished in %f s"%(nodes[i], endTime - startTime))

	vectorsDictFile = open("./temp data/Vectors" + timeSpan, "w")
	pickle.dump(vectorsDict, vectorsDictFile)
	vectorsDictFile.close()
	print("timeSpan%s generated"%timeSpan)

if __name__ == '__main__':
	GenerateVectors(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime, "OverlappingCommunityDetection")
	GenerateVectors(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime, "OverlappingCommunityDetection")