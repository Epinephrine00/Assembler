from memory import Memory

class CPU:

    # 범용 레지스터 초기화
    Accumulator = 0x0000
    AX = lambda: CPU.Accumulator
    AH = lambda: CPU.Accumulator>>8
    AL = lambda: CPU.Accumulator&0xFF

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

    # IndexPointer = 0x0000
    # IX = lambda: CPU.IndexPointer

    def SetInstructionPointer(self, address):
        CodeSegmentOffset = Memory.CodeSegmentOffset
        CPU.InstructionPointer = address + CodeSegmentOffset

    def ALU(self):
        Instruction = Memory.getWordByAddress(CPU.IP())
        InstructionType = Instruction>>12
        
        if InstructionType&0x7000:
            self.RegRefInst(Instruction)
        elif Instruction&0xF000:
            self.IOInst(Instruction)
        elif Instruction&0x8000:
            self.MemRefInst_IndAddress(Instruction)
        else:
            self.MemRefInst_DirAddress(Instruction)

    def RegRefInst(self, Instruction):
        pass
    def IOInst(self, Instruction):
        pass
    def MemRefInst_IndAddress(self, Instruction):
        pass
    def MemRefInst_DirAddress(self, Instruction):
        pass



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
        Memory.setMemory(address, CPU.AX())

    def BUN(self, address):
        CodeSegmentOffset = Memory.CodeSegmentOffset
        CPU.InstructionPointer = address + CodeSegmentOffset
    
    def BSA(self, address):
        returnAddress = CPU.IP()
        CPU.InstructionPointer = address
        Memory.pushStack(returnAddress)