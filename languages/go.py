import os
from lang_graph import G
file = open('lang.dot', 'w')
file.write(G.to_string())
file.close();
os.system('neato -Tpdf lang.dot -o lang.pdf')
