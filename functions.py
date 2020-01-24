import re
from classes import *

def isRobEmpty(rob):
    for r in rob:
        if(r.busy):
            return False
    return True
def findLastInstIndex(instructions_memory,start):
    i = 0
    for x in range (start,len(instructions_memory)):
        if(instructions_memory[x] == None):
            break
        i+=1
    return i+start

def parser(StartingPosInstMem,branch):
    #returns data memory,labels array, instruction_memory
    #Imports
    test_path = "test.txt"

    #reading from file
    file = open(test_path, 'r')
    instructions_string_Array = file.readlines()

    seperated_instruction_array = [None]*(64*1024) #assuming 8KB Instruction Memory

    label_array = []


    #StartingPosInstMem = input('Please enter startng point of instructions in Inst Mem: ')
    i=int(StartingPosInstMem)
    j=0
    for instruction_string in instructions_string_Array:
        if(instruction_string=='.data\n'):
            break
        inst_string_length =len(instruction_string)

        if(instruction_string[inst_string_length-2]==':'):
            label = Label(instruction_string[0:inst_string_length-2],i)
            label_array.append(label)
            i+=1
            continue

        seperated_instruction = re.findall(r"[\w']+", instruction_string)

        if(seperated_instruction[0]=="JMP" or seperated_instruction[0]=="RET"):
            instruction = Instruction(seperated_instruction[0],seperated_instruction[1],0,0,i)
        else:
            if(seperated_instruction[0]=="JALR"):
                instruction = Instruction(seperated_instruction[0],seperated_instruction[1],seperated_instruction[2],0,i)
 
            else:
                if(seperated_instruction[0]=="SW" or seperated_instruction[0]=="BEQ"):
                    instruction = Instruction(seperated_instruction[0],seperated_instruction[3],seperated_instruction[1],seperated_instruction[2],i)
                else:
                    instruction = Instruction(seperated_instruction[0],seperated_instruction[1],seperated_instruction[2],seperated_instruction[3],i)
        #seperated_instruction_array.append(instruction)
        seperated_instruction_array[i] = instruction
        i+=1
        j+=1
        if(seperated_instruction[0]=="BEQ"):
            branch+=1

    data_memory_temp=[]
    for k in range(i+1,len(instructions_string_Array)):
        seperated_data = re.findall(r"[\w']+", instructions_string_Array[k])
        data_array=[]
        for j in range(2,len(seperated_data)):
            data_array.append(seperated_data[j])
            data = Data(seperated_data[0],seperated_data[1],data_array)
        data_memory_temp.append(data)



    #initialize data memory
    data_memory = [0]*(4*1024) #4KB data memory
    index=0
    for data in data_memory_temp:
        for single_data in data.data:   
            data_memory[index] = int(single_data)
            index+=1
    
    print("debug")
    return data_memory,label_array,seperated_instruction_array,branch

def num(stri):
    if(type(stri) == str and not stri.isdigit() ):
        return int(stri[1])
    else:
        if(stri == None):
            return 0
        return int(stri)

def fetch(instruction_buffer,instruct,cycles):
    instruct.fetch = cycles
    instruction_buffer.append(instruct)

