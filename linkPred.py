#coding=UTF-8
'''
有向网络中的链路预测程序
'''
import train_test_split
from Metrics import evaluationMetric
from Metrics import metric
from Metrics import AUC
import networkx as nx
import numpy as np
import numpy.matlib
import time
import random


def create_vertex(nodepair_set):
    vertex_set = {}
    num = 0
    for i in nodepair_set:
        if i[0] not in vertex_set:
            vertex_set[i[0]] = num
            num += 1
        if i[1] not in vertex_set:
            vertex_set[i[1]] = num
            num += 1
    return vertex_set


def create_adjmatrix(nodepair_set, vertex_set):
    '''
                nodepair_set  [ [i,j],[p,q],....]
                根据不同的顶点对，产生不同邻接矩阵
    '''
    init_matrix = np.zeros([len(vertex_set), len(vertex_set)])

    for pair in nodepair_set:
        if pair[0] in vertex_set and pair[1] in vertex_set:
            init_matrix[vertex_set[pair[0]]] [vertex_set[pair[1]]] = 1
    return init_matrix


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


if __name__ == '__main__':

    n_folds = 10
    linklist = []
    train_list = []
    test_list = []
    # nodepair_set = [[] for i in range(0, n_folds)]
    f = open("./Datasets/temporal_sort/email-Eu-core-temporal_sorted.txt", "r")
    train_list, test_list = train_test_split.train_test_split(f, 0.8)
    # f_t = open("train.txt", "r")
    # f_te = open("test.txt", "r")
    # for line in f_t.readlines():
    #     if "%" in line:
    #         continue
    #     data = line.strip('\n').split()
    #     train_list.append([int(data[0]), int(data[1])])
    #     # linklist.append([int(data[0]), int(data[1])])
    #     # nodepair_set[random.randint(0, n_folds - 1)].append([int(data[0]), int(data[1])])
    #     # new_line = data[0] + ' ' + data[1] + ' 1\n'
    #     # f_w.write(new_line)
    # for line in f_te.readlines():
    #     if "%" in line:
    #         continue
    #     data = line.strip('\n').split()
    #     test_list.append([int(data[0]), int(data[1])])

    # train_list = []
    # for templist in nodepair_set[0:8]:
    #     train_list = train_list + templist
    # test_list = nodepair_set[9]
    nodelist = create_vertex(train_list)
    train_adj = create_adjmatrix(train_list, nodelist)
    test_adj = create_adjmatrix(test_list, nodelist)
    # print(train_adj)
    # sim_bifan = np.dot(np.dot(train_adj, train_adj.T), train_adj)
    # sim_AA = nx.adamic_adar_index(train_adj)
    # sim_RA = AA(train_adj)
    # sim_IP = IP(train_adj, 0.8)
    # sim_jaccard = Jaccard(train_adj)
    # cn_score_1 = AUC.Calculation_AUC(train_adj, test_adj, sim_cn, len(nodelist))
    # cn_score_2 = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
    sim_cn = np.dot(train_adj, train_adj)
    # cn_score = metric.auc_score(sim_cn, test_adj, train_adj, 'cc')
    # print(cn_score)
    cn_score = AUC.Calculation_AUC(train_adj, test_adj, sim_cn, len(nodelist))
    print(cn_score)
    # cn_score = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
