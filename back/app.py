from utils import *
from flask import Flask, jsonify, request
from flask_cors import CORS
import networkx as nx


app = Flask(__name__)
CORS(app)

graph = nx.Graph()
current_root = []

@app.route('/getRandom')
def getRandom():
    return jsonify(makedict(graph))
@app.route('/addNode',methods=['POST'])
def addNode():
    data = request.get_json()
    graph.add_node(data['inputNode'])
    return jsonify(makedict(graph))
@app.route('/addEdge',methods=['POST'])
def addEdge():
    data = request.get_json()
    add_edge(data['inputEdge1'], data['inputEdge2'], graph)
    return jsonify(makedict(graph))
@app.route('/clear')
def clear():
    graph.clear()
    return jsonify(makedict(graph))
@app.route('/list',methods=['POST'])
def list():
    data = request.get_json()
    n = data['nvalue']
    k = data['kvalue']
    partial = data['partial']
    client = pymongo.MongoClient('localhost', 27017)
    db = client["Diplom"]
    col = db["K-trees"]
    end_list = []
    query = dict()
    if n != '':
        query['n']=int(n)
    if k != '' and partial != 'None':
        if partial == 'Yes':
            query['type'] = {'$regex': '^partial ' + str(k) }
        elif partial == 'No':
            query['type'] = {'$regex': '^' + str(k) }
    if partial != 'None' and k == '':
        if partial == 'Yes':
            query['type'] = {'$regex': '^partial' }
        elif partial == 'No':
            query['type'] = {'$regex': '^[^partial]' }
    if partial == 'None' and k != '':
        query['type'] = {'$regex': '.*'+str(k) }
    _list = [elem for elem in col.find(query)]
    sample = 10 if len(_list) >= 10 else len(_list)
    for elem in random.sample(_list,sample):
        graphNX = nx.from_numpy_matrix(np.matrix(elem['data']))

        adj_matrix = nx.adjacency_matrix(graphNX).todense()
        ktree_type = define_ktree_type(adj_matrix)
        if ktree_type == '1-tree':
            current_roots = calculate_current_root(graphNX.copy())
            if len(current_roots) == 1:
                canonic_code = canon_code(adj_matrix, int(current_roots[0]) - 1, int(current_roots[0]) - 1)
            else:
                canonic_codes = []
                for current_root in current_roots:
                    canonic_codes.append(canon_code(adj_matrix, int(current_root) - 1, int(current_root) - 1))
                canonic_code = '0' + ''.join(sorted(canonic_codes)) + '1'
        else:
            canonic_code = get_canonic(adj_matrix, len(adj_matrix))

        end_list.append({'description':elem['type'],'graph':makedict(graphNX),'canonic_code':canonic_code})
    return jsonify(end_list)

@app.route('/get_time_stat')
def get_time_stat():
    client = pymongo.MongoClient('localhost', 27017)
    db = client["Diplom"]
    col = db["Time_stats"]
    return jsonify([{'n':str(elem['n']),'time':math.log(elem['time'])} for elem in col.find()])

@app.route('/getCanonicalCode')
def getCanonicalCode():
    adj_matrix = nx.adjacency_matrix(graph).todense()
    ktree_type = define_ktree_type(adj_matrix)
    if ktree_type == '1-tree':
        current_roots = calculate_current_root(nx.convert_node_labels_to_integers(graph))
        if len(current_roots) == 1:
            canonic_code = canon_code(adj_matrix, int(current_roots[0]) - 1, int(current_roots[0]) - 1)
        else:
            canonic_codes = []
            G_copy = nx.convert_node_labels_to_integers(graph)
            G_copy.remove_edge(current_roots[0],current_roots[1])
            G_part = []
            for elem in nx.connected_components(G_copy):
                G_part.append(G_copy.subgraph(elem))

            for i, current_root in enumerate(current_roots):
                adj_matrix = nx.adjacency_matrix(G_part[i]).todense()
                current_root_mod = current_root if i == 0 else 0
                code = canon_code(adj_matrix, current_root_mod , current_root_mod)
                canonic_codes.append(code)
            canonic_codes.sort()
            canonic_code = canonic_codes[1] + '0' + canonic_codes[0] + '1'
        return jsonify(canonic_code)
    else:
        return jsonify(get_canonic(adj_matrix,len(adj_matrix)))


app.run()