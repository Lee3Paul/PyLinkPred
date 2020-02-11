
import sys, os
from copy import copy
from operator import itemgetter
from heapq import heappush, heappop
from collections import defaultdict
from itertools import combinations, chain # requires python 2.6+
from optparse import OptionParser
import pickle
import sys
import InitialData
sys.path.append("../tools")
import StringProcessing

def swap(a,b):
    if a > b:
        return b,a
    return a,b


def Dc(m,n):
    """partition density"""
    try:
        return m*(m-n+1.0)/(n-2.0)/(n-1.0)
    except ZeroDivisionError: # numerator is "strongly zero"
        return 0.0


class HLC:
    def __init__(self,adj,edges):
        self.adj   = adj # node -> set of neighbors
        self.edges = edges # list of edges
        self.Mfactor  = 2.0 / len(edges)
        self.edge2cid = {}
        self.cid2nodes,self.cid2edges = {},{}
        self.orig_cid2edge = {}
        self.curr_maxcid = 0
        self.linkage = []  # dendrogram

        self.initialize_edges() # every edge in its own comm
        self.D = 0.0 # partition density
    
    def initialize_edges(self):
        for cid,edge in enumerate(self.edges):
            edge = swap(*edge) # just in case
            self.edge2cid[edge] = cid
            self.cid2edges[cid] = set([edge])
            self.orig_cid2edge[cid]  = edge
            self.cid2nodes[cid] = set( edge )
        self.curr_maxcid = len(self.edges) - 1
    
    def merge_comms(self,edge1,edge2,S,dendro_flag=False):
        if not edge1 or not edge2: # We'll get (None, None) at the end of clustering
            return
        cid1,cid2 = self.edge2cid[edge1],self.edge2cid[edge2]
        if cid1 == cid2: # already merged!
            return
        m1,m2 = len(self.cid2edges[cid1]),len(self.cid2edges[cid2])
        n1,n2 = len(self.cid2nodes[cid1]),len(self.cid2nodes[cid2])
        Dc1, Dc2 = Dc(m1,n1), Dc(m2,n2)
        if m2 > m1: # merge smaller into larger
            cid1,cid2 = cid2,cid1

        if dendro_flag:
            self.curr_maxcid += 1; newcid = self.curr_maxcid
            self.cid2edges[newcid] = self.cid2edges[cid1] | self.cid2edges[cid2]
            self.cid2nodes[newcid] = set()
            for e in chain(self.cid2edges[cid1], self.cid2edges[cid2]):
                self.cid2nodes[newcid] |= set(e)
                self.edge2cid[e] = newcid
            del self.cid2edges[cid1], self.cid2nodes[cid1]
            del self.cid2edges[cid2], self.cid2nodes[cid2]
            m,n = len(self.cid2edges[newcid]),len(self.cid2nodes[newcid]) 
            
            self.linkage.append( (cid1, cid2, S) )

        else:
            self.cid2edges[cid1] |= self.cid2edges[cid2]
            for e in self.cid2edges[cid2]: # move edges,nodes from cid2 to cid1
                self.cid2nodes[cid1] |= set( e )
                self.edge2cid[e] = cid1
            del self.cid2edges[cid2], self.cid2nodes[cid2]
            
            m,n = len(self.cid2edges[cid1]),len(self.cid2nodes[cid1]) 

        Dc12 = Dc(m,n)
        self.D = self.D + ( Dc12 -Dc1 - Dc2) * self.Mfactor # update partition density

    def single_linkage(self, threshold=None, w=None, dendro_flag=False):
        self.list_D = [(1.0,0.0)] # list of (S_i,D_i) tuples...
        self.best_D = 0.0
        self.best_S = 1.0 # similarity threshold at best_D
        self.best_P = None # best partition, dict: edge -> cid

        if w == None: # unweighted
            H = similarities_unweighted( self.adj ) # min-heap ordered by 1-s
        else: 
            H = similarities_weighted( self.adj, w )
        S_prev = -1
        
        # (1.0, (None, None)) takes care of the special case where the last
        # merging gives the maximum partition density (e.g. a single clique). 
        for oms,eij_eik in chain(H, [(1.0, (None, None))] ):
            S = 1-oms # remember, H is a min-heap
            if threshold and S < threshold:
                break
                
            if S != S_prev: # update list
                if self.D >= self.best_D: # check PREVIOUS merger, because that's
                    self.best_D = self.D  # the end of the tie
                    self.best_S = S
                    self.best_P = copy(self.edge2cid) # slow...
                self.list_D.append( (S,self.D) )
                S_prev = S

            self.merge_comms( eij_eik[0], eij_eik[1], S, dendro_flag )
        
        #self.list_D.append( (0.0,self.list_D[-1][1]) ) # add final val
        if threshold != None:
            return self.edge2cid, self.D
        if dendro_flag:
            return self.best_P, self.best_S, self.best_D, self.list_D, self.orig_cid2edge, self.linkage
        else:
            return self.best_P, self.best_S, self.best_D, self.list_D


