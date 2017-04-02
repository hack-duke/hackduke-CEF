import os
import subprocess
from sys import argv

def main(arg):
    try:
        retcode = subprocess.call("open " + arg, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e


if __name__ == "__main__":
    main(argv[1])

