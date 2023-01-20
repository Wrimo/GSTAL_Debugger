#---------------------------------------------------------
# File--------sandbox-numblines.py
# Developer---B. Crawley & B. Cadena
# Course------Research Assistant
# Project-----Project #2
# Date--------February 8th, 2019
#
# This program is a GSTAL Virtual Machine
#-------------------------------------------------------------------
import sys
import argparse
from gstalmem import DataCell
# print("This program is a GSTAL Virtual Machine")

#--------------------------GSTALVM-----------------------------------------------    

class GSTALVM: 
    def __init__(self):            #set initial values
        self._tos = -1
        self._pc = 0
        self._act = 0
        self._dataMem = []
        self._codeMem = []
                                   #stack methods
    def isEmpty(self):
        return self._dataMem == []

    def push(self, x):
        self._tos += 1
        self._dataMem.append(x) 

    def pop(self):                 
        if(len(self._dataMem) < 1): #stackunderflow error            
            return self.runError()
        else:         
            self._tos -= 1
            return self._dataMem.pop() 

    def peek(self):
        if(len(self._dataMem) < 1): #stackunderflow error            
            return self.runError()
        else:         
            return self._dataMem[self._tos]

    def size(self):
        return self._tos+1
    
    def runError(self):    
        print("ERROR: GOOD LUCK IN THE COMPUTER APOCALYPSE") #eventually change this to an argument error (i.e. Error: Stack Underflow or Error: Divide by zero or Error: 
        parser = argparse.ArgumentParser() #read command line check for -d 
        parser.add_argument('-d', '--stackdump') #creates argument stackdump 
        stackdump=True
        if stackdump == True:  
            file= open("stackdump.txt","w+")
            x = len(self._dataMem)
            for i in range(0, x):
                file.write(str(self.pop()))
            file.close()
            self._pc = -1 
        return sys.exit()                            

    def reset(self): #stackDump 
        x = len(self._dataMem)
        for i in range (0, x):
            self.pop()
        self._pc = 0    
        return    

    def load(self, file):   #add flag, check operand is valid 
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
        
        ef = file
        try:
            f=open(ef)
        except Exception: 
            flag=True
            print("Error: File name not valid")
        f.seek(0)
        #lines = f.readlines()
        #print(lines)
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
                print("error")
#check it
        i = 0
        while i < len(allInstr):
            opcode = str(allInstr[i])
            if(opcode in _dictionary):
                self._codeMem = allPiece
            else:
                flag = True
                print("This instruction is not in the GSTAL dictionary:", opcode)
            i = i+1    
        return flag
            
            
    def execute(self):       
        if(self._pc < 0):
            return
        opcode = self._codeMem[self._pc][0]
        operand = self._codeMem[self._pc][1] 
        instr = "self."+opcode+"("
        if operand != None:
            instr = instr + str(operand)
        instr = instr + ")"
        exec(instr)
        return    

    def run(self):
        while(self._pc >= 0 and self._pc < len(self._codeMem)):
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
        
#command line instructions LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL

    def L(self):
        parser = argparse.ArgumentParser() #read command line check for -d 
        parser.add_argument('-l', '--listing') #creates argument stackdump         
        with open('testing.txt', 'r') as f:  
            for index, line in enumerate(f):
                code = line.strip()
                print(index, code)
                #python version of distinct??? 
        return       
    
    #command line instructions LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
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
        self.push(DataCell(x-y))
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
            print("Oops! This is not an int. Please try again.")
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
        if(len(self._dataMem < a)):
            self._dataMem[a.int()] = b
        else: 
            self.runError()
        return

#Input Output    
    def PTI(self):
        a = self.pop()
        #print("%d" % a.int(), end="")
        TL.insert(END, a.int())
        self._pc += 1
        return
    
    def PTF(self):
        a = self.pop()
        #print("%e" % a.float(), end="") #scientific notation??
        TL.insert(END, a.float())
        self._pc += 1
        return    
    
    def PTC(self):
        a = self.pop()
         #print("%c"%a.int(), end="")
        a = a.int()
        TL.insert(END, chr(a))
        #TL.insert(END, a.ascii())
        self._pc += 1
        return
    
    def PTL(self):
        #print("")
        TL.insert(END, "argh")
        TL.delete(END)
        self._pc += 1
        return
    
    def INI(self): #use get() 
        a  = int(input(""))
        self.push(DataCell(a))
        self._pc += 1
        return       
    
    def INF(self):
        #x = float(input(""))
        x = enter.get()
        x = float(x.strip())
        self.push(DataCell(x))
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
        if(x >=len(self._codeMem)):
            self.runError()
        else: 
            self._pc = x
        return
    
    def JPF(self, x):   
        if(x >=len(self._codeMem)):
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
        if(self._dataMem[self._act + 1].int() + 1 >= len(self._codeMem)):
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
        self._pc = -1
        return

#------------------set up GSTAL VM-----------------
vm = GSTALVM()

#--------------------------tkinter-----------------------------------------------
import tkinter as tk
from tkinter import filedialog

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[0]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)
            #--------CheckBoxes----------
            self.var = tk.BooleanVar()
            self.brpt = tk.Checkbutton(root,variable=self.var)
            self.brpt.pack(side="left")
            self.pr = tk.Button(root, text="Print", command=self.testing)
            self.pr.pack(side="bottom")
            #create list of var (.append)  (list is started at 0, line 0 in code
            
    def testing(self):
        print("Checked Boxes: \n    %d" % self.var.get())

            #--------CheckBoxes----------

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        # self.linenumbers = TextLineNumbers(self, width=30)
        # self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        # self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        #--------if there are any errors its because of here--------

        self.op = tk.Button(root, text="Open", command=self._open_file)
        self.op.pack(side="bottom")
        #self.ss = tk.Button(root, text="Single-Step", command=vm.execute)
        #self.ss.pack(side="bottom")

        
        
        
    def _on_change(self, event):
        pass
        # self.linenumbers.redraw()

    def _open_file(self):
        vm.reset()
        self.text.delete("1.0", "end")
        root.filename = filedialog.askopenfilename(initialdir = "/",
            title="Select file", filetypes=(("GSTAL Files","*.gstal"),
            ("Text Files", "*.txt"), ("All Files", "*.*")))
        with open(root.filename, "r") as f:
            text = f.read()
            self.text.insert("end", text)

    #--------end mistakes--------

#new code
class Reggie(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        tosLbl = tk.Label(self, text = '_tos ')
        tosEnt = tk.Entry(self)
        tosEnt.insert(0, vm._tos)

        pcLbl = tk.Label(self, text = '_pc')
        pcEnt = tk.Entry(self)
        pcEnt.insert(0, vm._pc)

        actLbl = tk.Label(self, text = '_act')
        actEnt = tk.Entry(self)
        actEnt.insert(0, vm._act)

        #packs
        tosLbl.pack()
        tosEnt.pack()
        pcLbl.pack()
        pcEnt.pack()
        actLbl.pack()
        actEnt.pack()

    def _on_change(self, event="<ButtonRelease-1>"):
        tosEnt.insert(0, vm._tos)
        pcEnt.insert(0, vm._pc)
        actEnt.insert(0, vm._act)

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    # Reggie(root).pack(side="left", fill="y", expand=True)
    root.mainloop()


