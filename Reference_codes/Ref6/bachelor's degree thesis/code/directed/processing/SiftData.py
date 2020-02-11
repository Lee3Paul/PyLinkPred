#Author: Kai Huang
#Date: 2015.04.20

import sys
sys.path.append("../tools")
import StringProcessing
lines = open("../../../data/dblp_coauthor/sorted_out.dblp_coauthor", "r")
lines1970_1979 = open("../../../data/dblp_coauthor/edges1970_1979.dblp_coauthor", "w")
lines1980_1984 = open("../../../data/dblp_coauthor/edges1980_1984.dblp_coauthor", "w")
lines1970_1985 = open("../../../data/dblp_coauthor/edges1970_1985.dblp_coauthor", "w")
lines1986_1990 = open("../../../data/dblp_coauthor/edges1986_1990.dblp_coauthor", "w")
for line in lines:
	tokens = StringProcessing.SplitLine(line)
	if tokens[4] <= "1979":
		lines1970_1979.write(tokens[0] + ' ' + tokens[1] + '\n')
	if tokens[4] >= "1980" and tokens[4] <= "1984":
		lines1980_1984.write(tokens[0] + ' ' + tokens[1] + '\n')
	if tokens[4] <= "1985":
		lines1970_1985.write(tokens[0] + ' ' + tokens[1] + '\n')		
	if tokens[4] >= "1986" and tokens[4] <= "1990":
		lines1986_1990.write(tokens[0] + ' ' + tokens[1] + '\n')
lines1970_1979.close()
lines1980_1984.close()
lines1970_1985.close()
lines1986_1990.close()