def execute(res_s,data_mem,PC,rob,reg_stat,instruction_buffer,tail,miss):
    branched = False
    for b in range(0,15):
        Out = -1
        if(res_s[b].qj == 0 and res_s[b].qk == 0):
            instr_op = res_s[b].op

            if(instr_op=="LW"):
                if(res_s[b].cycles >= 2):
                    res_s[b].out=data_mem[res_s[b].a]
                    res_s[b].cycles=0
                    res_s[b].ready = True
                else:
                    if(res_s[b].cycles ==1):
                        res_s[b].a = res_s[b].vj +res_s[b].a
                        res_s[b].vj=0
                    res_s[b].cycles=res_s[b].cycles+1 

            else: 
                if(instr_op=="SW"):
                    if(res_s[b].cycles>=2):
                        res_s[b].out=res_s[b].vj
                        res_s[b].cycles=0
                        res_s[b].ready = True
                    else:
                        if(res_s[b].cycles ==1):
                            res_s[b].a = res_s[b].vk +res_s[b].a
                            res_s[b].vk=0
                        res_s[b].cycles=res_s[b].cycles+1

                else:
                    if(instr_op=="JMP"):
                        if(res_s[b].cycles>=1):
                            PC=res_s[b].a + res_s[b].PC +1
                            branched = True 
                            res_s[b].cycles=0
                            res_s[b].ready = True
                            tail = needToFlush(rob,res_s,res_s[b].PC,reg_stat,instruction_buffer,tail)
                        else:
                            res_s[b].cycles = res_s[b].cycles+1
                    else:
                        if(instr_op=="BEQ"):
                            if(res_s[b].cycles>=1):
                                if(res_s[b].vj==res_s[b].vk):
                                    miss+=1
                                    PC=res_s[b].a + res_s[b].PC +1
                                    branched = True
                                    tail = needToFlush(rob,res_s,res_s[b].PC,reg_stat,instruction_buffer,tail)  
                                else:
                                    Out=-1
                                res_s[b].cycles=0
                                res_s[b].ready = True
                            else:
                                res_s[b].cycles=res_s[b].cycles+1

                        else:
                            if(instr_op=="JALR"):
                                if(res_s[b].cycles>=1):
                                    PC=res_s[b].vj
                                    branched = True
                                    res_s[b].out=res_s[b].PC
                                    res_s[b].cycles=0
                                    res_s[b].ready = True
                                    tail = needToFlush(rob,res_s,res_s[b].PC,reg_stat,instruction_buffer,tail)
                                else:
                                    res_s[b].cycles=res_s[b].cycles+1

            
                            else:
                                if(instr_op=="RET"):
                                    if(res_s[b].cycles >= 1):
                                        branched = True
                                        PC=res_s[b].vj
                                        res_s[b].cycles=0
                                        res_s[b].ready = True
                                        tail = needToFlush(rob,res_s,res_s[b].PC,reg_stat,instruction_buffer,tail)
                                    else:
                                        res_s[b].cycles=res_s[b].cycles+1

                                    

            
                                else:
                                    if(instr_op=="ADD"):
                                        if(res_s[b].cycles>=2):
                                            res_s[b].out=res_s[b].vj+res_s[b].vk
                                            res_s[b].cycles=0
                                            res_s[b].ready = True

                                        else:
                                            res_s[b].cycles=res_s[b].cycles+1


                                    else:
                                        if(instr_op=="SUB"):
                                            if(res_s[b].cycles>=2):
                                                res_s[b].out=res_s[b].vj-res_s[b].vk
                                                res_s[b].cycles=0
                                                res_s[b].ready = True
                                            else:
                                                res_s[b].cycles=res_s[b].cycles+1

                                        else:
                                            if(instr_op=="ADDI"):
                                                if(res_s[b].cycles>=2):
                                                    res_s[b].out=res_s[b].vj+int(res_s[b].vk)
                                                    res_s[b].cycles=0
                                                    res_s[b].ready = True
                                                else:
                                                    res_s[b].cycles=res_s[b].cycles+1

            
                                            else:
                                                if(instr_op=="NAND"):
                                                    if(res_s[b].cycles>=1):
                                                        res_s[b].out=~(res_s[b].vj & res_s[b].vk)
                                                        res_s[b].cycles=0
                                                        res_s[b].ready = True
                                                    else:
                                                        res_s[b].cycles=res_s[b].cycles+1

            
                                                else:
                                                    if(instr_op=="MUL"):
                                                        if(res_s[b].cycles>=8):
                                                            res_s[b].out=res_s[b].vj*res_s[b].vk
                                                            res_s[b].cycles=0
                                                            res_s[b].ready = True
                                                        else:
                                                            res_s[b].cycles=res_s[b].cycles+1
        if(not res_s[b].ready):
            res_s[b].out = Out
    return branched,PC,tail,miss
    
 
