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

def InitialNodesPairWeightDict(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	nodesPairWeightDictFile = open("../../../data/facebook-wosn-wall/NodesPairWeightDict" + timeSpan + ".data", "r")
	nodesPairWeightDict = pickle.load(nodesPairWeightDictFile)
	nodesPairWeightDictFile.close()
	return nodesPairWeightDict

def InitialNodesList(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	nodesList = set()
	lines = open("../../../data/facebook-wosn-wall/edges" + timeSpan + ".data", "r")
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		nodesList.add(int(tokens[0]))
	lines.close()
	return nodesList

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
