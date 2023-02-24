#---------------------------------------------------------
# File--------GSTAL_Virtual_Machine.py
# Developer---B. Crawley & B. Cadena
# Course------Research Assistant
# Project-----Project #1
# Date--------October 19, 2018
#
# This program is a GSTAL Virtual Machine
# 
# Modified in Spring 2023 by B. Cottrell 
# To connect it to GSTAL Debugger
#-------------------------------------------------------------------
import sys
import argparse
import time
from gstalmem import DataCell
from uimanager import View

#--------------------------GSTALVM-----------------------------------------------    

class GSTALVM: 
    def __init__(self):            #set initial values
        self.init()
                                   #stack methods
    def isEmpty(self):
        return self._dataMem == []

    def push(self, x):
        self._tos += 1
        self._dataMem.append(x) 
        self.view.add_to_stack(x)

    def pop(self):                
        if(len(self._dataMem) < 1): #stackunderflow error            
            return self.runError()
        else:         
            self._tos -= 1
            self.view.remove_from_stack()
            return self._dataMem.pop() 

    def peek(self):
        if(len(self._dataMem) < 1): #stackunderflow error            
            return self.runError()
        else:         
            return self._dataMem[self._tos]

    def size(self):
        return self._tos+1
    
    def finished_execution(self):
        return self._pc >= self._inst_count or self._stopped

    def runError(self):    
        self.view.write_terminal("ERROR: GOOD LUCK IN THE COMPUTER APOCALYPSE") #eventually change this to an argument error (i.e. Error: Stack Underflow or Error: Divide by zero or Error: 
        parser = argparse.ArgumentParser() #read command line check for -d 
        parser.add_argument('-d', '--stackdump') #creates argument stackdump 
        stackdump=True
        if stackdump == True:  
            file= open("stackdump.txt","w+")
            x = len(self._dataMem)
            for i in range(0, x):
                file.write(str(self.pop()))
            file.close()
            self.stop()
        return sys.exit()                            

    def stack_reset(self): #stackDump 
        x = len(self._dataMem)
        for i in range (0, x):
            self.pop()
        self._pc = 0    
        self._stopped = False
        return    

    def stop(self):
        self._pc = -1
        self._stopped = True
        self.view.clear_highlight()
        return

    def full_reset(self): # resets code and data memory 
        self.stack_reset() 
        self.init()
        return

    def init(self): 
        self._tos = -1
        self._pc = 0
        self._act = 0
        self._inst_count = 0
        self._stopped = False
        self._dataMem = []
        self._codeMem = []

    def load(self, file):   #add flag, check operand is valid 
        self.full_reset()

        _dictionary = { "ADI":(1,None),  "SBI":(2,None),  "MLI":(3,None),
                        "DVI":(4,None),  "NGI":(5,None),
                        
                        "ADF":(6,None),  "SBF":(7,None),  "MLF":(8,None),
                        "DVF":(9,None), "NGF":(10,None),
                        
                       "EQI":(11,None), "NEI":(12,None), "LTI":(13,None),
                       "LEI":(14,None), "GTI":(15,None), "GEI":(16,None),
                        
                       "EQF":(17,None), "NEF":(18,None), "LTF":(19,None),
                       "LEF":(20,None), "GTF":(21,None), "GEF":(22,None),
                        
                       "FTI":(23,None), "ITF":(24,None),
                        
                       "PTI":(25,None), "PTF":(26,None), "PTC":(27,None),
                       "PTL":(28,None), "INI":(29,None), "INF":(30,None),
                        
                       "LLI":(31,"i"),  "LLF":(32,"f"),  "ISP":(33,"n"),
                       "DSP":(34,"n"),  "STO":(35,None), "STM":(36,None),
                       "LOD":(37,None),
                        
                       "LAA":(38,"n"),  "LRA":(39,"n"),  "JMP":(40,"n"),
                       "JPF":(41,"n"),  "PAR":(42,"n"),  "CAL":(43,"n"),
                       "RET":(44,None), "NOP":(45,None), "HLT":(46,None),
                       
                       "ADD":(47,None), "D":(48, None)}        
        allInstr = []
        allPiece = []
        flag = False
        f = file
        try:
            f = open(f)
        except Exception: 
            flag=True
            self.view.write_terminal("Error: File name not valid")
    
        for line in f:
            line=line.upper()
            pieces = line.split(";")[0]           
            instr = pieces.split()
            if(len(instr) <= 2):
                if(len(instr) < 2):
                    var = None  #add None to print instruction  
                    instr.append(var)
                allPiece.append(tuple(instr))
                allInstr.append(instr[0])
            else:
                self.view.write_terminal("error")
