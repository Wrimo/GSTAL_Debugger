# ---------------------------------------------------------
# File--------terminal.py
# Developer---Brennan Cottrell
# Date--------January, 20 2023
#
# Definition of a class to handle writing to and getting from
# the debugger's terminal. Allows for one set of methods for both
# debugger.py and GSTAL_Virtual_Machine.py
# -------------------------------------------------------------------


from tkinter import *
from tkinter import ttk


class UIObject:
    def __init__(self, tk_object):
        self.object = tk_object
    
    def write(self, val):
        self.object.insert(END, (f"{val}"))

    def get(self, _start = 0, _end = END): 
         return self.object.get(float(_start), _end)


class Editor(UIObject): 
    def __init__(self, tk_object):
        super().__init__(tk_object)
        self.line = 1

    def highlight_line(self, line): 
        self.remove_highlight(self.line) 
        self.object.tag_add("step", float(line), f"{float(line)} lineend")
        self.line = line

    def clear_highlight(self):
        self.remove_highlight(self.line)
    
    def remove_highlight(self, line): 
        self.object.tag_remove("step", float(line), f"{float(line)} lineend")
    

class Terminal(UIObject): 
    def __init__(self, tk_object):
        self.object = tk_object
        self.entered = IntVar()  # used by the debugger to signal when the user has finished entering input 
    
    def write(self, val):
        self.object.configure(state="normal")
        self.object.insert(END, (f"{val}"))
        self.object.configure(state="disabled")

    def get(self): 
        self.object.configure(state="normal")
        start = self.get_line_count()
        self.object.wait_variable(self.entered)
        val = self.object.get(float(start), END)
        self.object.configure(state="disabled")
        return val

    def get_size(self):
        return len(self.object.get("1.0", "end-1c"))

    def get_line_count(self): # https://stackoverflow.com/questions/4609382/getting-the-total-number-of-lines-in-a-tkinter-text-widget
        return int(self.object.index('end-1c').split('.')[0])

    def clear(self):
        self.object.configure(state="normal")
        self.object.delete(1.0, END)
        self.object.configure(state="disabled")