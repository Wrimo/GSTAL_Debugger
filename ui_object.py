# ---------------------------------------------------------
# File--------ui_object.py
# Developer---B. Cottrell
# Date--------February, 4 2023
#
# Custom UI widgets to allow for features not provided by default in
# tkinter.
# -------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
import tkinter as tk
import textwrap
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from enum import Enum

# Adds text at the bottom, expanding upwards. Useful for visualisation of stack.
class StackObject(Frame):
    class State(Enum):
        INT = 0
        FLOAT = 1
        CHAR = 2
        BINARY = 3
        HEXADECIMAL = 4

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(
            self, bg="grey", height=kwargs["height"], width=kwargs["width"])

        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.pack(side=RIGHT, fill=Y)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.height = kwargs["height"]
        self.x = 10
        self.y = kwargs["height"]
        self.stack = []
        self.state = StackObject.State.INT
        self.font = Font(family="haveltica", size=20, weight="bold")

    def add_text(self, s):
        text = self.canvas.create_text(
            self.x, self.y, anchor=SW, font=self.font)
        self.y -= 25
        self.canvas.itemconfigure(text, text=s)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.y < 0:
            self.canvas.yview_moveto('0.0')
        return text

    def highglight_text(self, text):
        self.canvas.itemconfigure(text, fill="red")

    def update_stack(self, stack, act):
        for i in range(0, len(stack)):
            if self.stack[i][0] != stack[i]:  # item has changed
                self.canvas.itemconfigure(self.stack[i][1], text=f"{i}: {self.convert_item(stack[i], self.state)}")
            if i == act:
                self.highglight_text(self.stack[i][1])

    def push_item(self, item):  # add an item to the stack
        value = self.convert_item(item, self.state)
        self.stack.append((item, self.add_text(
                f"{len(self.stack)}: {value}")))

    def pop_item(self):  # remove last item from the stack
        last = len(self.stack) - 1
        self.canvas.delete(self.stack[last][1])
        self.y += 25
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        del self.stack[last]

    def int_mode(self):
        if self.state == StackObject.State.INT:
            return
        self.font.config(size=20)
        self.state = StackObject.State.INT
        for i in range(0, len(self.stack)):
            self.canvas.itemconfigure(
                self.stack[i][1], text=f"{i}: {self.stack[i][0].int()}")

    def float_mode(self):
        if self.state == StackObject.State.FLOAT:
            return
        self.font.config(size=20)
        self.state = StackObject.State.FLOAT
        for i in range(0, len(self.stack)):
            self.canvas.itemconfigure(
                self.stack[i][1], text=f"{i}: {self.stack[i][0].float()}")

    def char_mode(self):
        if self.state == StackObject.State.CHAR:
            return
        self.font.config(size=22)
        self.state = StackObject.State.CHAR
        for i in range(0, len(self.stack)):
            c = self.stack[i][0].char()
            self.canvas.itemconfigure(
                self.stack[i][1], text=f"{i}: {c}")
            
    def bin_mode(self):
        if self.state == StackObject.State.BINARY:
            return
        self.font.config(size=9)
        self.state = StackObject.State.BINARY
        for i in range(0, len(self.stack)):
            c = self.stack[i][0].bin()
            self.canvas.itemconfigure(
                self.stack[i][1], text=f"{i}: {c}")

    def hex_mode(self):
        if self.state == StackObject.State.HEXADECIMAL:
            return
        self.font.config(size=18)
        self.state = StackObject.State.HEXADECIMAL
        for i in range(0, len(self.stack)):
            c = self.stack[i][0].hex()
            self.canvas.itemconfigure(
                self.stack[i][1], text=f"{i}: {c}")
            
    def convert_item(self, x, type):
        if type == StackObject.State.INT: 
            return x.int() 
        elif type == StackObject.State.FLOAT: 
            return x.float() 
        elif type == StackObject.State.CHAR:
            return x.char()
        elif type == StackObject.State.BINARY:
            return x.bin()
        elif type == StackObject.State.HEXADECIMAL:
            return x.hex()


# allows for outputing of text and textbox entry 
class TerminalObject(Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(
            self, bg="grey", height=kwargs["height"], width=kwargs["width"])

        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.pack(side=RIGHT, fill=Y)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.height = self.y = kwargs["height"] - 20
        self.width = kwargs["width"]
        self.x = 10

        self.line = None
        self.entered = IntVar()

    def create_text(self):
        self.y += 25
        self.line = self.canvas.create_text(
            self.x, self.y, anchor=SW, font=("haveltica 12"))

    def add_text(self, s):
        if self.line is None:
            self.create_text()

        self.canvas.insert(self.line, "end", s)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto('1.0')

    def add_entry(self):
        self.entry = Entry(self, width=45, bg="grey",
                           disabledbackground="grey",
                           disabledforeground="black",
                           borderwidth=0, highlightthickness=0, font=("haveltica 12"))
        self.entry.focus_set()
        self.y += 25
        self.canvas.create_window(self.x, self.y, window=self.entry, anchor=SW)
        self.create_text()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto('1.0')

    def get_entry(self):
        self.add_entry()
        self.wait_variable(self.entered)
        self.entry.configure(state="disabled")
        return self.entry.get()

    def clear(self):
        self.y = self.height
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.create_text()

# simple wrapper for labels, used to display register values
class RegisterObject(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.text = kwargs["text"]

    def write(self, val):
        self.configure(text=f"{self.text} {val}")

# editor object to allow for showing line number and break points
class EditorObject(ScrolledText):
    def __init__(self, *args, **kwargs):
        ScrolledText.__init__(self, *args, **kwargs)
        self.line = 0

    def highlight_line(self, line):
        self.remove_highlight(self.line)
        self.tag_add("step", float(line), f"{float(line)} lineend")
        self.line = line

    def clear_highlight(self):
        self.remove_highlight(self.line)

    def remove_highlight(self, line):
        self.tag_remove("step", float(line), f"{float(line)} lineend")
