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


    def SetInstructionPointer(self, address):
        CodeSegmentOffset = Memory.CodeSegmentOffset
        CPU.InstructionPointer = address
    

    def ALU(self):
        Instruction = Memory.getWordByAddress(CPU.IP(), mode=Memory.CODE_SEGMENT)
        InstructionType = Instruction>>12
        
        if InstructionType&0x7000:
            self.RegRefInst(Instruction)
        elif Instruction&0xF000:
            self.IOInst(Instruction)
        elif Instruction&0x8000:
            self.MemRefInst_IndAddress(Instruction)
        else:
            self.MemRefInst_DirAddress(Instruction)
        
        if CPU.isFinished:
            return
        elif CPU.isSkipNextInstruction:
            CPU.InstructionPointer += 0x10

    def RegRefInst(self, Instruction):
        funcs = []
        if Instruction&0xF00:
            funcs = [self.CLA, self.CLE, self.CMA, self.CME]
            Instruction >>=2
        elif Instruction&0x0F0:
            funcs = [self.CIR, self.CIL, self.INC, self.SPA]
            Instruction = (Instruction>>1)&1
        elif Instruction&0x00F:
            funcs = [self.SNA, self.SZA, self.SZE, self.HLT]
            Instruction &= 1

    def IOInst(self, Instruction):
        pass
    # 입출력 및 인터럽트 등 구현에 대한 "귀찮음" 이슈로 입출력 명령어는 구현하지 않았습니다. 

    def MemRefInst_IndAddress(self, Instruction):
        address = Memory.getWordByAddress(Instruction&0xFFF)&0xFFF
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
        CPU.DataReg = Memory.getWordByAddress(address)
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
        CPU.DataReg = Memory.getWordByAddress(address)
        for i in range(16): # 반복문은 반칙같아서 쓰기 싫었지만, 숫자만 다른 같은 코드의 반복이라 "귀찮아서" 반복문 사용
            s, c = self.FullAdder(CPU.AX()>>i&1, CPU.DX()>>i&1, c)
            result |= s<<i
        # 최상위 비트(16번 비트)는 16비트 시스템에선 무시하므로 최종 캐리를 더해주지 않음
        CPU.Accumulator = result&0xffff #그래도 혹시모르니 16비트로 고정
    def LDA(self, address):
        CPU.Accumulator = Memory.getWordByAddress(address)
    
    def STA(self, address):
        Memory.setWordByAddress(address, CPU.AX())

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
        CPU.DataReg = Memory.getWordByAddress(address)
        c = 0
        result = 0
        for i in range(16): # 반복문은 반칙같아서 쓰기 싫었지만, 숫자만 다른 같은 코드의 반복이라 "귀찮아서" 반복문 사용
            s, c = self.FullAdder(CPU.DX()>>i&1, 1>>i&1, c)
            result |= s<<i
        Memory.setWordByAddress(address, result)
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
    
