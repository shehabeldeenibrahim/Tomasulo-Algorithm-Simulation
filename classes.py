class Instruction():
    def __init__(self,operation,rd,rs1,rs2,pc):
        self.operation = operation
        self.rd = (rd)
        self.rs1= (rs1)
        self.rs2= (rs2)
        self.PC = pc
        self.fetch = None

    
class Data():
    def __init__(self,label,size,data):
        self.label = label
        self.size = size
        self.data=data

class Label():
    def __init__(self,name,position):
        self.name = name
        self.position = position

class ROB():
    def __init__(self):
        self.num = None
        self.instruction = None
        self.dest = None
        self.value = None
        self.ready = False
        self.busy = False
        self.fetch = None

class ReservationStation():
    def __init__(self):
        self.out = -1
        self.busy = False
        self.name = None
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = 0
        self.qk = 0
        self.dest = None
        self.a = None
        self.ready=False
        self.PC=None
        self.fetch = None
        self.cycles = 1