#check it
        i = 0
        while i < len(allInstr):
            opcode = str(allInstr[i])
            if(opcode in _dictionary):
                self._codeMem = allPiece
            else:
                flag = True
                self.view.write_terminal(f"This instruction is not in the GSTAL dictionary: {opcode}")
            i = i+1    
        self._inst_count = len(self._codeMem)
        return flag
            
            
    def execute(self):   
        if(self._pc < 0 or self._pc >= self._inst_count):
            return
            
        opcode = self._codeMem[self._pc][0]
        operand = self._codeMem[self._pc][1] 
        instr = "self."+opcode+"("
        if operand != None:
            instr = instr + str(operand)
        instr = instr + ")"
        exec(instr)  
        # update UI components. 
        self.view.update(self._dataMem, self._tos, self._act, self._pc)      
        return    

    # def run(self):
    #     while(self._pc >= 0 and self._pc < self._inst_count):
    #         self.execute()
    #     return  

    def run(self):
        self.execute()
        if not self.finished_execution():
            self.view.wait(self.run)
        else: 
            self.view.clear_highlight()

    def step_run(self):
        self.execute()
        return 
    
    def doit(self, opcode, operand=None):
        instr = "self."+opcode+"("
        if operand != None:
            instr = instr + str(operand)
        instr = instr + ")"
        exec(instr)
        return        
        
    def ADD(self): #only here for debug purposes 
        self.ADI()    
        
