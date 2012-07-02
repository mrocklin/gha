import numpy as np
from util import load_graph, compute_ratios

def process_lang(line):
    snum, lang1, lang2 = [item.strip('"') for item in line.strip().split('\t')]
    return int(snum), lang1, lang2

def get_lang_data(filename):
    interactions = load_graph(filename, process_lang)
    langs, ratio = compute_ratios(interactions,
                              lambda key: interactions[key,key] > 100)
    return langs, ratio
