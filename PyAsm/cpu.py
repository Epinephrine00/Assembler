from memory import Memory
from data import Stack

class CPU:

    # 범용 레지스터 초기화
    Accumulator = 0x0000
    AX = lambda: CPU.Accumulator
    AH = lambda: CPU.Accumulator>>8
    AL = lambda: CPU.Accumulator&0xFF
    ExtendedAccumulator = 0x0000
    EAX = lambda: CPU.ExtendedAccumulator
    EAH = lambda: CPU.ExtendedAccumulator>>8
    EAL = lambda: CPU.ExtendedAccumulator&0xFF

    BaseReg = 0x0000
    BX = lambda: CPU.BaseReg
    BH = lambda: CPU.BaseReg>>8
    BL = lambda: CPU.BaseReg&0xFF

    CountReg = 0x0000
    CX = lambda: CPU.CountReg
    CH = lambda: CPU.CountReg>>8
    CL = lambda: CPU.CountReg&0xFF

    DataReg = 0x0000
    DX = lambda: CPU.DataReg
    DH = lambda: CPU.DataReg>>8
    DL = lambda: CPU.DataReg&0xFF


    # 강의 내용상, 스택 영역이 없는 16비트 CPU를 상정하고 있으므로
    # 스택 포인터 (SP) 및 베이스 포인터(BP) 레지스터는 갖지 않는다. 
    # 또한 SI/DI 레지스터는 현 단계에서 필요치 않다고 판단하여 추가하지 않았다. 
    InstructionPointer = 0x0000
    IP = lambda: CPU.InstructionPointer


    # CPU 제어 변수(작동 알고리즘을 구현하기 위한 변수들)
    InstructionPointerStackForBranches = Stack()
    #isBranch = False    # banch 관리를 위해 선언하려 한 두 변수였으나, 놀랍게도(당연하게도) 파이썬은 이미 branch가 잘 구현되어있는 고급 언어이므로 그냥 재귀를 이용하겠습니다
    isSkipNextInstruction = False
    isFinished = False
    # 각각의 값을 핸들링하는 메소드를 구현하고, True일 때 ALU에서 적당히 처리하도록 구현.

    AccessableMemory = Memory()


    def SetInstructionPointer(self, address):
        CodeSegmentOffset = Memory.CodeSegmentOffset
        CPU.InstructionPointer = address
    

    def ALU(self):
        Instruction = CPU.AccessableMemory.getWordByAddress(CPU.IP(), mode=Memory.CODE_SEGMENT)
        InstructionType = (Instruction>>12)&0xF
        
        if InstructionType==0x7:
            self.RegRefInst(Instruction)
        elif Instruction==0xF:
            self.IOInst(Instruction)
        elif Instruction==0x8:
            self.MemRefInst_IndAddress(Instruction)
        else:
            self.MemRefInst_DirAddress(Instruction)
        
        if CPU.isFinished:
            return
        elif CPU.isSkipNextInstruction:
            CPU.InstructionPointer += 0x10
        CPU.InstructionPointer += 0x10
        self.ALU()
        return

    def RegRefInst(self, Instruction):
        func = {0x7800:self.CLA, 0x7400:self.CLE, 0x7200:self.CMA, 0x7100:self.CME, 
                 0x7080:self.CIR, 0x7040:self.CIL, 0x7020:self.INC, 0x7010:self.SPA, 
                 0x7008:self.SNA, 0x7004:self.SZA, 0x7002:self.SZE, 0x7001:self.HLT}[Instruction]
        func()

    def IOInst(self, Instruction):
        pass
    # 입출력 및 인터럽트 등 구현에 대한 "귀찮음" 이슈로 입출력 명령어는 구현하지 않았습니다. 

    def MemRefInst_IndAddress(self, Instruction):
        address = CPU.AccessableMemory.getWordByAddress(Instruction&0xFFF)&0xFFF
        newInstruction = (Instruction&0x7000)|address
        self.MemRefInst_DirAddress(newInstruction)
        
    def MemRefInst_DirAddress(self, Instruction):
        address = Instruction&0xFFF
        func = (Instruction>>12)&0xF
        [self.AND, self.ADD, self.LDA, self.STA, self.BUN, self.BSA, self.ISZ][func](address)

    def skipNextInstruction(self):
        CPU.isSkipNextInstruction = True
    
    def Halt(self):
        CPU.isFinished = True



    def AND(self, address):
        CPU.DataReg = CPU.AccessableMemory.getWordByAddress(address)
        CPU.Accumulator = CPU.AX() & CPU.DX()

    def FullAdder(self, a, b, cin):
        a = a&1
        b = b&1
        cin = cin&1
        s = (a^b)^cin
        cout = (a&b) | ((a^b)&cin)
        return (s, cout) #절대로 사칙연산 안쓰기
    def ADD(self, address):
        result = 0
        c = 0
        CPU.DataReg = CPU.AccessableMemory.getWordByAddress(address)
        for i in range(16): # 반복문은 반칙같아서 쓰기 싫었지만, 숫자만 다른 같은 코드의 반복이라 "귀찮아서" 반복문 사용
            s, c = self.FullAdder(CPU.AX()>>i&1, CPU.DX()>>i&1, c)
            result |= s<<i
        # 최상위 비트(16번 비트)는 16비트 시스템에선 무시하므로 최종 캐리를 더해주지 않음
        CPU.Accumulator = result&0xffff #그래도 혹시모르니 16비트로 고정
    def LDA(self, address):
        CPU.Accumulator = CPU.AccessableMemory.getWordByAddress(address)
    
    def STA(self, address):
        CPU.AccessableMemory.setWordByAddress(address, CPU.AX())

    def BUN(self, address):
        CPU.InstructionPointer = address
        self.ALU()
        self.Halt()

    def BSA(self, address):
        CPU.InstructionPointerStackForBranches.push(CPU.IP())
        CPU.InstructionPointer = address
        self.ALU()
        CPU.InstructionPointer = CPU.InstructionPointerStackForBranches.pop()
    
    def ISZ(self, address):
        CPU.DataReg = CPU.AccessableMemory.getWordByAddress(address)
        c = 0
        result = 0
        for i in range(16): # 반복문은 반칙같아서 쓰기 싫었지만, 숫자만 다른 같은 코드의 반복이라 "귀찮아서" 반복문 사용
            s, c = self.FullAdder(CPU.DX()>>i&1, 1>>i&1, c)
            result |= s<<i
        CPU.AccessableMemory.setWordByAddress(address, result)
        if not result:
            self.skipNextInstruction()
    

    def CLA(self):
        CPU.Accumulator = 0
    def CLE(self):
        CPU.ExtendedAccumulator = 0
    def CMA(self): #this may occur bug (파이썬 자료형의 한계로 인해 이게 제대로 작동할지 의문임. C였으면 그냥 short형(16비트정수)썼으면 됐는데 파이썬은 그런거 없어서;;)
        CPU.Accumulator = ~CPU.Accumulator
    def CME(self): #this may occur bug
        CPU.ExtendedAccumulator = ~CPU.ExtendedAccumulator
    def CIR(self):
        CPU.Accumulator = (CPU.AX()>>1) | ((CPU.AX()&1)<<15)
    def CIL(self):
        CPU.Accumulator = (CPU.AX()<<1) | ((CPU.AX()>>15)&1)
    def INC(self):
        c = 0
        result = 0
        for i in range(16): # 반복문은 반칙같아서 쓰기 싫었지만, 숫자만 다른 같은 코드의 반복이라 "귀찮아서" 반복문 사용
            s, c = self.FullAdder(CPU.AX()>>i&1, 1>>i&1, c)
            result |= s<<i
        CPU.Accumulator = result
    def SPA(self):
        if not ((CPU.AX()>>15)&1):
            self.skipNextInstruction()
    def SNA(self):
        if (CPU.AX()>>15)&1:
            self.skipNextInstruction()
    def SZA(self):
        if ~CPU.AX():
            self.skipNextInstruction()
    def SZE(self):
        if ~CPU.EAX():
            self.skipNextInstruction()
    def HLT(self):
        self.Halt()
    

