from cpu import CPU
from memory import Memory
import sys


def main(argc:int, argv:list) -> int:
    if argc<2:
        raise Exception("Invalid Argument")
    cpu = CPU()
    mem = Memory()
    line = ''
    with open(argv[1], 'r') as f:
        line = f.read().split('\n')[0].strip()

    instructionList = []
    for i in range(len(line)//8):
        descripter = line[i*8:(i+1)*8]
        LC, instruction = descripter[:4], descripter[4:]
        instructionList.append((int(LC,16), int(instruction,16)))
        #print(int(LC,16), int(instruction,16))

    instructionList.sort(key=lambda x:x[0])
    Memory.CodeSegmentOffset = instructionList[0][0]
    Memory.DataSegmentOffset = Memory.CodeSegmentOffset
    for i in instructionList:
        mem.setWordByAddress(i[0], i[1], mode = Memory.ABSOLUTE_ADDRESS)
    #print(mem)
    #try:
    cpu.ALU()
    #except Exception as e:
    #    print(e,'\n\n')
    print('\n\n\n-- Debug : \nAccumulator :', CPU.AX())
    print('\nMemory Values\n'+str(mem))
    


if __name__=="__main__":
    main(len(sys.argv), sys.argv)