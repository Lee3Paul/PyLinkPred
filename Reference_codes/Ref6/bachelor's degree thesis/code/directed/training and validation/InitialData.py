#Author: Kai Huang
#Date: 2015.04.06

import pickle
import sys
sys.path.append("../tools")
import StringProcessing
import os

def FileWalker(path):
    filesNames = os.listdir(path)
    fullFilesNames = []
    for fileName in filesNames:
        fullFileName = os.path.join(path, fileName)
        fullFilesNames.append(fullFileName)
    return filesNames, fullFilesNames

def InitialNodesPairWeightDict(timeSpan):
	nodesPairWeightDictFile = open("../../../data/dblp_coauthor/NodesPairWeightDict" + timeSpan + ".dblp_coauthor", "r")
	nodesPairWeightDict = pickle.load(nodesPairWeightDictFile)
	nodesPairWeightDictFile.close()
	return nodesPairWeightDict

def InitialNodesList(timeSpan):
	nodesList = set()
	lines = open("../../../data/dblp_coauthor/edges"+timeSpan+".dblp_coauthor", "r")
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		nodesList.add(int(tokens[0]))
	lines.close()
	return nodesList

def InitialNodesActiveYearsDict():
	nodesDict = {}
	lines = open("../../../data/dblp_coauthor/sorted_out.dblp_coauthor", "r")
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		node = int(tokens[0])
		if node not in nodesDict:
			nodesDict[node] = set()
		nodesDict[node].add(int(tokens[4]))
	lines.close()
	return nodesDict

def InitialMatrix():
	adjacencyMatrix =\
	[
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0]
	]
	return adjacencyMatrix