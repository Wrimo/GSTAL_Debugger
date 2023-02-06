# ---------------------------------------------------------
# File--------uimaanager.py
# Developer---B. Cottrell
# Date--------January, 20 2023
#
# Definition of classes to handle writing to and getting
# tkinter objects. Allows for one set of methods for both
# debugger.py and GSTAL_Virtual_Machine.py
# -------------------------------------------------------------------


from tkinter import *
from tkinter import ttk
from ui_object import *


class View: 
    def update(self, stack, tos, act, pc): 
        self.stack.update_stack(stack, act)
        self.regs.write(tos, act, pc)
        self.editor.highlight_line(pc + 1)
        self.editor.object.see(float(pc + 15))
    
    def wait(self, call_back): 
          self.root.after(int(self.delay.get()), call_back)

    def write_terminal(self, val):
        self.terminal.write(val)

    def get_terminal(self):
        self.terminal.write("\n")
        val = self.terminal.get()
        return val
    
    def clear_highlight(self):
        self.editor.clear_highlight()

class UIObject:
    def __init__(self, tk_object):
        self.object = tk_object
    
    def write(self, val):
        self.object.insert(END, (f"{val}"))

    def write_top(self, val):
        self.object.insert(INSERT, (f"{val}"))

    def get(self, _start = 0, _end = END): 
         return self.object.get(float(_start), _end)

    def clear(self):
        self.object.delete(1.0, END)


class RegisterValue(UIObject):
    def __init__(self, tk_object):
        self.object = tk_object
    def write(self, tos, act, pc):
        self.object.configure(text=f"tos: {tos} act: {act} pc: {pc}")

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
        super().write(val)
        self.object.configure(state="disabled")

    def write_top(self, val):
        self.object.configure(state="normal")
        super().write_top(val)
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
        super().clear()
        self.object.configure(state="disabled")
 
class Stack(UIObject):
    def update_stack(self, stack, act):
        self.object.reset()
        for i in range(0, len(stack)):
            if i == act: 
                self.object.add_text(f"{i}: {stack[i].int()}", True)                
            else:
                self.object.add_text(f"{i}: {stack[i].int()}", False)
