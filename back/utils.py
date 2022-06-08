'''

    Database interaction methods


'''
import pymongo

def init_DB():
    client = pymongo.MongoClient('localhost', 27017)
    db = client["Diplom"]
    return db["K-trees"]

def clear_DB_col(col):
    col.delete_many({})
    
def drop_DB_col(col):
    col.drop()
    
def find_docs(col,query = None):
    if query != None:
        return col.find(query) 
    else:
        return col.find()
    
def find_one_docs(col,query = None):
    if query != None:
        return col.findOne(query) 
    else:
        return col.findOne()
    
def insert_DB_col(col,mydict):
    col.insert_one(mydict)
    

'''

    App methods


'''

def makedict(G):
    nodes_arr = []
    edges_arr = []
    for node in G.nodes:
        nodes_arr.append({"id":int(node),"label":node,"title":node})
    for edge in G.edges:
        edges_arr.append({"from":int(edge[0]),"to":int(edge[1])})
    return {"nodes":nodes_arr,"edges":edges_arr}

def add_edge(f_item, s_item, G):
    G.add_node(f_item)
    G.add_node(s_item)
    G.add_edge(f_item, s_item)
    G.add_edge(s_item, f_item)


'''

    Canonical coding methods


'''


def canon_insert(constituents, instert):
    return '0' + canon_compare(constituents) + '1' if instert else canon_compare(constituents)

def canon_compare(constituents):
    return ''.join(sorted(constituents, key=lambda i: i[1:len(i)-1]))

def canon_code(adj_matrix, head, prev):
    visited = 0
    constituents = []
    for i, vertex in enumerate(adj_matrix[head].T):
        if i == prev or i == head:
            continue
        if vertex:
            visited += 1
            constituents.append(canon_code(adj_matrix, i, head))

    if not visited:
        return '01'

    return canon_insert(constituents,False if head==prev else True)


def calculate_current_root(G):
    search = True
    while search:
        adj_matrix = nx.adjacency_matrix(G).todense().tolist()
        deletion_arr = []
        for i, line in enumerate(adj_matrix):
            counter = sum(line)
            if counter == 1:
                deletion_arr.append(i)

        G.remove_nodes_from([list(G.nodes)[elem] for elem in deletion_arr])

        if len(list(G.nodes)) <= 2:
            search = False
    return list(G.nodes)

'''

    K-tree generation methods


'''

import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import math
import random
import numpy as np
from datetime import datetime
import igraph

def define_ktree_type(adj):
    G = nx.from_numpy_matrix(np.matrix(adj))
    cliques = list(nx.find_cliques(G))
    min_clique = min([len(_) for _ in cliques])
    treewidth = nx.algorithms.approximation.treewidth.treewidth_min_degree(G)[0]
    if treewidth > min_clique-1:
        return "partial " + str(treewidth) + "-tree"
    else:
        return str(treewidth) + "-tree" 

def w(n,set_n):
    numerator = math.factorial(n)
    denominator = 1
    for i,k in enumerate(set_n):
        denominator *= math.pow(i+1,k)
    for k in set_n:
        denominator *= math.factorial(k)
    return numerator/denominator

def c(n,set_n):
    sum1 = 0
    sum2 = 0
    for i in range(n):
        for j in range(n):
            sum1 += set_n[i]*set_n[j]*math.gcd(i+1, j+1)
    for i in range(n):
        sum2 += set_n[i]*((i+1)%2)
        
    return 1/2*(sum1 - sum2)
 
def g(n,all_w,all_c,all_set_n):
    sum1 = 0
    for i, set_n in enumerate(all_set_n):
        sum1 += all_w[i]*math.pow(2,all_c[i])
    return (1/math.factorial(n))*sum1

def canculate_num(n):
    all_w = []
    all_c = []
    all_set_n = [[n]]
    for i in range(2,n+1):
        all_set_n.extend(partition(n,i))
    for set_n in all_set_n:
        all_w.append(w(n,cyclic_structure(n,set_n)))
        all_c.append(c(n,cyclic_structure(n,set_n)))
    return round(g(n,all_w,all_c,all_set_n))

def weight(n,g,set_n):
    return w(n,set_n)*math.pow(2,c(n,set_n))/math.factorial(n)*g


def ktree_generator_NX(n):
    start_time = start_time = datetime.now()
    part = [[n]]
    for i in range(2,n+1):
        part.extend(partition(n,i))
    part = part[::-1]
    current_adj = []
    num = canculate_num(n)
    iter_ = 0
    max_iter = 100000
    while True:
        # a = random.random()
        # sum_ = 0
        # part_iter = 0
        # while sum_ < a:
        #     selected_part = part[part_iter]
        #     sum_ += weight(n,num,selected_part) 
        #     part_iter += 1
        selected_part = part[random.randint(0,len(part)-1)]
        cycl = cyclic_structure(n,selected_part)
        adapt_cycl = adaptive_cyclic_structure(n,cycl)
        adj = filling_adj_matrix(n,adapt_cycl)
        if check_isomorphic_NX(adj,current_adj):
            current_adj.append(adj)
        iter_ += 1
        if len(current_adj) == num or iter_ == max_iter:
            break
    
    if iter_ == max_iter:
        print('n - ' + str(n) + ' !reach iter limit! must be - ' + str(num) + ' generated - ' + str(len(current_adj)))
    else:
        print('n - ' + str(n) + ' num :' + str(num) +   ' iter :' + str(iter_))
        
    time = datetime.now() - start_time
    print(time)
    
    return time,current_adj

