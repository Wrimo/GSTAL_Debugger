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

# Adds text at the bottom, expanding upwards. Useful for visualisation of stack.


class UpwardText(Frame):
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

    def add_text(self, s, highlight=False):
        text = self.canvas.create_text(
            self.x, self.y, anchor=SW, font=("haveltica 20 bold"))
        self.y -= 25
        self.canvas.itemconfigure(text, text=s)
        if highlight:
            self.canvas.itemconfigure(text, fill="red")
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.y < 0:
            self.canvas.yview_moveto('0.0')

    def reset(self):
        self.y = self.height
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class OutputBox(Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(
            self, bg="grey", height=kwargs["height"], width=kwargs["width"])

        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.pack(side=RIGHT, fill=Y)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.height = self.y = kwargs["height"]
        self.width = kwargs["width"]
        self.x = 10

        self.line = None

    def create_text(self):
        self.line = self.canvas.create_text(
            self.x, self.y, anchor=SW, font=("haveltica 12"))
        self.y += 15

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
        self.canvas.create_window(self.x, self.y, window=self.entry, anchor=SW)
        self.y += 15
        self.create_text()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto('1.0')

    def get_entry(self):
        self.entry.configure(state="disabled")
        return self.entry.get()

    def clear(self):
        self.y = self.height
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.create_text()