def similarities_unweighted(adj):
    """Get all the edge similarities. Input dict maps nodes to sets of neighbors.
    Output is a list of decorated edge-pairs, (1-sim,eij,eik), ordered by similarity.
    """
    i_adj = dict( (n,adj[n] | set([n])) for n in adj)  # node -> inclusive neighbors
    min_heap = [] # elements are (1-sim,eij,eik)
    for n in adj: # n is the shared node
        if len(adj[n]) > 1:
            for i,j in combinations(adj[n],2): # all unordered pairs of neighbors
                edge_pair = swap( swap(i,n),swap(j,n) )
                inc_ns_i,inc_ns_j = i_adj[i],i_adj[j] # inclusive neighbors
                S = 1.0 * len(inc_ns_i&inc_ns_j) / len(inc_ns_i|inc_ns_j) # Jacc similarity...
                heappush( min_heap, (1-S,edge_pair) )
    return [ heappop(min_heap) for i in xrange(len(min_heap)) ] # return ordered edge pairs


def similarities_weighted(adj, ij2wij):
    """Same as similarities_unweighted but using tanimoto coefficient. `adj' is a dict
    mapping nodes to sets of neighbors, ij2wij is a dict mapping an edge (ni,nj) tuple
    to the weight wij of that edge.  
    """
    i_adj = dict( ( n, adj[n]|set([n]) ) for n in adj ) # node -> inclusive neighbors
    
    Aij = copy(ij2wij)
    n2a_sqrd = {}
    for n in adj:
        Aij[n,n] = 1.0*sum( ij2wij[swap(n,i)] for i in adj[n] )/len(adj[n])
        n2a_sqrd[n] = sum( Aij[swap(n,i)]**2 for i in i_adj[n] ) # includes (n,n)!
    
    min_heap = [] # elements are (1-sim,eij,eik)
    for ind,n in enumerate(adj): # n is the shared node
        #print ind, 100.0*ind/len(adj)
        if len(adj[n]) > 1:
            for i,j in combinations(adj[n],2): # all unordered pairs of neighbors
                edge_pair = swap( swap(i,n),swap(j,n) )
                inc_ns_i,inc_ns_j = i_adj[i],i_adj[j] # inclusive neighbors
                
                ai_dot_aj = 1.0*sum( Aij[swap(i,x)]*Aij[swap(j,x)] for x in inc_ns_i&inc_ns_j )
                
                S = ai_dot_aj / (n2a_sqrd[i]+n2a_sqrd[j]-ai_dot_aj) # tanimoto similarity
                heappush( min_heap, (1-S,edge_pair) )
    return [ heappop(min_heap) for i in xrange(len(min_heap)) ] # return ordered edge pairs


def read_edgelist_unweighted(filename,delimiter=None,nodetype=str):
    """reads two-column edgelist, returns dictionary
    mapping node -> set of neighbors and a list of edges
    """
    adj = defaultdict(set) # node to set of neighbors
    edges = set()
    for line in open(filename, 'U'):
        L = line.strip().split(delimiter)
        ni,nj = nodetype(L[0]),nodetype(L[1]) # other columns ignored
        if ni != nj: # skip any self-loops...
            edges.add( swap(ni,nj) )
            adj[ni].add(nj)
            adj[nj].add(ni) # since undirected
    return dict(adj), edges


