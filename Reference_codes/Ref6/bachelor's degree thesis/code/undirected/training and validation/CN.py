#Author: Kai Huang
#Date: 2015.05.18

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
import math
from sklearn.metrics import f1_score, recall_score, precision_score, roc_auc_score
class CN:
	def __init__(self, firstStartTime, firstEndTime, secondStartTime, secondEndTime):
		self.firstStartTime = firstStartTime
		self.firstEndTime = firstEndTime
		self.secondStartTime = secondStartTime
		self.secondEndTime = secondEndTime

	def GenerateRank(self, partitionMethod = "ConnectedComponents"):
		timeSpan = StringProcessing.GetTimeSpan(self.firstStartTime, self.firstEndTime)
		nodesDict = InitialData.InitialNodesPairWeightDict(self.firstStartTime, self.firstEndTime)
		nodesDictLabel = InitialData.InitialNodesPairWeightDict(self.secondStartTime, self.secondEndTime)
		if partitionMethod == "ConnectedComponents":
			connectedComponents = ConnectedComponents.ReadAllConnectedComponentsFromFile(self.firstStartTime, self.firstEndTime)
		elif partitionMethod == "CommunityDetection":
			connectedComponents = CommunityDetection.ReadCommunitiesFromFile(self.firstStartTime, self.firstEndTime)
		else:
			connectedComponents = LinkClustering.ReadAllConnectedComponentsFromFile(self.firstStartTime, self.firstEndTime)
		pairDict = {}
		y_true = []
		y_score = []
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
						if nodes[i] not in pairDict:
							pairDict[nodes[i]] = {}
						pairDict[nodes[i]][nodes[j]] = 1
						# startTime = time.time()
						iNeighbors = []
						for neighbor in nodesDict[nodes[i]]:
							iNeighbors.append(neighbor)
						jNeighbors = []
						for neighbor in nodesDict[nodes[j]]:
							jNeighbors.append(neighbor)
						intersect = set(iNeighbors)&set(jNeighbors)
						y_score.append(len(intersect))
						if nodes[i] in nodesDictLabel and nodes[j] in nodesDictLabel[nodes[i]]:
							y_true.append(1)
						else:
							y_true.append(-1)
						# endTime = time.time()
						# print("find paths time:%f"%(endTime - startTime))
						
				endTime = time.time()
				print("nodes[%s] generated, finished in %f s"%(nodes[i], endTime - startTime))
		components = ConnectedComponents.ReadAllConnectedComponentsFromFile(self.firstStartTime, self.firstEndTime)
		for component in components:
			for i in component:
				for j in component:
					if i != j:
						if i not in pairDict or (i in pairDict and j not in pairDict[i]):
							if i not in nodesDict or (i in nodesDict and j not in nodesDict[i]):
								if i in nodesDictLabel and j in nodesDictLabel[i]:
									y_true.append(1)
								else:
									y_true.append(-1)
								y_score.append(0)
		return y_true, y_score

	def Validate(self, y_true, y_score):
		print "roc", roc_auc_score(y_true, y_score)

		y_tuple = []
		for i in xrange(0, len(y_true)):
			y_tuple.append((y_score[i], y_true[i]))
		y_tuple.sort(cmp=lambda x,y:-cmp(x[0],y[0]))
		positiveCount = 0
		for i in xrange(0, 50):
			if y_tuple[i][1] == 1:
				positiveCount += 1
			print "p = ", positiveCount, "L = ", i + 1, "p/L = ", positiveCount / float(i + 1) 

if __name__ == '__main__':
	cn = CN(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime, DataInfo.secondTestingStartTime, DataInfo.secondTestingEndTime)
	y_true, y_score = cn.GenerateRank("ConnectedComponents")
	cn.Validate(y_true, y_score)