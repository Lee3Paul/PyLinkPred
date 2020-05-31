# coding=UTF-8
"""
数据集划分方法
"""

import numpy as np
from preprocess import handle_list_matrix
import numpy.matlib
import random
import time


def read_from_txt(f_tr, f_te):
    """
    输入：文件id
    输出：划分数据集
    """
    train_list = []
    test_list = []
    for line in f_tr.readlines():
        data = line.strip('\n').split()
        train_list.append([int(data[0]), int(data[1])])
    for line in f_te.readlines():
        data = line.strip('\n').split()
        test_list.append([int(data[0]), int(data[1])])
    node_list, max_node = handle_list_matrix.create_vertex(train_list)
    train = handle_list_matrix.create_adjmatrix(train_list, node_list, max_node)
    test = handle_list_matrix.create_adjmatrix(test_list, node_list, max_node)
    return train, test


def time_based_split(fr, ratio):
    """
    输入：文件id
    输出：划分数据集
    划分方法：直接按边数量截断，不随机选取
    """
    train_list = []
    test_list = []
    linklist = []
    link_cnt = 1
    lines = fr.readlines()
    n_link = len(lines)
    n_train = int(n_link * ratio)
    for line in lines:
        data = line.strip('\n').split()
        linklist.append([int(data[0]), int(data[1])])
        if link_cnt > n_train:
            train_list.append([int(data[0]), int(data[1])])
        else:
            test_list.append([int(data[0]), int(data[1])])
        link_cnt += 1
    node_list = handle_list_matrix.create_vertex(train_list)
    train = handle_list_matrix.create_adjmatrix(train_list, node_list)
    test = handle_list_matrix.create_adjmatrix(test_list, node_list)
    return train, test


def k_fold_split_fr(fr, n_folds):
    """
    输入：文件id，K折数量
    输出：划分数据集
    划分方法：划分为K段，每次随机选用一段作为测试集
    """
    linklist = [[] for i in range(0, n_folds)]
    lines = fr.readlines()
    for line in lines:
        data = line.strip('\n').split()
        linklist[random.randint(0, n_folds - 1)].append([int(data[0]), int(data[1])])
    train_list = []
    for templist in linklist[0:(n_folds - 2)]: # 将其中K-1份作为训练集
        train_list = train_list + templist
    test_list = linklist[n_folds - 1] # 将其中1份作为测试集
    print(len(train_list), len(test_list))
    node_list = handle_list_matrix.create_vertex(train_list)
    train = handle_list_matrix.create_adjmatrix(train_list, node_list)
    test = handle_list_matrix.create_adjmatrix(test_list, node_list)
    return train, test


def k_fold_split(linklist, n_folds):
    """
    输入：边列表，K折数量
    输出：划分数据集
    划分方法：划分为K段，每次随机选用一段作为测试集
    """
    group_linklist = [[] for i in range(0, n_folds)]
    for i in linklist:
        group_linklist[random.randint(0, n_folds - 1)].append([int(i[0]), int(i[1])])
    train_list = []
    for templist in group_linklist[0:(n_folds - 2)]: # 将其中K-1份作为训练集
        train_list = train_list + templist
    test_list = group_linklist[n_folds - 1] # 将其中1份作为测试集
    print(len(train_list), len(test_list))
    node_list = handle_list_matrix.create_vertex(train_list)
    train = handle_list_matrix.create_adjmatrix(train_list, node_list)
    test = handle_list_matrix.create_adjmatrix(test_list, node_list)
    return train, test


def k_fold_split_alter(linklist, n_folds):
    """
    输入：边列表，K折数量
    输出：划分数据集
    划分方法：划分为K段，每次随机选用一段作为测试集
    """
    group_linklist = [[] for i in range(0, n_folds)]
    for i in linklist:
        group_linklist[random.randint(0, n_folds - 1)].append([int(i[0]), int(i[1])])
    train_list = []
    for templist in group_linklist[0:(n_folds - 2)]: # 将其中K-1份作为训练集
        train_list = train_list + templist
    test_list = group_linklist[n_folds - 1] # 将其中1份作为测试集
    print(len(train_list), len(test_list))
    node_list = handle_list_matrix.create_vertex(train_list)
    train = handle_list_matrix.create_adjmatrix(train_list, node_list)
    test = handle_list_matrix.create_adjmatrix(test_list, node_list)
    return train, test


def connect_split(linklist, ratio):
    """
    输入：边列表，划分比例
    输出：划分数据集
    划分方法：保证连通性的划分
    """
    n_link = len(linklist)
    n_test = int(float(1 - ratio) * n_link)
    print(n_test)
    nodelist = handle_list_matrix.create_vertex(linklist)
    adjmatrix = handle_list_matrix.create_adjmatrix(linklist, nodelist)
    n_node = adjmatrix.shape[0]
    testmatrix = np.zeros([n_node, n_node])

    while (len(np.nonzero(testmatrix)[0]) < n_test):
        print(len(np.nonzero(testmatrix)[0]))
        index_Link = int(np.random.rand(1) * len(linklist))
        Uid1 = int(linklist[index_Link][0])
        Uid2 = int(linklist[index_Link][1])
        adjmatrix[Uid1, Uid2] = 0
        adjmatrix[Uid2, Uid1] = 0
        tempVector = adjmatrix[Uid1]
        sign = 0
        Uid1_TO_Uid2 = np.dot(tempVector, adjmatrix) + tempVector
        if Uid1_TO_Uid2[Uid2] > 0:
            sign = 1
        else:
            count = 1
            while (len((handle_list_matrix.spones(Uid1_TO_Uid2) - tempVector).nonzero()[0]) != 0):
                tempVector = handle_list_matrix.spones(Uid1_TO_Uid2)
                Uid1_TO_Uid2 = np.dot(tempVector, adjmatrix) + tempVector
                count += 1
                if Uid1_TO_Uid2[Uid2] > 0:
                    sign = 1
                    break
                if count >= adjmatrix.shape[0]:
                    sign = 0
        if sign == 1:
            linklist = np.delete(linklist, index_Link, axis=0)
            testmatrix[Uid1, Uid2] = 1
        else:
            linklist = np.delete(linklist, index_Link, axis=0)
            adjmatrix[Uid1, Uid2] = 1
    train = adjmatrix
    test = testmatrix
    DivideTime_End = time.clock()
    return train, test