#INTEGER ARTHMETIC                                 
    def ADI(self):                 
        x = self.pop().int()
        y = self.pop().int()
        self.push(DataCell(x+y))
        self._pc = self._pc + 1
        return   
    
    def SBI(self):          
        x = self.pop().int()
        y = self.pop().int()
        self.push(DataCell(y-x))
        self._pc = self._pc + 1
        return   
    
    def MLI(self):          
        y = self.pop().int()
        x = self.pop().int()
        self.push(DataCell(x*y))
        self._pc = self._pc + 1
        return
    
    def DVI(self):                 
        y = self.pop().int()
        x = self.pop().int()
        if(x==0):
            self.runError()
        else:    
            self.push(DataCell(x // y))
            self._pc = self._pc + 1
        return  
    
    def NGI(self):   
        x = self.pop().int()
        self.push(DataCell(-x))
        self._pc = self._pc + 1
        return            
    
#FLOAT ARITHMETIC 
    def ADF(self):           
        x = self.pop().float()
        y = self.pop().float()
        self.push(DataCell(x+y))
        self._pc = self._pc + 1
        return
    
    def SBF(self):           
        y = self.pop().float()
        x = self.pop().float()
        self.push(DataCell(x-y))
        self._pc = self._pc + 1
        return
    
    def MLF(self):          
        y = self.pop().float()
        x = self.pop().float()
        self.push(DataCell(x*y))
        self._pc = self._pc + 1
        return
    
    def DVF(self):
        y = self.pop().float()
        x = self.pop().float()
        if(x==0):
            self.runError()
        else:    
            self.push(DataCell(x // y))
            self._pc = self._pc + 1    
        return
     
    
    def NGF(self):   
        x = self.pop().float()
        y = -x
        self.push(DataCell(y)) #error
        self._pc = self._pc + 1
        return  
        
#INTEGER RELATIONAL OPERATIONS
    def EQI(self):
        b = self.pop().int()
        a = self.pop().int()
        x = (a==b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return              

    def NEI(self):
        b = self.pop().int()
        a = self.pop().int()
        x = (a!=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def LTI(self):
        b = self.pop().int()
        a = self.pop().int()
        x = (a<b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def LEI(self):
        b = self.pop().int()
        a = self.pop().int()
        x = (a<=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def GTI(self):       
        b = self.pop().int()
        a = self.pop().int()
        x = (a>b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def GEI(self):
        b = self.pop().int()
        a = self.pop().int()
        x = (a>=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
#FLOAT RELATIONAL OPERATIONS                have them push a zero or one <-- apparently never fixed this
    def EQF(self):
        b = self.pop().float()
        a = self.pop().float()
        x = (a==b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return 
    
    def NEF(self):
        b = self.pop().float()
        a = self.pop().float()
        x = (a!=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def LTF(self):
        b = self.pop().float()
        a = self.pop().float()
        x = (a<b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def LEF(self):
        b = self.pop().float()
        a = self.pop().float()
        x = (a<=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def GTF(self):       
        b = self.pop().float()
        a = self.pop().float()
        x = (a>b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def GEF(self):
        b = self.pop().float()
        a = self.pop().float()
        x = (a>=b)
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
#DATA TYPE CONVERSION
    def FTI(self):
        x = self.pop().float()
        self.push(DataCell(int(x)))
        self._pc = self._pc + 1
        return
    
    def ITF(self):                                              
        x = self.pop().int()
        self.push(DataCell(float(x)))
        self._pc = self._pc + 1
        return
    
#STACK MANIPULATION    
    def LLI(self, x):            #cant handle 0 in front of ints   
        try:
            x = int(x)
            self.push(DataCell(x))     
            self._pc = self._pc + 1            
        except Exception:
            self.view.write_terminal("Oops! This is not an int. Please try again.")
        return
    
    def LLF(self, x):                                                      
        self.push(DataCell(x)) 
        self._pc = self._pc + 1
        return    
    
    def ISP(self, x):         
        self._pc = self._pc + 1
        for y in range(0, x): 
            self.push(DataCell(0))
        return
    
    def DSP(self, x):         
        if(len(self._dataMem) < x):
            self._pc = self._pc + 1
            for y in range(x):
                self.pop()
        return    
    
    def STO(self):
        self._pc = self._pc + 1
        b = self.pop()
        a = self.pop()
        if(len(self._dataMem) > a.int()):
            self._dataMem[a.int()] = b
        else: 
            self.runError()
        return

#Input Output    
    def PTI(self):
        a = self.pop()
        self.view.write_terminal(a.int())
        self._pc += 1
        return
    
    def PTF(self):
        a = self.pop()
        self.view.write_terminal(a.float()) #scientific notation??
        self._pc += 1
        return    
    
    def PTC(self):
        a = self.pop()
        self.view.write_terminal("%c"%a.int())
        self._pc += 1
        return
    
    def PTL(self):
        self.view.new_line_terminal()
        self._pc += 1
        return
    
    def INI(self):
        a  = int(self.view.get_terminal())
        self.push(DataCell(a))
        self._pc += 1
        return       
    
    def INF(self):
        a = float(self.view.get_terminal())
        self.push(DataCell(a))
        self._pc += 1
        return    
    
#Flow Control    
    def LAA(self, x):
        self._pc = self._pc + 1
        self.push(DataCell(x))
        return
    
    def LRA(self, x):
        self._pc = self._pc + 1
        y = x + self._act
        self.push(DataCell(y))
        return

    def LOD(self):
        a = self.pop()
        address = a.int()
        value = self._dataMem[address]
        self.push(value)
        self._pc += 1
        return
    
    def JMP(self, x):
        if(x >=self._inst_count):
            self.runError()
        else: 
            self._pc = x
        return
    
    def JPF(self, x):   
        if(x >=self._inst_count):
            self.runError()
        else:         
            a = self.pop()
            if(a.int()==0):
                self._pc = x
            else:
                self._pc += 1
        return    
    
    def PAR(self, x):
        self._pc = self._pc + 1
        self.push(DataCell(self._act - x))
        return
    
    def CAL(self, x): #check line jmp too again and if not exist RUNTIME ERROR WOOOOOOOOOOOOOOOT
        if(len(self._dataMem) >= x):
            self.runError()
        else:         
            self.push(DataCell(self._act))
            self._act = self._tos
            self.push(DataCell(self._pc))
            self._pc = x
        return
    
    def RET(self): 
        if(self._dataMem[self._act + 1].int() + 1 >= self._inst_count):
            self.runError()
        else:    
            pop_this_many = self._tos - (self._act - 1)   
            if(pop_this_many >= len(self._dataMem)):               
                self.runError()
            else: 
                self._pc = self._dataMem[self._act + 1].int() + 1     
                self._act = self._dataMem[self._act].int()
                for i in range(pop_this_many):
                    self.pop()
       
    def NOP(self): 
        self._pc = self._pc + 1
        return
    
    def HLT(self):
        self.stop()
        return  