#Author: Kai Huang
#Date: 2015.04.06

import Queue
import InitialData
import pickle
import os
import sys
import StringProcessing

def FindAllConnectedComponents(nodesPairWeightDict):
	nodesList = nodesPairWeightDict.keys()
	connectedComponents = []
	while len(nodesList) != 0:
		nodesInConnectedComponent = FindConnectedComponent(nodesList[0], nodesPairWeightDict)
		nodesList = list(set(nodesList).difference(nodesInConnectedComponent))
		connectedComponents.append(list(nodesInConnectedComponent))
	return connectedComponents

def FindConnectedComponent(start, nodesPairWeightDict):
	nodesInConnectedComponent = set()
	nodesInConnectedComponent.add(start)
	queue = Queue.Queue(-1)
	queue.put(start)
	while queue.empty() is not True:
		node = queue.get()
		for neighbor in nodesPairWeightDict[node]:
			if neighbor not in nodesInConnectedComponent:
				queue.put(neighbor)
				nodesInConnectedComponent.add(neighbor)
	return nodesInConnectedComponent

def WriteAllConnectedComponentsToFile(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(startTime, endTime)
	connectedComponents = FindAllConnectedComponents(nodesPairWeightDict)
	connectedComponentsFile = open("./temp data/ConnectedComponents" + timeSpan, "w")
	pickle.dump(connectedComponents, connectedComponentsFile)
	connectedComponentsFile.close()

def ReadAllConnectedComponentsFromFile(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	if os.path.exists(sys.path[0] + "\ConnectedComponents" + timeSpan):
		connectedComponentsFile = open("./temp data/ConnectedComponents" + timeSpan, "r")
		connectedComponents = pickle.load(connectedComponentsFile)
		connectedComponentsFile.close()
		return connectedComponents
	else:
		nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(startTime, endTime)
		connectedComponents = FindAllConnectedComponents(nodesPairWeightDict)
		return connectedComponents

