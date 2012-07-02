from repos import file_to_dot
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage:\n\t%s infile.csv outfile.dot"%(sys.argv[0])
        sys.exit(0)

    _, infilename, outfilename = sys.argv
    infile = open(infilename)
    outfile = open(outfilename, 'w')

    outfile.write(file_to_dot(infile))
    outfile.close()
