from memory import Memory


class CPU:

    __InstructionTable = {}

    # Universal Registor
    __Accumulator = 0x0000
    AX = lambda: CPU.__Accumulator
    AH = lambda: CPU.__Accumulator>>8
    AL = lambda: CPU.__Accumulator&0xFF

    __BaseReg = 0x0000
    BX = lambda: CPU.__BaseReg

    __CountReg = 0x0000
    CX = lambda: CPU.__CountReg

    __DataReg = 0x0000
    DX = lambda: CPU.__DataReg

    __InstructionPointer = 0x0000
    IP = lambda: CPU.__InstructionPointer

    def SetInstructionPointer(address):
        CodeSegmentOffset = Memory.CodeSegmentOffset
        CPU.__InstructionPointer = address + CodeSegmentOffset

    def ALU():
        Instruction = Memory.getDataAt(CPU.IP())
        