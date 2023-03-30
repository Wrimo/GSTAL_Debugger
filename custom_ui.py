from tkinter import *
from tkinter import ttk
import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, textwidget, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = textwidget
        self.redraw()

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

        # Refreshes the canvas widget 30fps
        self.after(30, self.redraw)