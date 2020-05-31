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
    f = open("./Datasets/raw/wikivote.txt", "r")
    linklist = prehandle_dataset.gen_linklist_from_txt(f)
    adj_train, adj_test = train_test_split.k_fold_split(linklist, 10)

    sim_CN = np.dot(adj_train, adj_train)
    auc_CN_1 = AUC.Calculation_AUC(adj_train, adj_test, sim_CN, adj_train.shape[0], 10000)
    auc_CN_2 = metric.auc_score(sim_CN, adj_test, adj_train, 10000)
    print(auc_CN_1)
    print(auc_CN_2)

