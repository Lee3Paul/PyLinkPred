import numpy as np
import time


def CN(train_adj):
    """
    Common Neighbors index
    :param train_adj:
    :return sim:
    """
    return np.dot(train_adj, train_adj)


def AA(train_adj):
    """
    Adamic-Adar index
    :param train_adj:
    :return sim:
    """
    deg_out = np.matlib.repmat(train_adj.sum(1).T, len(train_adj), 1).T
    # deg_in = np.matlib.repmat(train_adj.sum(0).T, len(train_adj),1)
    temp = train_adj/(np.log2(deg_out+1)+1)
    temp[np.isnan(temp)] = 0
    temp[np.isinf(temp)] = 0
    return np.dot(train_adj, temp)


def RA(train_adj):
    """
    Resource Allocation index
    :param train_adj:
    :return sim:
    """
    deg_out = np.matlib.repmat(train_adj.sum(1).T, len(train_adj), 1).T
    # deg_in = np.matlib.repmat(train_adj.sum(0).T, len(train_adj), 1)
    temp = train_adj/(deg_out+1)
    temp[np.isnan(temp)] = 0
    temp[np.isinf(temp)] = 0
    return np.dot(train_adj, temp)


def PA(train_adj):
    """
    Preference Attachment index
    :param train_adj:
    :return sim:
    """
    deg_out = np.matlib.repmat(train_adj.sum(1).T, len(train_adj), 1).T
    deg_in = np.matlib.repmat(train_adj.sum(0).T, len(train_adj), 1)
    return deg_out*deg_in


def LP(train_adj, alpha=0.01):
    """
    Local Path index
    :param train_adj:
    :param alpha: adjusting parameter
    :return sim:
    """
    temp1 = np.dot(train_adj, train_adj)
    temp2 = np.dot(train_adj, np.dot(train_adj, train_adj))
    return temp1 + alpha*temp2


def Bifan(train_adj):
    """
    Local Path index
    :param train_adj:
    :return sim:
    """
    return np.dot(train_adj, np.dot(train_adj.T, train_adj))


def Katz(train_adj, alpha=0.01):
    """
    Katz index
    :param train_adj:
    :param alpha: adjusting parameter
    :return:
    """
    I_eye = np.eye(train_adj.shape[0])
    return np.linalg.inv(I_eye-alpha*train_adj)-I_eye


def LO(train_adj, alpha=0.01):
    """
    Linear Optimization index
    :param train_adj:
    :param alpha: adjusting parameter
    :return:
    """
    I_eye = np.eye(train_adj.shape[0])
    temp1 = np.dot(train_adj.T, train_adj)
    temp2 = np.linalg.inv(alpha*temp1+I_eye)
    return np.dot(train_adj, alpha*np.dot(temp2, temp1))


def IP(train_adj, sigma=0.5):
    """
    Investment-Profit index
    :param train_adj:
    :param sigma: adjusting parameter
    :return sim:
    """
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
    return sigma*simtemp1 + (1-sigma)*simtemp2