def OpStrToNum (oper,ResStat):
    op = -1
    if(oper == "LW"):
        if(ResStat[0].busy != True):
            op = 0
        else:
            if(ResStat[1].busy != True):
                op = 1


    else:
        if(oper == "SW"):
            if(ResStat[2].busy != True):
                op = 2
            else:
                if(ResStat[3].busy != True):
                    op = 3

        else:
            if(oper == "JMP" or oper == "JALR" or oper =="RET"):
                if(ResStat[4].busy != True):
                    op = 4
                else:
                    if(ResStat[5].busy != True):
                        op = 5
                    else:
                        if(ResStat[6].busy != True):
                            op = 6

            else:
                if(oper == "BEQ"):
                    if(ResStat[7].busy != True):
                        op = 7
                    else:
                        if(ResStat[8].busy != True):
                            op = 8
                
                else:
                    if(oper == "ADD" or oper == "ADDI" or oper == "SUB"):
                        if(ResStat[9].busy != True):
                            op = 9
                        else:
                            if(ResStat[10].busy != True):
                                op = 10
                            else:
                                if(ResStat[11].busy != True):
                                    op = 11
                    else:
                        if(oper == "NAND"):
                            if(ResStat[12].busy != True):
                                op = 12
                        
                        else:
                            if(oper == "MUL"):
                                if(ResStat[13].busy != True):
                                    op = 13
                                else:
                                    if(ResStat[14].busy != True):
                                        op = 14
    return op

def issue(instruction,reg_stat, rob, reservation_s,rob_num,regs,PC,fetch):

    op = OpStrToNum(instruction.operation,reservation_s)
    instruction_op = instruction.operation
    reservation_s[op].op = instruction_op
    rs = instruction.rs1
    rt = instruction.rs2
    rd = instruction.rd
    rob[rob_num].busy = True
    
    if instruction_op != "JMP":
        if reg_stat[num(rs)] != 0: #if reg stat is busy
            h = reg_stat[num(rs)]  
            if rob[h].ready:
                reservation_s[op].vj = rob[h].value
                reservation_s[op].qj = 0
            else:
                reservation_s[op].qj = h
        else:
            reservation_s[op].vj = regs[num(rs)]#"regs["+rs+"]"
            reservation_s[op].qj = 0

        reservation_s[op].busy = True
        reservation_s[op].dest = rob_num
        rob[rob_num].instruction = instruction_op
        rob[rob_num].dest = rd
        rob[rob_num].ready = False
        if instruction_op != "LW" and instruction_op != "ADDI" and instruction_op != "JALR" and instruction_op != "RET":
            if reg_stat[num(rt)] != 0: #if reg stat is busy
                h = reg_stat[num(rt)]  
                if rob[h].ready:
                    reservation_s[op].vk = rob[h].value
                    reservation_s[op].qk = 0
                else:
                    reservation_s[op].qk = h
            else:
                reservation_s[op].vk = regs[num(rt)]#"regs["+rt+"]"
                reservation_s[op].qk = 0

        if instruction_op != "LW" and instruction_op != "ADDI" and instruction_op != "SW" and instruction_op != "BEQ" and instruction_op != "RET":
            reg_stat[num(rd)] = rob_num
            rob[rob_num].dest = rd

        if instruction_op == "LW":
            reservation_s[op].a = int(rt)
            reg_stat[num(rd)] = rob_num
            rob[rob_num].dest = rd

        if  instruction_op == "ADDI":
            reg_stat[num(rd)] = rob_num
            rob[rob_num].dest = rd
            reservation_s[op].vk = rt
            reservation_s[op].qk = 0

        if instruction_op == "SW" or instruction_op == "BEQ":
            reservation_s[op].a = int(rd)
    else:
        reservation_s[op].a = int(rd)
        reservation_s[op].busy = False
        reservation_s[op].dest = 0
        rob[rob_num].dest = rd
    reservation_s[op].PC=instruction.PC
    reservation_s[op].fetch = instruction.fetch
    rob[rob_num].fetch = instruction.fetch

