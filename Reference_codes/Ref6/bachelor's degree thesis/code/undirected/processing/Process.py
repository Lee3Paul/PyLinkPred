from CleanData import *
from SiftData import *
from CalWeight import *
import sys
sys.path.append("../tools")
import DataInfo

CleanData()
SiftData(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime)
SiftData(DataInfo.secondTrainingStartTime, DataInfo.secondTrainingEndTime)
SiftData(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime)
SiftData(DataInfo.secondTestingStartTime, DataInfo.secondTestingEndTime)

CalWeight(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime)
CalWeight(DataInfo.secondTrainingStartTime, DataInfo.secondTrainingEndTime)
CalWeight(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime)
CalWeight(DataInfo.secondTestingStartTime, DataInfo.secondTestingEndTime)