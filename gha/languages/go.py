import sys
import os
from lang_graph import make_lang_graph

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage:\n\t%s lang_data.csv graph.dot graph.pdf"%sys.argv[0]
        sys.exit(1)

    _, infilename, dotfilename, outfilename = sys.argv
    G = make_lang_graph(infilename)
    dotfile = open(dotfilename, 'w')
    dotfile.write(G.to_string())
    dotfile.close();

    os.system('neato -Tpdf %s -o %s'%(dotfilename, outfilename))
