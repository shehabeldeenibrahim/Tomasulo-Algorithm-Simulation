from functions import *
from classes import *
import numpy as np
def main_fun(starting_point):
    StartingPointInstMem = int(starting_point)
    data_memory,labels_array,instructions_memory= parser(StartingPointInstMem) 
    EndingPointInstMem  = findLastInstIndex(instructions_memory)
    PC=int(StartingPointInstMem)
    n_instructions = EndingPointInstMem-int(StartingPointInstMem)
    commited = 0
    data_memory[300], data_memory[301], data_memory[302], data_memory[303] = 19,2,25,208
    cycles=1
    rf = [None]*(8)
    for i in range(0,8):
        rf[i] = i*2

    rob = []
    reservation_s = []
    instruction_buffer = []

    for b in range (0,15):
        reservation_s.append(ReservationStation())

    for c in range (0,7):
        rob.append(ROB())

    rat_inst = {
        "Register" :  0 ,
        "ROB #" : 0 
    }
    reg_stat = [0]*(8)

    mapping = {"Load1":0
    ,"Load2":1
    ,"Store1":2
    ,"Store2":3
    ,"Jump1":4
    ,"Jump2":5
    ,"Jump3":6
    ,"Branch1":7
    ,"Branch2":8
    ,"ALU1":9
    , "ALU2":10
    , "ALU3":11
    , "NAND":12
    , "MULT1":13
    , "MULT2":14
    }

    reservation_s[0].name = "Load1"
    reservation_s[1].name = "Load2"
    reservation_s[2].name = "Store1"
    reservation_s[3].name = "Store2"
    reservation_s[4].name = "Jump1"
    reservation_s[5].name = "Jump2"
    reservation_s[6].name = "Jump3"
    reservation_s[7].name = "Branch1"
    reservation_s[8].name = "Branch2"
    reservation_s[9].name = "ALU1"
    reservation_s[10].name = "ALU2"
    reservation_s[11].name = "ALU3"
    reservation_s[12].name = "NAND"
    reservation_s[13].name = "MULT1"
    reservation_s[14].name = "MULT2"
    head=1
    tail=1

    while commited<n_instructions:
        
        if(head == 7):
            head = 1    
        if(rob[head].ready):
            commit(rob,head,data_memory,rf,reg_stat,head)
            commited+=1
            head +=1
            if(head == 7):
                head = 1
                previous_head = 6
            else:
                previous_head = head-1
            if(rob[head].ready):
                commit(rob,head,data_memory,rf,reg_stat,head)
                commited+=1
                head +=1

        write(reservation_s,mapping,rob,tail)

        execute(reservation_s,data_memory,PC,rob,reg_stat,instruction_buffer)

        if(len(instruction_buffer)!=0):   
            if((head != tail or cycles ==2) and OpStrToNum(instruction_buffer[0].operation,reservation_s) != -1 ): 
                issue(instruction_buffer[0],reg_stat,rob,reservation_s,tail,rf,PC,cycles)
                instruction_buffer = instruction_buffer[1:]
                if(tail == 6):
                    tail = 1
                else:
                    tail += 1
            if(len(instruction_buffer) > 0):

                if((head != tail or cycles ==2) and OpStrToNum(instruction_buffer[0].operation,reservation_s) != -1 ): 
                    issue(instruction_buffer[0],reg_stat,rob,reservation_s,tail,rf,PC,cycles)
                    instruction_buffer = instruction_buffer[1:]
                    if(tail == 6):
                        tail = 1
                    else:
                        tail += 1

        if(len(instruction_buffer)<4):
            if(PC < EndingPointInstMem and instructions_memory[PC]!=None):
                fetch(instruction_buffer,instructions_memory[PC],cycles)
                PC+=1
                if(PC < EndingPointInstMem and len(instruction_buffer)<4):
                    fetch(instruction_buffer,instructions_memory[PC],cycles)
                    PC+=1



    
        cycles+=1
    return "Number of cycles: " + str(cycles) + "\n" + "IPC:" + str(n_instructions/cycles) 

    
