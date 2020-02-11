from copy import deepcopy
import random
import numpy as np
import math
import time
import matplotlib.pyplot as plt

# #edges=[["0","1"],["1","2"],["1","3"],["1","4"],["1","5"],["2","4"],["2","3"],["2","5"],["3","4"],["3","6"],["3","8"],["6","7"],["7","8"],["5","9"],["9","10"],["9","11"],["9","12"],["9","13"],["9","14"]]
# dic1 = {"1":1,"2":2,"4":4}
# dic2 = {"1":1,"3":3,"5":5}
# edges=[["0","1"],["0","2"],["1","3"],["1","4"],["1","5"],["2","5"]]

def read_file(file_path):
    edges = []
    with open(file_path, 'r') as f:
        edges_num = 0
        while True:
            edge = f.readline()
            if not edge:
                print("total eges:", edges_num)
                break
            else:
                edges_num = edges_num + 1
                edge = edge.strip().split()
                if int(edge[0]) > int(edge[1]):
                    edges.append(list((edge[1],edge[0])))
                else:
                    edges.append(edge)
    return edges

def dictNet(edges,ver):
    net = {}
    for edge in edges:
        if edge[0] not in net.keys():
            net.setdefault(edge[0],[]).append(edge[1])
        else:
            net[edge[0]].append(edge[1])
        if edge[1] not in net.keys():
            net.setdefault(edge[1], []).append(edge[0])
        else:
            net[edge[1]].append(edge[0])
    vertice=set(net.keys())
    for s in (ver-vertice):
        net[s]=[]
    return net


def getNoLinked(net,total_node):
    L = [str(x) for x in range(total_node)]
    noLinked_set = {}
    for i in net.keys():
        dup_L = deepcopy(L)
        dup_L.remove(i)
        noLinked_list = filter(lambda n:n not in net[i],dup_L)
        newList = list(noLinked_list)
        noLinked_set[i] = newList
    print("noLinked：", noLinked_set)

def devide_train_and_test_set(edges,ratio):
    dup_edges = deepcopy(edges)
    test_set_num = int(len(edges)*ratio)
    test_set = random.sample(edges,test_set_num)
    train_set = list(filter(lambda n: n not in test_set, dup_edges))
    return train_set,test_set


def getDictDegree(net):
    degree = {}
    for i in net:
        degree[i] = len(net[i])
    return degree

# 传入一个节点的邻居的度，得到这个节点的 h-indice
def H(real):
    h=0
    r = sorted(real,reverse=True)
    for i in range(1,len(real)+1):
        if i>r[i-1]:
            h=i-1
            break
        if i==r[i-1] or i==len(real):
            h=i
            break
    return h

#cur 是字典形式存储的当前图的结构， degreeDict 是字典形式存储当前图每个节点的度
def getHIndice(cur,degreeDict,c):
    HIndice = {}
    order = 0
    HIndice["h(%s)"%order]=degreeDict
    indice = []
    for order in range(1,10):
        Hn = {}
        for i in cur:
            for j in cur[i]:
                indice.append(HIndice["h({a})".format(a=order-1)][j])
            h = H(indice)
            Hn[i] = h
            indice.clear()
        #print(Hn)
        HIndice["h({b})".format(b=order)]=Hn
        if Hn==c:
            break
    return HIndice

def getCore(net,degreeDict):
    cur=deepcopy(net)
    c={}
    for i in cur:
        if len(cur[i]) == 0:
            c[i] = 0
            cur.pop(i)
        else:
            c[i]=1
    for core in range(2,10):
        while True:
            for j in list(cur.keys()):
                if degreeDict[j]<core:
                    for index in cur:
                        if j in cur[index]:
                            cur[index].remove(j)
                    cur.pop(j)
            temp=getDictDegree(cur)
            if temp==degreeDict:
                break
            degreeDict=temp
        for item in cur:
            c[item]=core
        if len(cur)==0:
            break
    return c

#传入测试集和未连接边的 {预测边:连接概率} 的字典关系，得到AUC
def getAUC(test_set,info):
    t1=time.time()
    auc = 0
    test_set_score_info = []
    noLinked_set_score_info = []
    for i in set(info.keys()):
        if list(i) in test_set:
            test_set_score_info.append(info[i])
        else:
            noLinked_set_score_info.append(info[i])
    len_test = len(test_set_score_info)
    print("len_test------>",len_test)
    len_noLinked = len(noLinked_set_score_info)
    print("len_nolinked-------->",len_noLinked)
    print("info------>",len(info.keys()))
    test_list=sorted(test_set_score_info)
    noLinked_list = sorted(noLinked_set_score_info)
    for t in test_list:
        for n in noLinked_list:
            if t==n:
                auc = auc+0.5
            elif t>n:
                auc = auc+1
            else:
                break
    auc = auc/(len_test*len_noLinked)
    t2=time.time()
    print("AUC_time:",t2-t1)
    return auc

def createAdj(vertice,cur):
    len_vertice = len(vertice)
    init = np.zeros((len_vertice,len_vertice))
    for v in cur:
        for adj in cur[v]:
            init[int(v)][int(adj)] = 1
    return init

def getVertice(edges):
    vertice = []
    for v in edges:
        vertice = vertice+v
    return set(vertice)


def CN(adjMatrix,vertice,cur):
    CN_info = {}
    set_ver = set(vertice)
    square = adjMatrix.dot(adjMatrix)
    for v in vertice:
        notDirecLinked = set_ver-set(cur[v])
        for n in notDirecLinked:
            if int(n)>int(v):
                CN_info[(v,n)]=square[int(v)][int(n)]
    return CN_info


def AA_RA(vertice,cur,adj):
    t1=time.time()
    AA_info = {}
    RA_info = {}
    set_ver = set(vertice)
    for v in vertice:
        notLinked = set_ver-set(cur[v])
        for n in notLinked:
            if int(n)>int(v):
                total_AA = 0
                total_RA = 0
                dup_vertice = deepcopy(vertice)
                dup_vertice.remove(v)
                for j in dup_vertice:
                    if adj[int(v)][int(j)] !=0 and adj[int(j)][int(n)] != 0:
                        k_j = sum(adj[int(j)])
                        total_AA = total_AA+1/math.log(2,k_j)
                        total_RA = total_RA+1/k_j
                AA_info[(v,n)] = total_AA
                RA_info[(v,n)] = total_RA
                if (v,n) not in set(AA_info.keys()):
                    AA_info[(v,n)] = 0
                if (v, n) not in set(AA_info.keys()):
                    AA_info[(v, n)] = 0
    t2=time.time()
    print("AA_RA_time:",t2-t1)
    return AA_info,RA_info

def LRW():
    pass

filename = r"C:\Users\Tang\Desktop\data\new_test.txt"
edges = read_file(filename)
print(edges)
t1=time.time()
v=getVertice(edges)
print("vertice:",v)
n=dictNet(edges,v)
print("dict:",n)
nolink=getNoLinked(n,len(v))
tr,te=devide_train_and_test_set(edges,0.1)
print("tr:",tr)
print("te",te)
trNet = dictNet(tr,v)
print(trNet)
adj=createAdj(v,trNet)
info_cn=CN(adj,v,trNet)
print("info_CN:")
print(info_cn)
AA,RA=AA_RA(v,trNet,adj)
print(AA,RA)
t2=time.time()
print("total time:",t2-t1)
auc_RA = getAUC(te,RA)
print("RA:",auc_RA)