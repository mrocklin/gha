import numpy as np
from collections import defaultdict
from pylab import text, xticks, yticks, show, figure

# File IO

def load_graph(filename, process):
    """
    Loads a csv file into a dictionary with
    keys of the form   :: (node, node)
    values of the form :: value

    Takes a filename and a function to process one line
    process :: line -> (value, node, node)
    """
    file = open(filename)
    #header = file.next()

    interactions = defaultdict(lambda : 0)
    for line in file:
        n, l1, l2 = process(line)
        interactions[l1, l2] = n
    return interactions

# Graph computations
def compute_ratios(interactions, key_filter=lambda key: True):
    """
    Given a dictionary of interactions (edges) produce a dictionary of how much
    stronger each edge is relative to a uniform prior.

    ratio[a,b] = interactions[a,b] / expected_interactions[a,b]

    input
        interactions - dictionary of edges :: (node, node) : value
        key_filter   - a function to filter important nodes :: (node) -> bool

    output
        keys - the set of nodes used in the final graph :: {node}
        ratios - a dictionary of novel strength of edges :: (node, node) : float
    """
    all_keys = {a for a,b in interactions}
    keys = filter(key_filter, all_keys)
    outdegree = {key: sum(interactions[key, a]    for a in keys if a != key)
                                                  for key in keys}
    total_degree = sum(outdegree[a] for a in keys)

    def expected(a,b):
        if a!=b:
            return (1.0 * outdegree[a]*outdegree[b]
                    / (total_degree - outdegree[a]))
        else:
            return outdegree[a]

    return (keys,
            {(a,b) : interactions[a,b] / expected(a,b) if expected(a,b) else 0
                                        for a in keys
                                        for b in keys})

def make_graph(graphname, nodes, edges, size, fontsize,
               length, weight, color, penwidth, edge_exists):
    """ Construct a pydot graph

    inputs
    ------
    graphname - Title of graph :: str
    nodes - iterable of nodes :: [node]
    edges - iterable of edges :: [(node, node)]

    size - size of node function :: node -> float
    fontsize - fontsize of node fn :: node -> int

    length - length (in inches) between two nodes :: node, node -> float
    weight - importance that this length is kept  :: node, node -> float
    color  - color of an edge (can include alpha) :: node, node -> str #000000FF
    penwidth    - pen width with which to draw an edge :: node, node -> int
    edge_exists - does an edge exist?             :: node, node -> bool
    """

    # Make Graph
    import pydot
    G = pydot.Graph(graphname, graph_type='graph')
    # Nodes
    for node in nodes:
        dot_node = pydot.Node(node, width=size(node),
                                    height=size(node),
                                    fontsize=fontsize(node))
        G.add_node(dot_node)

    # Edges
    for a,b in edges:
        if a<b:
            continue
        if edge_exists(a,b):
            edge = pydot.Edge(a, b, len=length(a,b),
                                    weight=weight(a,b),
                                    color=color(a,b),
                                    penwidth=penwidth(a,b))
            G.add_edge(edge)
    return G

# Graph computation
def spectral_embedding(W, k):
    """ Spectral embedding of a graph W in k dimensions

    W[i,j] should represent the similarity between nodes i and j

    k is the dimension of the reconstruction you want

    output - an n by k array holding n points in R^k
    """

    W = W.copy()
    W[range(len(W)), range(len(W))] = 0
    W = np.matrix(W)
    d = np.squeeze(W.sum(1).A)#degrees
    D = np.matrix(np.diag(d))
    Dhalf = np.matrix(np.diag(np.sqrt(d)))
    Dhalfinv = np.matrix(np.diag(d**-.5))
    L = D-W
    Lsym = Dhalfinv*L*Dhalfinv
    evals, evects = np.linalg.eig(Lsym)
    P = Dhalfinv * evects[:,1:k+1]
    return P

# Plotting
def plot_points(points, names):
    points -= points.min(0)
    points /= points.max()

    figure()
    for x,y,s in zip(points[:,0], points[:,1], names):
        text(x,y,s)
    xticks(visible=False)
    yticks(visible=False)
    show()

def affine(i,v,I,o,O):
    """ Takes value v from range [i,I] to range [o,O]
    >>> affine(0, .5, 1, 0, 10)
    5.0
    >>> affine(0, .5, 1, 10, 20)
    15.0
    """
    return (1.0*O-o)*(1.0*v-i)/(1.0*I-i) + 1.0*o
