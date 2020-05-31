# coding=UTF-8
"""
文件预处理
"""
from preprocess import handle_list_matrix
import numpy as np


def gen_linklist_from_txt(fr):
    """
    输入：文件id
    输出：边列表
    划分方法：从文件读取边列表
    """
    linklist = []
    for line in fr.readlines():
        data = line.strip('\n').split()
        linklist.append([int(data[0]), int(data[1])])
    return linklist


def gen_adjmatrix_from_linklist(linklist):
    """
    由边列表生成邻接矩阵
    :param linklist: 边列表
    :return adjmatrix: 邻接矩阵
    """
    nodelist = handle_list_matrix.create_vertex(linklist)
    adjmatrix = handle_list_matrix.create_adjmatrix(linklist, nodelist)
    return adjmatrix


