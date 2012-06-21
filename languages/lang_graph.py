from lang import ratio, langs, interactions
from math import exp, log, sqrt
from util import make_graph

# Define properties of nodes
#   size
#   fontsize
def size(lang):
    return (interactions[lang, lang]**(1.0/2))/50
def fontsize(lang):
    return max(size(lang)*15, 12)
size_of_graph = 5 * size("Java")

# Define properties of edges
#   length
#   weight
#   color
def affinity(x):
    """ Some function that takes
    1 to scale of graph (no affinity)
    oo to 0
    1 to size_of_graph / 2
    0 to size_of_graph
    probably takes
    2 to size_of_graph / 10
    """
    #alpha = size_of_graph / pi
    #y_offset = pi/2
    #x_offset = size_of_graph / 2
    #return alpha * (atan(beta * (x - x_offset) + c)
    alpha = exp(1) * size_of_graph / 3
    return alpha * exp(-x)

def length(a,b):
    """
    Intended length between two nodes
    """

    rat = max(ratio[a,b], ratio[b,a])
    len = affinity(rat)
    len = len * size('Java')
    len = min(len, size_of_graph) # make sure we don't go beyond the bounds
    len = max(len, size(a) + size(b)) # make sure we don't collide
    return len

def weight(a,b):
    """
    How much we care about a length between two langauges

    Edges with low weights will not have their lengths respected by the
    layout engine
    """
    return interactions[a,b]

def edge_exists(a,b):
    """ Whether or not an edge exists between langs a and b """
    return interactions[a,b] > 7 and (ratio[a,b]>1 or ratio[b,a]>1)

def affine(i,v,I,o,O):
    """ Takes value v from range [i,I] to range [o,O]
    >>> affine(0, .5, 1, 0, 10)
    5.0
    >>> affine(0, .5, 1, 10, 20)
    15.0
    """
    return (1.0*O-o)*(1.0*v-i)/(1.0*I-i) + 1.0*o

def color(a, b):
    """ The color of an edge """
    val = (ratio[a,b] + ratio[b,a])/2
    alpha = affine(1, val, 3, 0, 1) # map range 1 to 3 to 0 to 1
    alpha = min(max(alpha, 0), 1)
    col  = "#000000"+hex(int(alpha*256))[2:]
    return col

def penwidth(a, b):
    return 1

G = make_graph('Languages', langs, ratio,
                size, fontsize,
                length, weight, color, penwidth, edge_exists)
