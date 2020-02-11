#Author: Kai Huang
#Date: 2015.04.10

import sys
sys.path.append("../tools")
import StringProcessing
import pickle

def CalWeight(timeSpan):
	lines = open("../../../data/dblp_coauthor/edges" + timeSpan + ".dblp_coauthor", "r")
	nodesPairWeightDict = {}
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		first = int(tokens[0])
		second = int(tokens[1])
		if first not in nodesPairWeightDict:
			nodesPairWeightDict[first] = {}
		nodesPairWeightDict[first][second] = nodesPairWeightDict[first].get(second, 0) + 1
	nodesPairWeightDictFile = open("../../../data/dblp_coauthor/NodesPairWeightDict" + timeSpan+ ".dblp_coauthor", "w")
	pickle.dump(nodesPairWeightDict, nodesPairWeightDictFile)
	nodesPairWeightDictFile.close()

if __name__ == '__main__':
	CalWeight("1970_1979")