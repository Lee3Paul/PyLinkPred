# coding=UTF-8
"""
边列表、矩阵转换
"""

import numpy as np


def create_vertex(linklist):
    """
    从边列表中获取节点列表
    :param linklist:
    :return nodelist:
    """
    nodelist = {}
    num = 0
    max_node = 0
    for i in linklist:
        if i[0] not in nodelist:
            nodelist[i[0]] = i[0]
            if i[0] > max_node:
                max_node = i[0]
        if i[1] not in nodelist:
            nodelist[i[1]] = i[1]
            if i[1] > max_node:
                max_node = i[1]
    return nodelist, max_node


def create_vertex_origin(linklist):
    """
    从边列表中获取节点列表
    :param linklist:
    :return nodelist:
    """
    nodelist = {}
    num = 0
    for i in linklist:
        if i[0] not in nodelist:
            nodelist[i[0]] = num
            num += 1
        if i[1] not in nodelist:
            nodelist[i[1]] = num
            num += 1
    return nodelist


def create_vertex_array(linklist):
    """
    从边列表中获取节点列表
    :param linklist: array格式
    :return nodelist:
    """
    nodelist = {}
    num = 0
    for i in range(len(linklist)):
        if linklist[i, 0] not in nodelist:
            nodelist[linklist[i, 0]] = num
            num += 1
        if linklist[i, 1] not in nodelist:
            nodelist[linklist[i, 1]] = num
            num += 1
    return nodelist


def create_adjmatrix(linklist, nodelist, max_node):
    """
    nodepair_set  [ [i,j],[p,q],....]
    根据不同的顶点对，产生不同邻接矩阵
    """
    init_matrix = np.zeros([max_node, max_node])

    for pair in linklist:
        if pair[0] in nodelist and pair[1] in nodelist:
            init_matrix[nodelist[pair[0]]-1][nodelist[pair[1]]-1] = 1
    return init_matrix


def create_adjmatrix_array(linklist, nodelist):
    """
    nodepair_set  [ [i,j],[p,q],....]
    根据不同的顶点对，产生不同邻接矩阵
    """
    init_matrix = np.zeros([len(nodelist), len(nodelist)])

    for i in range(len(nodelist)):
        if linklist[i, 0] in nodelist and linklist[i, 1] in nodelist:
            init_matrix[nodelist[linklist[i, 0]]] [nodelist[linklist[i, 1]]] = 1
    return init_matrix


def spones(array):
    for index in range(len(array)):
        if array[index] != 0:
            array[index] = 1
    return array