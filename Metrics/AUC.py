#coding=UTF-8
'''
与Matlab中的CalcAUC_directed()结果基本一致
'''
import numpy as np
# import time


def Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum, AUCnum):
    # AUC_TimeStart = time.clock()
    
    Matrix_similarity = Matrix_similarity - Matrix_similarity * MatrixAdjacency_Train
    Matrix_NoExist = np.ones(MaxNodeNum) - MatrixAdjacency_Train - MatrixAdjacency_Test - np.eye(MaxNodeNum)
     
    Test = MatrixAdjacency_Test
    NoExist = Matrix_NoExist

    Test_num = len(np.argwhere(Test == 1))
    NoExist_num = len(np.argwhere(NoExist == 1))
      
    Test_rd = [int(x) for index, x in enumerate((Test_num * np.random.rand(1, AUCnum))[0])]
    NoExist_rd = [int(x) for index, x in enumerate((NoExist_num * np.random.rand(1, AUCnum))[0])]
    TestPre= Matrix_similarity * Test
    NoExistPre = Matrix_similarity * NoExist
    
    TestIndex = np.argwhere(Test == 1)
    Test_Data = np.array([TestPre[x[0], x[1]] for index, x in enumerate(TestIndex)]).T
    NoExistIndex = np.argwhere(NoExist == 1)
    NoExist_Data = np.array([NoExistPre[x[0], x[1]] for index, x in enumerate(NoExistIndex)]).T
    
    Test_rd = np.array([Test_Data[x] for index, x in enumerate(Test_rd)])
    NoExist_rd = np.array([NoExist_Data[x] for index, x in enumerate(NoExist_rd)])
    n1, n2 = 0, 0
    for num in range(AUCnum):
        if Test_rd[num] > NoExist_rd[num]:
            n1 += 1
        elif Test_rd[num] == NoExist_rd[num]:
            n2 += 0.5
        else:
            n1 += 0
    # AUC_TimeEnd = time.clock()
    return float(n1+n2)/AUCnum