def read_edgelist_weighted(filename,delimiter=None,nodetype=str,weighttype=float):
    """same as read_edgelist_unweighted except the input file now has three
    columns: node_i<delimiter>node_j<delimiter>weight_ij<newline>
    and the output includes a dict `ij2wij' mapping edge tuple (i,j) to w_ij
    """
    adj = defaultdict(set)
    edges = set()
    ij2wij = {}
    for line in open(filename, 'U'):
        L = line.strip().split(delimiter)
        ni,nj,wij = nodetype(L[0]),nodetype(L[1]),weighttype(L[2]) # other columns ignored
        if ni != nj: # skip any self-loops...
            ni,nj = swap(ni,nj)
            edges.add( (ni,nj) )
            ij2wij[ni,nj] = wij
            adj[ni].add(nj)
            adj[nj].add(ni) # since undirected
    return dict(adj), edges, ij2wij


def write_edge2cid(e2c,filename,delimiter="\t"):
    """writes the .edge2comm, .comm2edges, and .comm2nodes files"""
    
    # renumber community id's to be sequential, makes output file human-readable
    c2c = dict( (c,i+1) for i,c in enumerate(sorted(list(set(e2c.values())))) ) # ugly...
    
    cid2edges,cid2nodes = defaultdict(set),defaultdict(set) # faster to recreate here than
    for edge,cid in e2c.iteritems():                        # to keep copying all dicts
        cid2edges[cid].add( edge )                          # during the linkage...
        cid2nodes[cid] |= set(edge)
    cid2edges,cid2nodes = dict(cid2edges),dict(cid2nodes)
    
    # write list of edges for each comm, each comm on its own line
    # first entry of each line is cid
    overlappingCommunitiesFile = open("./temp data/OverlappingCommunities" + filename, "w")
    overlappingCommunities = []
    for cid in sorted(cid2edges.keys()):
        overlappingCommunity = []
        for node in cid2nodes[cid]:
            overlappingCommunity.append(int(node))
        overlappingCommunities.append(overlappingCommunity)
    pickle.dump(overlappingCommunities, overlappingCommunitiesFile)

def write_dendro(filename, orig_cid2edge, linkage):
    with open(filename + '.cid2edge.txt', 'w') as fout:
        for cid, e in orig_cid2edge.iteritems():
            fout.write("%d\t%s,%s\n" % (cid, str(e[0]), str(e[1])))

    with open(filename + '.linkage.txt', 'w') as fout:
        for x in linkage:
            fout.write('%s\n' % '\t'.join(map(str, x)))

def OverlappingCommunityDetection(startTime, endTime):
    timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
    delimiter = " "
    fullFileName = "../../../data/facebook-wosn-wall/edges" + timeSpan + ".data"
    
    nodesPairWeightDict = InitialData.InitialNodesPairWeightDict(startTime, endTime)
    ij2wij = {}
    for i in nodesPairWeightDict:
        for j in nodesPairWeightDict[i]:
            ij2wij[str(i), str(j)] = nodesPairWeightDict[i][j]

    basename = os.path.splitext(fullFileName)[0]
    adj, edges = read_edgelist_unweighted(fullFileName, delimiter=delimiter)
     
    edge2cid,S_max,D_max,list_D = HLC( adj,edges ).single_linkage( w=ij2wij )
    write_edge2cid( edge2cid, timeSpan, delimiter=delimiter )

def ReadAllConnectedComponentsFromFile(startTime, endTime):
    timeSpan = StringProcessing.GetTimeSpan(startTime, endTime)
    overlappingCommunitiesFile = open("./temp data/OverlappingCommunities" + timeSpan, "r")
    overlappingCommunities = pickle.load(overlappingCommunitiesFile)
    overlappingCommunitiesFile.close()
    return overlappingCommunities