# coding=UTF-8
"""
有向网络中的链路预测程序
"""

from preprocess import train_test_split
from metrics import AUC
from algorithms import basic_measures
import numpy as np

if __name__ == '__main__':

    # NetData = np.loadtxt("./Datasets/raw/wikivote.txt")
    f = open("./Datasets/raw/wikivote.txt", "r")
    # train, test = train_test_split.k_fold_split(f, 10)
    # sim = np.dot(train, train)
    # score = AUC.Calculation_AUC(train, test, sim, train.shape[0])
    # print(score)

    # train, test = train_test_split.time_based_split(f, 0.9)
    f_tr = open("train.txt", "r")
    f_te = open("test.txt", "r")
    train, test = train_test_split.read_from_txt(f_tr, f_te)
    sim_1 = np.dot(train, train)
    score_1 = AUC.Calculation_AUC(train, test, sim_1, train.shape[0], 10000)
    print(score_1)
    sim_2 = np.dot(np.dot(train, train.T), train)
    score_2 = AUC.Calculation_AUC(train, test, sim_2, train.shape[0], 10000)
    print(score_2)
    sim_3 = basic_measures.IP(train, 0.3)
    score_3 = AUC.Calculation_AUC(train, test, sim_3, train.shape[0], 10000)
    print(score_3)


    # n_folds = 10
    # linklist = []
    # train_list = []
    # test_list = []
    # f = open("./Datasets/temporal_sort/email-Eu-core-temporal_sorted.txt", "r")
    # train_list, test_list = train_test_split.train_test_split(f, 0.8)
    # # f_t = open("train.txt", "r")
    # # f_te = open("test.txt", "r")
    # # for line in f_t.readlines():
    # #     if "%" in line:
    # #         continue
    # #     data = line.strip('\n').split()
    # #     train_list.append([int(data[0]), int(data[1])])
    # #     # linklist.append([int(data[0]), int(data[1])])
    # #     # nodepair_set[random.randint(0, n_folds - 1)].append([int(data[0]), int(data[1])])
    # #     # new_line = data[0] + ' ' + data[1] + ' 1\n'
    # #     # f_w.write(new_line)
    # # for line in f_te.readlines():
    # #     if "%" in line:
    # #         continue
    # #     data = line.strip('\n').split()
    # #     test_list.append([int(data[0]), int(data[1])])
    #
    # # train_list = []
    # # for templist in nodepair_set[0:8]:
    # #     train_list = train_list + templist
    # # test_list = nodepair_set[9]
    # nodelist = create_vertex(train_list)
    # train_adj = create_adjmatrix(train_list, nodelist)
    # test_adj = create_adjmatrix(test_list, nodelist)
    # # print(train_adj)
    # # sim_bifan = np.dot(np.dot(train_adj, train_adj.T), train_adj)
    # # sim_AA = nx.adamic_adar_index(train_adj)
    # # sim_RA = AA(train_adj)
    # # sim_IP = IP(train_adj, 0.8)
    # # sim_jaccard = Jaccard(train_adj)
    # # cn_score_1 = AUC.Calculation_AUC(train_adj, test_adj, sim_cn, len(nodelist))
    # # cn_score_2 = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
    # sim_cn = np.dot(train_adj, train_adj)
    # # cn_score = metric.auc_score(sim_cn, test_adj, train_adj, 'cc')
    # # print(cn_score)
    # cn_score = AUC.Calculation_AUC(train_adj, test_adj, sim_cn, len(nodelist))
    # print(cn_score)
    # # cn_score = evaluationMetric.cal_AUC(train_adj, test_adj, sim_cn, 10000)
