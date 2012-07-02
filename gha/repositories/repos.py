import os
import sys
sys.path.insert(0, os.path.relpath(".."))

import networkx as nx
from math import log, sqrt
from collections import defaultdict
from util import compute_ratios

def clean(s):
    s = s if s[0] not in '0123456789' else '_'+s
    s = s.replace('.', '')
    s = s.replace('-', '')
    s = s.replace('node', 'node_project')
    s = s.replace('Node', 'node_project')
    s = s.lower()
    return s

def process(line):
    words = line.strip().split('\t')
    words[0] = int(words[0])
    words[1:] = map(clean, words[1:])
    return words
assert process("10\tnumpy\tC\tscipy\tPython") == \
        [10, "numpy", "c", "scipy", "python"]
assert process("5\tas-f\t1.x") == [5, "asf", "_1x"]

def edges(file):
    for line in file:
        users, a, langa, b, langb = process(line)
        yield ("%s_%s"%(a, langa), "%s_%s"%(b, langb), users)

color_dict = {"c"           : "#0000FF",
              "python"      : "#00FF00",
              "javascript"  : "#00FFFF",
              "ruby"        : "#FF0000",
              "php"         : "#FF00FF",
              "c++"         : "#FFFF00",
              "clojure"     : "#FFFFFF",
              "emacslisp"  : "#880000",
              "java"        : "#008800",
              "shell"       : "#000088"}
def color(G, node):
    lang = node.split('_')[-1]
    if lang in color_dict:
        return color_dict[lang]
    else:
        return "#000000"
assert color("", "rails_ruby") == color_dict['ruby']

def size(G, node):
    try:        users = G.edge[node][node]['users']
    except:     users = 5
    return sqrt(users)/20.

def merge(*dicts):
    return {k:v for d in dicts for k,v in d.iteritems()}
assert merge({'a':1}, {'b':2}) == {'a':1, 'b':2}

def file_to_dot(infile):
    interactions = defaultdict(lambda : 0)
    es = list(edges(infile))
    for a,b,users in es:
        interactions[a,b] = users
    keys, ratio = compute_ratios(interactions, lambda k: interactions[k,k]>5)

    G = nx.Graph()
    for a,b,users in es:
        if a > b and a in keys and b in keys and users>0 and ratio[a,b]>0:
            rat = (ratio[a,b] + ratio[b,a])/2
            G.add_edge(a,b, {'ratio': rat,
                             'users':users,
                             'connection':rat**-1})

    btwn = nx.edge_betweenness_centrality(G, weight='connection')
    GG = nx.Graph()
    GG.add_edges_from([(a, b, {'weight':val}) for (a,b), val in btwn.items()])
 #   GG.add_edges_from([(a, b, merge({'betweenness':btwn[a,b]}, G[a][b]))
 #                       for a,b in G.edges_iter()])

    for node in GG.nodes_iter():
        GG.node[node]['height'] = GG.node[node]['width'] = size(G, node)
        GG.node[node]['color'] = color(G, node)

    Gtree = nx.minimum_spanning_tree(GG)
    Gtree_dot = nx.to_pydot(Gtree)

    return Gtree_dot.to_string()

