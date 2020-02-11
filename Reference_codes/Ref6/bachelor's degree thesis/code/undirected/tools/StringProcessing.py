#Author: Kai Huang
#Date: 2015.04.02

def SplitLine(line):
	tokens = line.split()
	return tokens
	
def GetTimeSpan(startTime, endTime):
	return startTime + "_" + endTime