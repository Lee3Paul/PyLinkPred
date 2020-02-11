from ConnectedComponents import *
from CommunityDetection import *
from LinkClustering import *
import sys
sys.path.append("../tools")
import DataInfo

WriteAllConnectedComponentsToFile(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime)
WriteAllConnectedComponentsToFile(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime)

CommunityDetection(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime)
CommunityDetection(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime)

OverlappingCommunityDetection(DataInfo.firstTrainingStartTime, DataInfo.firstTrainingEndTime)
OverlappingCommunityDetection(DataInfo.firstTestingStartTime, DataInfo.firstTestingEndTime)