def ktree_generator_canonic(n):
    start_time = start_time = datetime.now()
    part = [[n]]
    for i in range(2,n+1):
        part.extend(partition(n,i))
    part = part[::-1]
    current_adj = []
    current_canonic = []
    num = canculate_num(n)
    iter_ = 0
    while True:
        # a = random.random()
        # sum_ = 0
        # part_iter = 0
        # while sum_ < a:
        #     selected_part = part[part_iter]
        #     sum_ += weight(n,num,selected_part)
        #     part_iter += 1
        selected_part = part[random.randint(0,len(part)-1)]
        cycl = cyclic_structure(n,selected_part)
        adapt_cycl = adaptive_cyclic_structure(n,cycl)
        adj = filling_adj_matrix(n,adapt_cycl)
        canonic = get_canonic(adj,n) 
        if not canonic in current_canonic:
            current_adj.append(adj)
            current_canonic.append(canonic)
        iter_ += 1
        if len(current_adj) == num:
            break
    
    print('n - ' + str(n) + ' num :' + str(num) +   ' iter :' + str(iter_))
    
    time = datetime.now() - start_time
    print(time)
    
    return time,current_adj,current_canonic

    
def get_canonic(adj,n):
    g = igraph.Graph.Adjacency(adj)
    return relabel(g,n,g.canonical_permutation())
    
def relabel(G,n,lab):
    graph_relabeled = igraph.Graph()
    graph_relabeled.add_vertices(n)
    for elem in G.get_edgelist():

        graph_relabeled.add_edges([(lab[elem[0]],lab[elem[1]])]) 
        
    pres = list(set(graph_relabeled.get_edgelist()))
    pres.sort()

    prep = str(pres).replace(',', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '')

    return prep
    


def partition(n,m):
    part = [1 for i in range(m)]
    part[0] = n - m + 1
    part_list = []
    while True:
        part_list.append(part.copy())
        if part[1] < part[0]-1:
            part[0] -= 1
            part[1] += 1
        else:
            s = part[0]-1
            for i in range(1,m):
                if part[i] < part[0] - 1:
                    break
                s += part[i]
            else:
                break
            part[i] += 1
            for j in range(1,i):
                part[j] = part[i]
                s -= part[i]
            part[0] = s
    return part_list

def cyclic_structure(n,part):
    res = [0 for _ in range(n)]
    for i in part:
        res[i-1] += 1
    return res

def adaptive_cyclic_structure(n,cycl):
    current_state = 0
    res = []
    for i,elem in enumerate(cycl):
        if elem > 0:
            steps_elem = elem
            while steps_elem > 0:
                steps_i = i
                start_state = current_state
                while steps_i > 0:
                    res.append(current_state+1)
                    current_state +=1
                    steps_i -= 1
                res.append(start_state)
                current_state +=1
                steps_elem -= 1
    return res 

def start_adj_matrix(n):
    adj = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i!=j:
                adj[i][j]=2          
    return adj.tolist()

def filling_adj_matrix(n,adapt_cycl):
    adj = start_adj_matrix(n)
    for i in range(n):
        for j in range(i):
            if adj[i][j] == 2:
                a = random.randint(0,1)
                stable_i = i
                stable_j = j
                edit_i = i
                edit_j = j
                step = True
                while step:
                    adj[edit_i][edit_j]=a
                    adj[edit_j][edit_i]=a
                    edit_i = adapt_cycl[edit_i]
                    edit_j = adapt_cycl[edit_j]
                    if edit_i == stable_i and edit_j == stable_j:
                        step = False
    return adj 

def check_isomorphic_NX(adj,current_adj):
    G1 = nx.from_numpy_matrix(np.matrix(adj))
    for elem in current_adj:
        G2 = nx.from_numpy_matrix(np.matrix(elem))
        if nx.is_isomorphic(G1, G2):
            return False
    return True

def check_isomorphic_Canonic(adj,current_adj):
    G1 = nx.from_numpy_matrix(np.matrix(adj))
    for elem in current_adj:
        G2 = nx.from_numpy_matrix(np.matrix(elem))
        if nx.is_isomorphic(G1, G2):
            return False
    return True

def draw(adj):
    graph = nx.from_numpy_matrix(np.matrix(adj) )
    pos = graphviz_layout(graph, prog="dot")
    plt.subplots()
    nx.draw(graph,pos,with_labels=True)
    plt.plot()