
class Memory:
    memory = []*(2**16) # 16-bit Address bus : 0~(2^16)-1 range of memory

    # Memory mode selector const : Use when Set or get Memory
    BIN = 0
    OCT = 1
    DEC = 2
    HEX = 3

    # Offsets
    CodeSegmentOffset = 0x0000

    def __init__(self, address, isPointer=False):
        self.address = address
        self.isPointer = isPointer
    
    def setMemory(mode:int=2):
        Memory.BIN