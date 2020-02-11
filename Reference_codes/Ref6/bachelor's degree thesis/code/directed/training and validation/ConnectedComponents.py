#Author: Kai Huang
#Date: 2015.04.06

import Queue
import InitialData
import pickle
import os
import sys

def FindAllConnectedComponents(nodesPairWeightDict):
	nodesList = nodesPairWeightDict.keys()
	connectedComponents = []
	while len(nodesList) != 0:
		nodesInConnectedComponent = FindConnectedComponent(nodesList[0], nodesPairWeightDict)
		nodesList = list(set(nodesList).difference(nodesInConnectedComponent))
		connectedComponents.append(nodesInConnectedComponent)
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

def WriteAllConnectedComponentsToFile(timeSpan):
	nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(timeSpan)
	connectedComponents = FindAllConnectedComponents(nodesPairWeightDict)
	connectedComponentsFile = open("./temp data/ConnectedComponents_" + timeSpan, "w")
	pickle.dump(connectedComponents, connectedComponentsFile)
	connectedComponentsFile.close()

def ReadAllConnectedComponentsFromFile(timeSpan):
	if os.path.exists(sys.path[0] + "\ConnectedComponents_" + timeSpan):
		connectedComponentsFile = open("./temp data/ConnectedComponents_" + timeSpan, "r")
		connectedComponents = pickle.load(connectedComponentsFile)
		connectedComponentsFile.close()
		return connectedComponents
	else:
		nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(timeSpan)
		connectedComponents = FindAllConnectedComponents(nodesPairWeightDict)
		return connectedComponents

if __name__ == '__main__':
	WriteAllConnectedComponentsToFile("1970_1979")
