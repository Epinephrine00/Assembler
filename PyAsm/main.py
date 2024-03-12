import sys


def runFileWithPath(path):
    lines = []
    try:
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
    except Exception as e:
        print(e)
        return
    

def oneArgv(args) -> None:
    pass

def twoArgv(args) -> None:
    import os
    path = args[1]
    if os.path.isfile(path):
        runFileWithPath(path)
    else:
        print('Invalid File Path')
        pass
    

argHandler = [oneArgv, twoArgv]

def main() -> None:
    args = sys.argv
    if (idx:=len(args))<=len(argHandler):
        argHandler[idx-1](args)

if __name__=="__main__":
    #f = open("asdf.a", "wb")
    #f.write(b"asdf")
    #f.close()
    main()