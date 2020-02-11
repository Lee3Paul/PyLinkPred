#Author: Kai Huang
#Date: 2015.04.01

import sys
sys.path.append("../tools")
import time
def SecsToYear(secs):
	if secs >= 0:
		return time.strftime("%Y",time.gmtime(secs))
	else:
		return "0000"

def SecsToDatetime(secs):
	if secs >= 0:
		return time.strftime("%Y/%m",time.gmtime(secs))
	else:
		return "0000"