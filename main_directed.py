# coding=UTF-8
"""
有向网络链路预测
"""

from preprocess import prehandle_dataset
from preprocess import train_test_split
from metrics import metric
from metrics import AUC
from algorithms import basic_measures
import numpy as np

if __name__ == '__main__':
    # f = open("./Datasets/raw/wikivote.txt", "r")
    # linklist = prehandle_dataset.gen_linklist_from_txt(f)

    # f = open("linklist.txt", "r")
    # linklist = prehandle_dataset.gen_linklist_from_txt(f)
    # adj_train, adj_test = train_test_split.k_fold_split(linklist, 10)

    network = "PB"
    N_exp = 5

    auc_CN = np.zeros((1, 5))
    for ith_exp in range(N_exp):
        f_tr = open("./divided_dataset/"+network+"_tr_0.9_"+str(ith_exp+1)+".txt", "r")
        f_te = open("./divided_dataset/"+network+"_te_0.9_"+str(ith_exp+1)+".txt", "r")
        adj_train, adj_test = train_test_split.read_from_txt(f_tr, f_te)
        sim_CN = basic_measures.IP(adj_train, 0.5)
        auc_CN[0, ith_exp] = AUC.Calculation_AUC(adj_train, adj_test, sim_CN, adj_train.shape[0], 10000)
    print(auc_CN.mean())

