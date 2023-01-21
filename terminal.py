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


class Terminal: 
    def __init__(self, tk_object):
        self.object = tk_object
        self.entered = IntVar()  # used by the debugger to signal when the user has finished entering input 
    
    def write(self, val):
        self.object.configure(state="normal")
        self.object.insert(END, (f"{val}"))
        self.object.configure(state="disabled")

    def get(self): 
        self.object.configure(state="normal")
        start = self.get_size()
        val = self.object.get(float(start), END)
        self.object.wait_variable(self.entered)
        self.object.configure(state="disabled")
        return val

    def get_size(self):
        return len(self.object.get("1.0", 'end-1c'))