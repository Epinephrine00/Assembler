from cpu import CPU
from memory import Memory
import sys


def main(argc:int, argv:list) -> int:
    print(argc, argv)
    if argc<2:
        raise Exception("Invalid Argument")
    with open(argv[1], 'r') as f:
        print("")
    


if __name__=="__main__":
    main(len(sys.argv), sys.argv)