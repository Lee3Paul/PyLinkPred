#Author: Kai Huang
#Date: 2015.04.20

import sys
sys.path.append("../tools")
import StringProcessing

lines = open("../../../data/enron/sorted_out.enron", "r")
counts = {}
for line in lines:
	tokens = StringProcessing.SplitLine(line)
	counts[tokens[4]] = counts.get(tokens[4], 0) + 1
lines.close()
result = open("../../../data/enron/aggregate.enron", "w")
for key in sorted(counts.keys()):
	result.write(key + ' ' + str(counts[key]) + '\n')
result.close()