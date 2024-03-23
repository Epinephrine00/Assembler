# PADE.py
# Python-Assembler Developed by Epinephrine00
# python pade.py "Path_of_Your_ASM_File.asm"
# python pade.py "Path_of_Your_ASM_File.asm" "Path_of_Output_OBJE_File.obje"
# Recommended Output File Extension : *.obje (OBJect defined by Epinephrine00)
import sys

getInstruction = lambda x:x.split()[',' in x]
getAddress = lambda x:x.split()[(',' in x)+1] if len(x.split()[',' in x:])>1 else ''

class Assembler:
    MRI = ['AND', 'ADD', 'LDA', 'STA', 'BUN', 'BSA', 'ISZ']
    NonMRI = {'CLA':0x7800, 'CLE':0x7400, 'CMA':0x7200, 'CME':0x7100,
           'CIR':0x7080, 'CIL':0x7040, 'INC':0x7020, 'SPA':0x7010,
           'SNA':0x7008, 'SZA':0x7004, 'SZE':0x7002, 'HLT':0x7001,
           'INP':0xF800, 'OUT':0xF400, 'SKI':0xF200, 'SKO':0xF100,
           'ION':0xF080, 'IOF':0xF040}
    PseudoTable = {'ORG', 'END', 'DEC', 'HEX'}
    SymbolTable = {}
    lastAddress = 0x0
    code = []
    LC = 0
    MLC = ''   # Machine Language Code

    def __init__(self, args:list):
        if len(args)>1:
            if len(args)>2:
                self.outputFilename = args[2]
            else:
                self.outputFilename = '.'.join(args[1].split('.')[:-1])+'.obje'
            self.fileReader(args[1])
        else:
            return
        
    def fileReader(self, filename:str)->None:
        with open(filename, 'r') as f:
            self.code = f.readlines()
        return
    
    def Compile(self):
        self.FirstPass()
        self.SecondPass()
        self.SaveOutputFile()
        
    def FirstPass(self):
        self.LC = 0
        for i in self.code:
            line = i.strip().upper()
            if ',' in line: #Label : Yes
                label = line.split(',')[0]
                if not label in self.SymbolTable:
                    self.SymbolTable[label] = self.LC
                    self.LC+=1
            elif getInstruction(line)=='ORG':
                self.LC = int(line.split()[1])
            elif getInstruction(line)=='END':
                return
            else:
                self.LC+=1
                
    def SecondPass(self):
        self.LC = 0
        for i in self.code:
            line = i.strip().upper()
            instruction = getInstruction(line)
            try: # list.index()는 찾는 값이 없으면 ValueError를 raise함.
                # ":="연산자, 즉... "바다코끼리 연산자(Waleus Operator)"는... PEP 572이서 정의된... 대입표현식이라는 연산입니다...
                # index에 [].index(instruction)의 값을 대입함과 동시에 index의 값이 0과 같은지 비교하는 내용입니다.
                # 파이썬 3.8 이상에서만 사용가능합니다!!!!!!!!
                if (index:=['ORG', 'END', 'DEC', 'HEX'].index(instruction))==0:
                    self.LC = int(getAddress(line))
                elif index==1:
                    return
                elif index==2:
                    self.addMLC(int(getAddress(line)))
                    self.LC+=1
                else:
                    self.addMLC(int(getAddress(line), 16))
                    self.LC+=1
            except ValueError:
                code = 0
                if instruction in Assembler.MRI:
                    code|=Assembler.MRI.index(instruction)<<12
                    code|=self.SymbolTable[getAddress(line)]
                    if len(line.split())==(3+(',' in line)) and line.split()[-1]=='I':
                        code|= 0x8000
                    self.addMLC(code)
                elif instruction in Assembler.NonMRI:
                    code = Assembler.NonMRI[instruction]
                    self.addMLC(code)
                else:
                    a = ' '*line.find(instruction)
                    b = '^'*len(instruction)
                    
                    msg = f'\n\nCompile Error: Invalid Instruction!\n    {line}\n    {a}{b}\n    There\'s no Instruction on the Instruction table \"{instruction}\"'
                    raise Exception(msg)
                self.LC+=1

    def addMLC(self, content:int):
        self.MLC += '%04X%04X'%(self.LC,content)

    def SaveOutputFile(self):
        with open(self.outputFilename, 'w') as f:
            f.write(self.MLC)

if __name__=="__main__":
    if sys.version_info.major!=3:
        print('파이썬 3버전 이외에선 실행할 수 없습니다. 3.8 이상의 파이썬 버전을 사용해주세요.')
        sys.exit()
    if sys.version_info.minor<8:
        print('파이썬 3.8 미만에선 실행할 수 없습니다. 3.8 이상의 파이썬 버전을 사용해주세요.')
        sys.exit()
    asm = Assembler(sys.argv)
    asm.Compile()