def write(reservation_s, mapping,rob,rob_num):
    def KeyFunction(reser):
        return reser.PC
    ready_rs = []
    
    for rs in reservation_s:
        if(rs.ready):
            ready_rs.append(rs)
    ready_rs.sort(key = KeyFunction)
    for c in range (0,2):
        if(len(ready_rs)>0):
            r = mapping[ready_rs[c].name]
            reservation_s[r].busy = False
            if(ready_rs[0].name != "Store1" and ready_rs[0].name != "Store2"):
                b = reservation_s[r].dest
                if(b==None):
                    print("debug")
                for x in reservation_s:
                    if(x.qj == b):
                        x.vj = reservation_s[r].out
                        x.qj = 0

                for x in reservation_s:
                    if(x.qk == b):
                        x.vk = reservation_s[r].out
                        x.qk = 0

                rob[b].value = reservation_s[r].out # Need to check this
                rob[b].ready = True


            else:
                if(reservation_s[r]):
                    b = reservation_s[r].dest
                    if(b==None):
                        print("debug")
                    rob[b].value = reservation_s[r].vj
                    rob[b].ready = True
                    rob[b].dest = reservation_s[r].a
            
            reservation_s[r].busy = False
            reservation_s[r].op = None
            reservation_s[r].vj = None
            reservation_s[r].vk = None
            reservation_s[r].qj = 0
            reservation_s[r].qk = 0
            reservation_s[r].dest = None
            reservation_s[r].a  =  None
            reservation_s[r].ready = False
            reservation_s[r].PC = None
            reservation_s[r].cycles = 1
            if(len(ready_rs)>=2):
                if(ready_rs[0].fetch != ready_rs[1].fetch):
                    break
            else:
                break
        

def needToFlush(rob,reservation_s,beq_pc,reg_stat,instruction_buffer,tail):
    i=0
    index=[]
    for r in reservation_s:
        if(r.PC != None):
            if(r.PC > beq_pc):
                index.append(i)
        i+=1
    f = len(instruction_buffer)
    k=0
    for a in range(0,f):
        if(instruction_buffer[k].PC > beq_pc):
            instruction_buffer.remove(instruction_buffer[k])
            k-=1
        k+=1
        
    for b in index:
        #clear rob
        rob_num = reservation_s[b].dest
        dest_reg = rob[num(rob_num)].dest
        rob_new = ROB()
        rob.remove(rob[rob_num])
        rob.append(rob_new)
        tail = tail -1
        #clear rs
        reservation_s[b].out = -1
        reservation_s[b].busy = False
        reservation_s[b].op = None
        reservation_s[b].vj = None
        reservation_s[b].vk = None
        reservation_s[b].qj = None
        reservation_s[b].qk = None
        reservation_s[b].dest = None
        reservation_s[b].a  =  None
        reservation_s[b].ready = False
        reservation_s[b].PC = None
        reservation_s[b].cycles = -1

        #clear regstat
        reg_stat[num(dest_reg)] = 0
    return tail


def commit(rob, h, mem,rf,reg_stat,rob_num):

    if(type(rob[h].dest) is str):
        d = num(rob[h].dest)
    else:
        d = rob[h].dest
    rob[h].busy = False
    if(rob[h].instruction=="BEQ"):
        if(rob[h].value == -1):

            cleared_rob = ROB()
            rob[h] = cleared_rob
            #flush()
    else:
        if(rob[h].instruction=="SW"):
            mem[rob[h].dest] = rob[h].value
        else:
            rf[d] = rob[h].value
    rob[h].ready = False

    for i in range(0,len(reg_stat)):
        if(reg_stat[i] == rob_num):
            reg_stat[i] = 0
    


def checkDepend(inst1, inst2):
    rd1, rs1, rt1 = inst1.rd, inst1.rs1, inst1.rs2
    rd2, rs2, rt2 = inst2.rd, inst2.rs1, inst2.rs2

    if(rd1 == rs2 or rd1 == rt2 or rd2 == rs1 or rd2 == rt1 or rd1 == rd2):
        return False
    else:
        return True

