import numpy as np
from util import load_graph, compute_ratios

def process_lang(line):
    snum, lang1, lang2 = [item.strip('"') for item in line.strip().split(',')]
    return int(snum), lang1, lang2

interactions = load_graph('language_connections', process_lang)

langs, ratio = compute_ratios(interactions,
                              lambda key: interactions[key,key] > 100)
