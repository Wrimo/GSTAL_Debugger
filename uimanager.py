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
        if self.delay == 0:
            return
        self.tos_label.write(tos)
        self.act_label.write(act)
        self.pc_label.write(pc)
        self.editor.highlight_line(pc + 1)
        self.editor.text.see(float(pc + 15))
        self.stack.update_stack(stack, act)

    def add_to_stack(self, item):
        self.stack.push_item(item)

    def remove_from_stack(self):
        self.stack.pop_item()

    def reset(self): 
        self.terminal.clear()
        self.editor.clear_highlight()

    def wait(self, call_back):
        self.root.after(self.delay, call_back)

    def new_line_terminal(self):
        self.terminal.create_text()

    def write_terminal(self, val):
        self.terminal.add_text(val)

    def input_done(self):
        self.terminal.entered.set(self.terminal.entered.get())

    def get_terminal(self):
        val = self.terminal.get_entry()
        return val
    
    def line_is_breakpoint(self, line) -> bool: 
        return self.editor.linenumbers.breakpoints[line]

    def clear_highlight(self):
        self.editor.clear_highlight()

    def program_end(self): 
        self.play_button.config(image=self.play_image)
        self.clear_highlight()

    def stack_int(self): 
        self.stack.int_mode()
    def stack_float(self): 
        self.stack.float_mode() 
    def stack_char(self):
        self.stack.char_mode()
    def stack_bin(self):
        self.stack.bin_mode()
    def stack_hex(self):
        self.stack.hex_mode()