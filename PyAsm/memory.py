
class Memory:
    memory = [0]*(2**16) # 16-bit Address bus : 0~(2^16)-1 range of memory

    # Memory mode selector const : Use when Set or get Memory
    BIN = 0
    OCT = 1
    DEC = 2
    HEX = 3

    # Offsets
    CodeSegmentOffset = 0x0000
    DataSegmentOffset = 0x0000


    def __init__(self, address, isPointer=False):
        self.address = address
        self.isPointer = isPointer
    
    def setMemory(self, address, value):
        pass

    def pushStack(self, value):
        pass

    def getWordByAddress(self, address):
        result = ((Memory.memory[address]&1)<<7) | ((Memory.memory[address+1]&1)<<6) | ((Memory.memory[address+2]&1)<<5) | ((Memory.memory[address+3]&1)<<4) | ((Memory.memory[address+4]&1)<<3) | ((Memory.memory[address+5]&1)<<2) | ((Memory.memory[address+6]&1)<<1)| (Memory.memory[address+7]&1)
