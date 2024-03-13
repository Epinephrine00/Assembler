class Memory:
    space, words = 4096, 16
    memory = [0]*(space*words)

    # Offsets
    CodeSegmentOffset = 0x0000
    DataSegmentOffset = 0x0000

    # Mode Const
    ABSOLUTE_ADDRESS = -1
    DATA_SEGMENT = 0
    CODE_SEGMENT = 1


    def __init__(self):
        pass

    
    def setBit(self, address, value):
        Memory.memory[address] = value&1
    def getBit(self, address):
        return Memory.memory[address]&1

    def setWordByAddress(self, address, value):
        for i in range(Memory.words):
            Memory.memory[address+i] = (value>>((Memory.words-1)-i))&1
    def getWordByAddress(self, address, mode = 0):
        if mode == 0:
            address+=Memory.DataSegmentOffset
        elif mode == 1:
            address+=Memory.CodeSegmentOffset
        result = 0
        for i in range(Memory.words):
            result |= ((Memory.memory[address+i]&1)<<((Memory.words-1)-i))
        return result
    
    def __str__(self):
        result = ''
        hexadecimal = ['0', '1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        pointer = 0
        for i in range((Memory.space*Memory.words)//4):
            tmp = 0
            for j in range(4):
                tmp |= (Memory.memory[pointer]&1)<<(3-j)
                pointer+=1
            result+=hexadecimal[tmp]
            if pointer%128 == 0:
                result += "\n"
            elif pointer%64 == 0:
                result += "  |  "
            elif pointer%16 == 0:
                result += "  "
            elif pointer%8 == 0:
                result += " "
                
        return result

    def __repr__(self) -> str:
        return self.__str__()


# 테스트 코드
if __name__=="__main__":
    m = Memory()
    m.setWordByAddress(0, 0xF0FF)
    m.setWordByAddress(0x10, 0x110A) #최상위 두 워드에 61695(부호 적용시 -28978) 와 4362라는 두 값을 저장
    print(m)
    print(m.getWordByAddress(0x0))
    print(m.getWordByAddress(0x10))