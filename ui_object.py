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

# Adds text at the bottom, expanding upwards. Useful for visualisation of stack. 
class UpwardText(Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(self, bg="grey", height=kwargs["height"], width=kwargs["width"] )
        
        self.vbar=Scrollbar(self,orient=VERTICAL)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.pack(side=RIGHT,fill=Y)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(anchor= tk.CENTER, expand=True)
        
        self.height = kwargs["height"]
        self.x = 10
        self.y = kwargs["height"]

    def add_text(self, s, highlight=False):
        text = self.canvas.create_text(self.x, self.y, anchor=SW, font=("haveltica 20 bold"))
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