from utils import *

ktree_arr_nx = []
for i in range(1,9):
    time,arr = ktree_generator_NX(i)
    ktree_arr_nx.extend(arr)

count_dict_nx = {
    '0-tree':0,
    '1-tree':0,
    '2-tree':0,
    '3-tree':0,
    '4-tree':0,
    '5-tree':0,
    '6-tree':0,
    '7-tree':0,
    'partial 1-tree':0,
    'partial 2-tree':0,
    'partial 3-tree':0,
    'partial 4-tree':0,
    'partial 5-tree':0,
    'partial 6-tree':0,
    'partial 7-tree':0,
    'partial 8-tree':0
}
for elem in ktree_arr_nx:
    G = nx.from_numpy_matrix(np.matrix(elem))
    if nx.is_connected(G):
        count_dict_nx[define_ktree_type(elem)] += 1

ktree_arr = []
ktree_canonic = []
for i in range(1,11):
    time,arr,canonic = ktree_generator_canonic(i)
    ktree_arr.extend(arr)
    ktree_canonic.extend(canonic)

count_dict = {
    '0-tree':0,
    '1-tree':0,
    '2-tree':0,
    '3-tree':0,
    '4-tree':0,
    '5-tree':0,
    '6-tree':0,
    '7-tree':0,
    'partial 1-tree':0,
    'partial 2-tree':0,
    'partial 3-tree':0,
    'partial 4-tree':0,
    'partial 5-tree':0,
    'partial 6-tree':0,
    'partial 7-tree':0,
    'partial 8-tree':0
}
counted = 0
for elem in ktree_arr:
    G = nx.from_numpy_matrix(np.matrix(elem))
    if nx.is_connected(G):
        count_dict[define_ktree_type(elem)] += 1
        counted += 1


for adj in ktree_arr[0:50]:
    draw(adj)