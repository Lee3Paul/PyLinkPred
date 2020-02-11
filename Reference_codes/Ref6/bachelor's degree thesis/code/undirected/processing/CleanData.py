#Author: Kai Huang
#Date: 2015.04.01

import sys
sys.path.append("../tools")
import DateConversion
import StringProcessing

def CleanData():
	#read
	lines = open("../../../data/facebook-wosn-wall/out.data", "r")
	nodes = {}
	for line in lines:
		tokens = StringProcessing.SplitLine(line)
		if tokens[0] != tokens[1]:
			if int(tokens[0]) not in nodes:
				nodes[int(tokens[0])] = []
			newLine = "".join([tokens[0], ' ', tokens[1], ' ', tokens[2], ' ', tokens[3], ' ', DateConversion.SecsToDateString(int(tokens[3])), '\n'])
			nodes[int(tokens[0])].append(newLine)
			
			if int(tokens[1]) not in nodes:
				nodes[int(tokens[1])] = []
			newLine = "".join([tokens[1], ' ', tokens[0], ' ', tokens[2], ' ', tokens[3], ' ', DateConversion.SecsToDateString(int(tokens[3])), '\n'])
			nodes[int(tokens[1])].append(newLine)
	lines.close()
	#write
	sortedLines = open("../../../data/facebook-wosn-wall/cleaned_out.data", "w")
	for i in nodes:
		for j in nodes[i]:
			sortedLines.write(j)
	sortedLines.close()