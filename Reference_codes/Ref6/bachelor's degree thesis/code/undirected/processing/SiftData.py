#Author: Kai Huang
#Date: 2015.04.02
#Author: Kai Huang
#Date: 2015.04.02

import sys
sys.path.append("../tools")
import StringProcessing
from DateConversion import *

def SiftData(startTime, endTime):
	timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
	lines = open("../../../data/facebook-wosn-wall/cleaned_out.data", "r")
	siftedLines= open("../../../data/facebook-wosn-wall/edges" + timeSpan + ".data", "w")
	nodePairSet = set()
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		if tokens[4] >= startTime and tokens[4] <= endTime:
			if (tokens[0], tokens[1]) not in nodePairSet:
				nodePairSet.add((tokens[0], tokens[1]))
				siftedLines.write(tokens[0] + ' ' + tokens[1] + '\n')
	siftedLines.close()