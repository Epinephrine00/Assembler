# PADE.py
# Python-Assembler Developed by Epinephrine00
# python pade.py "Path_of_Your_ASM_File.asm"
# python pade.py "Path_of_Your_ASM_File.asm" "Path_of_Output_OBJE_File.obje"
import sys

MRI = {'AND':0x0000, 'ADD':0x1000, 'LDA':0x2000, 'STA':0x3000, 
       'BUN':0x4000, 'BSA':0x5000, 'ISZ':0x6000}
RRI = {'CLA':0x7800, 'CLE':0x7400, 'CMA':0x7200, 'CME':0x7100,
       'CIR':0x7080, 'CIL':0x7040, 'INC':0x7020, 'SPA':0x7010,
       'SNA':0x7008, 'SZA':0x7004, 'SZE':0x7002, 'HLT':0x7001}
IOI = {'INP':0xF800, 'OUT':0xF400, 'SKI':0xF200, 'SKO':0xF100,
       'ION':0xF080, 'IOF':0xF040}
PseudoTable = {'ORG', 'END', 'DEC', 'HEX'}
SymbolTable = {}
lastAddress = 0x0

def isHex(s:str):
    try:
        int(s, 16)
        return True
    except:
        return False

def labelAddresser(line:str):
    global SymbolTable, lastAddress
    if line.count(','):
        label = line.split(',')[0]
        if not label in SymbolTable:
            SymbolTable[label] = lastAddress
            lastAddress += 0x10
        

    

def compileFile(path):
    lines = []
    try:
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
    except Exception as e:
        print(e)
        return
    for line in lines:
        labelAddresser(line)
        pass
    

def oneArgv(args) -> None:
    pass

def twoArgv(args) -> None:
    import os
    path = args[1]
    if os.path.isfile(path):
        compileFile(path)
    else:
        print('Invalid File Path')
        pass
    

argHandler = [oneArgv, twoArgv]

def main() -> None:
    args = sys.argv
    if (idx:=len(args))<=len(argHandler):
        argHandler[idx-1](args)

if __name__=="__main__":
    main()