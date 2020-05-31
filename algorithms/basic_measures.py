import numpy as np
import time

def AA(train_adj):
    deg_out = np.matlib.repmat(train_adj.sum(0).T, len(train_adj), 1).T
    # deg_in = np.matlib.repmat(train_adj.sum(1).T, len(train_adj),1)
    temp = train_adj/(np.log2(deg_out+1)+1)
    temp[np.isnan(temp)] = 0
    temp[np.isinf(temp)] = 0
    sim = np.dot(train_adj, temp)
    return sim


def RA(train_adj):
    deg_out = np.matlib.repmat(train_adj.sum(0).T, len(train_adj), 1).T
    # deg_in = np.matlib.repmat(train_adj.sum(1).T, len(train_adj),1)
    temp = train_adj/(deg_out+1)
    temp[np.isnan(temp)] = 0
    temp[np.isinf(temp)] = 0
    sim = np.dot(train_adj, temp)
    return sim


def IP(train_adj,sigma):
    deg_out = np.matlib.repmat(train_adj.sum(0).T, len(train_adj), 1).T
    deg_in = np.matlib.repmat(train_adj.sum(1).T, len(train_adj), 1)
    temp1 = train_adj/(deg_out+1)
    temp1[np.isnan(temp1)] = 0
    temp1[np.isinf(temp1)] = 0
    simtemp = temp1.sum(1)

    sumtemp_in = np.matlib.repmat(simtemp.T, len(train_adj), 1)
    temp2 = np.dot(train_adj.T, temp1)/(sumtemp_in.T+1)
    temp2[np.isnan(temp2)] = 0
    temp2[np.isinf(temp2)] = 0
    simtemp1 = np.dot(train_adj, temp1)
    simtemp2 = np.dot(train_adj, temp2)

    sim = sigma*simtemp1 + (1-sigma)*simtemp2
    return sim