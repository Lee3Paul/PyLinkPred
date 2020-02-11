'''
数据集划分方法
'''

import numpy as np
import numpy.matlib


def train_test_split(fr, ratio):
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

    return train_list, test_list
