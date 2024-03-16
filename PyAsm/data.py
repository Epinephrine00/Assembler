# 사실 List 자료형에서 Stack과 Queue를 일부 지원하긴 합니다만....
# 타입을 명확하게 해서 가독성을 높이려는 목적으로 사용합니다. 

class Queue:
    def __init__(self, *args):
        self.queue = args if len(args)>0 else []
    
    def pop(self):
        r = self.queue[0]
        if len(self.queue)>1:
            self.queue = self.queue[1:]
        else:
            self.queue = []
        return r
    
    def append(self, value):
        self.queue.append(value)

    def __len__(self):
        return len(self.queue)
    

class Stack:
    def __init__(self, *args):
        self.stack = args if len(args)>0 else []

    def pop(self):
        r = self.stack[-1]
        self.stack = self.stack[:-1]
        return r

    def push(self, value):
        self.stack.append(value)

    def top(self):
        return self.stack[-1]
    
    def __len__(self):
        return len(self.stack)
