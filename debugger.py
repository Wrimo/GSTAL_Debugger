# ---------------------------------------------------------
# File--------debugger.py
# Developer---Brennan Cottrell
# Date--------January, 14 2023
#
# A program to allow the writing and debugging of
# GSTAL programs.
# -------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
from GSTAL_Virtual_Machine import GSTALVM
import os
import subprocess


def open_file(event=None):
    global file_path
    path = askopenfilename()
    file_path = path
    with open(path, "r") as file:
        code = file.read()
        vm.load(os.path.basename(file_path))
        editor.delete(1.0, END)
        editor.insert(1.0, code)


def new_file(event=None):
    global file_path
    file_path = ""
    vm.reset()
    editor.delete(1.0, END)
    editor.insert(END, "NOP ;GSTAL Debugger")


def save_file(event=None):
    global file_path
    if file_path == '':
        save_path = asksaveasfilename()
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        print("basename", os.path.basename(file_path))
        file.write(code)

    vm.load(os.path.basename(file_path))

def save_as(event=None):
    global file_path
    save_path = asksaveasfilename()
    file_path = save_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)

    vm.load(os.path.basename(file_path))

def close(event=None):
    root.destroy()


def run(event=None):
    vm.reset()
    vm.run()

def stop(event=None):
    vm.reset()


def step_run(event=None):
    pass

def run_end(event=None):
    pass

def exit(event=None):
    pass




root = Tk()
root.geometry("1366x768")
root.title = "GSTAL Debugger"


menu = Menu(root)
root.config(menu=menu)

root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_as)
root.bind("<Control-q>", close)


root.grid_rowconfigure(0, weight=2)

editor = ScrolledText(root, font=("haveltica 9 bold"),  wrap="none", width=45, height=45)
editor.grid(column=0, row=0)

output = ScrolledText(root, font=("haveltica 9 bold"),  wrap="none", width=45, height=45)
output.grid(column=1, row=0)


output.insert(END, "Output!")
# output.config(state='disabled')


file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
options_menu = Menu(menu, tearoff=0)


menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label="Options", menu=options_menu)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="New File", accelerator="Ctrl+N", command=new_file)
file_menu.add_separator()
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(
    label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)
run_menu.add_command(label="Run", accelerator="F5", command=run)
run_menu.add_command(label="Stop", command=stop)
run_menu.add_separator()
run_menu.add_command(label="Step run", command=step_run)
run_menu.add_command(label="Run to end", command=run_end)

vm = GSTALVM()
vm.output = output
new_file()


root.mainloop()
