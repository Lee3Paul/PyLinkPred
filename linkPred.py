from metrics import evaluationMetric
from metrics import metric
from metrics import AUC
import networkx as nx
import numpy as np
import numpy.matlib
import time
import random

# ig = nx.DiGraph()

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

n_folds = 10
linklist = []
nodepair_set = [[] for i in range(0, n_folds)]

# with open("./datasets/wikivote_sorted.txt","r") as f_r:
# with open("./datasets/ucirvine_sorted.txt","r") as f_r:
with open("./datasets/dnc_sorted.txt", "r") as f_r:
    lines = f_r.readlines()
    for line in lines:
        if "%" in line:
            continue
        data = line.strip('\n').split()
        linklist.append([int(data[0]), int(data[1])])
        nodepair_set[random.randint(0, n_folds - 1)].append([int(data[0]), int(data[1])])
        # new_line = data[0] + ' ' + data[1] + ' 1\n'
        # f_w.write(new_line)

    train_list = []
    for templist in nodepair_set[0:8]:
        train_list = train_list + templist
    test_list = nodepair_set[9]
    nodelist = create_vertex(linklist)
    train_adj = create_adjmatrix(train_list, nodelist)
    test_adj = create_adjmatrix(test_list, nodelist)
    # print(train_adj)
    sim_cn = np.dot(train_adj, train_adj)
    sim_bifan = np.dot(np.dot(train_adj, train_adj.T), train_adj)
    sim_AA = nx.adamic_adar_index(train_adj)
    sim_RA = AA(train_adj)
    sim_IP = IP(train_adj, 0.8)
    # sim_jaccard = Jaccard(train_adj)
    # cn_score_1 = AUC.Calculation_AUC(train_adj, test_adj, sim_cn, len(nodelist))
    # cn_score_2 = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
    cn_score_3 = metric.auc_score(sim_cn, test_adj, train_adj,'cc')
    # RA_score_1 = AUC.Calculation_AUC(train_adj, test_adj, sim_RA, len(nodelist))
    # RA_score_2 = evaluationMetric.cal_AUC(train_adj, test_adj, sim_RA, 10000)
    AA_score_3 = metric.auc_score(sim_AA, test_adj, train_adj, 'cc')
    RA_score_3 = metric.auc_score(sim_RA, test_adj, train_adj, 'cc')
    # bifan_score_1 = AUC.Calculation_AUC(train_adj, test_adj, sim_bifan, len(nodelist))
    # bifan_score_2 = evaluationMetric.cal_AUC(train_adj, test_adj, sim_bifan, 10000)
    bifan_score_3 = metric.auc_score(sim_bifan, test_adj, train_adj,'cc')

    IP_score = metric.auc_score(sim_IP, test_adj, train_adj, 'cc')
    # print(cn_score_1)
    # print(cn_score_2)
    print(cn_score_3)
    print(AA_score_3)
    # print(RA_score_1)
    # print(RA_score_2)
    print(RA_score_3)
    # print(bifan_score_1)
    # print(bifan_score_2)
    print(bifan_score_3)
    print(IP_score)
    # cn_score = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
    # cn_precision = evaluationMetric.cal_precision(train_adj, test_adj, sim_cn, 20)
    # jc_score = evaluationMetric.cal_AUC(train_adj, test_adj, sim_jaccard, 10000)
    # jc_precision = evaluationMetric.cal_precision(train_adj, test_adj, sim_cn, 20)
    # # score = metrics.auc_score(sim_cn, test_adj, train_adj)
    # print(cn_score)
    # print(cn_precision)
    # print(jc_score)
    # print(jc_precision)