# 테스트 코드
if __name__=="__main__":
    cpu = CPU()
    mem = Memory()
    Memory.CodeSegmentOffset = 0
    mem.setWordByAddress(0x0000, 0x2000, mode = Memory.CODE_SEGMENT)
    mem.setWordByAddress(0x0010, 0x1010, mode = Memory.CODE_SEGMENT)
    mem.setWordByAddress(0x0020, 0x3020, mode = Memory.CODE_SEGMENT)
    mem.setWordByAddress(0x0030, 0x7001, mode = Memory.CODE_SEGMENT)
    Memory.DataSegmentOffset = 0x100
    mem.setWordByAddress(0x0000, 0x001A)
    mem.setWordByAddress(0x0010, 0x0023)
    try:
        cpu.ALU()
    except Exception as e:
        print(e,'\n\n')
    print('\nAccumulator :', CPU.AX())
    print('\nMemory Values\n'+str(mem))

"""
테스트용 기계어 코드(및 그 어셈블리 표기)
LDA 0x000  -> 0x0000 : 2000 
ADD 0x010  -> 0x0010 : 1010
STA 0x020  -> 0x0020 : 3020
HLT        -> 0x0030 : 7001
아직 어셈블러는 안만들어서
직접 기계어로 번역 & 메모리 할당해서 돌려봄
"""