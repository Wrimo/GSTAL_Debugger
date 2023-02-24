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

from uimanager import *
from custom_ui import *


# USER ACTIONS
def open_file(event=None):
    global file_path
    global file_name
    path = askopenfilename()
    file_path = path
    with open(path, "r") as file:
        code = file.read()
        vm.load(os.path.basename(file_path))
        editor.delete(1.0, END)
        editor.insert(1.0, code)

    file_name = os.path.basename(file_path)
    v.terminal.clear()


def new_file(event=None):
    global file_path
    file_path = ""
    vm.full_reset()
    editor.delete(1.0, END)
    editor.insert(END, "NOP ;GSTAL Debugger")


def save_file(event=None):
    global file_path
    global file_name
    if file_path == '':
        save_path = asksaveasfilename()
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)

    file_name = os.path.basename(file_path)
    # will need to change this to let the debugger work with files not in the same directory
    vm.load(file_name)


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
    global file_name
    v.reset()
    # start_program()
    vm.stack_reset()
    vm.run()


def stop(event=None):
    stop_program()


def step_run(event=None):
    if vm.finished_execution():
        vm.full_reset()
        v.new_line_terminal()
    vm.execute()


def run_end(event=None):
    vm.editor.clear_highlight()
    vm.run()


def slider_change(event):
    v.delay = int(speed_slider.get() * 1000)

def run_button():
    if vm._pc > 0:
        stop_program()
    else:
        start_program()
    return


def exit(event=None):
    on_exit()
    
# HELPER FUNCTIONS
def enter_pressed(event):
    v.input_done()


def on_exit():
    vm.entered.set(vm.entered.get())
    root.destroy()
    exit()


def start_program():
    # global is_running
    # if not is_running:
    img = tk.PhotoImage(file="Assets/stop-button.png")
    play_button.config(image=img)
    # is_running = True
    vm.full_reset()
    vm.run()


def stop_program():
    # global is_running
    # if is_running:
    is_running = False
    img = tk.PhotoImage(file="Assets/play.png")
    play_button.config(image=img)
    vm.full_reset()


root = Tk()
root.title("The BC Gstal Debugger")
root.geometry("+1+1")
root.resizable(0, 0)
root.title = "GSTAL Debugger"
is_running = False

vm = GSTALVM()
v = View()

menu = Menu(root)
root.config(menu=menu)
root.focus()

root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_as)
root.bind("<Control-q>", close)


# img = tk.PhotoImage(file="Assets/play.png")
# play_button = tk.Button(root, image=img, command=run_button, compound=CENTER)
# play_button.grid(column=0, row=0)


control_frame = Frame(root, width=400, height=10)
control_frame.grid(column=0, row=0, columnspan=2, sticky=NSEW)


editor_frame = Frame(root, width=400, height=400)
editor_frame.grid(column=0, row=1, sticky=NSEW, rowspan=2)

root.grid_columnconfigure(0, weight=1)

output_frame = Frame(root, width=400, height=400)
output_frame.grid(column=1, row=1, sticky=NSEW)

stack_reg_frame = Frame(root, width=400, height=400)
stack_reg_frame.grid(column=1, row=2, sticky=NSEW)

stack_frame = Frame(stack_reg_frame, width=200, height=400)
stack_frame.grid(column=0, row=0, sticky=NSEW)

reg_frame = Frame(stack_reg_frame, bg="grey", width=200, height=400)
reg_frame.grid(column=1, row=0, sticky=NSEW)

stack_reg_frame.grid_columnconfigure(1, weight=1)

# control bar 
speed_label = Label(control_frame, text="Speed", font=("haveltica 9 bold"))
speed_label.grid(column=0, row=0, sticky=E)

speed_slider = ttk.Scale(control_frame, from_=1, to=0, orient="horizontal", command=slider_change)
speed_slider.grid(column=1, row=0, padx=5)

int_button = Button(control_frame, text="INT", command=v.stack_int)
int_button.grid(column=2, row=0)

float_button = Button(control_frame, text="FLOAT", command=v.stack_float)
float_button.grid(column=3, row=0)

char_button = Button(control_frame, text="CHAR", command=v.stack_char)
char_button.grid(column=4, row=0)

bin_button = Button(control_frame, text="BIN", command=v.stack_bin)
bin_button.grid(column=5, row=0)

hex_button = Button(control_frame, text="HEX", command=v.stack_hex)
hex_button.grid(column=6, row=0)

# editor
editor = EditorObject(editor_frame, font=("haveltica 9 bold"),
                      wrap="none", width=45, height=45)
editor.grid(column=0, row=0, sticky=NSEW)
editor.tag_configure("step", background="red")

# output
output = TerminalObject(output_frame, width=550, height=300)
output.grid(column=0, row=0, sticky=NSEW)


# stack and register view 
stack = StackObject(stack_frame, width=370, height=372)
stack.grid(column=0, row=0, sticky=NSEW)

tos_label = RegisterObject(reg_frame, bg="grey", text="tos",
                  font=("haveltica 26 bold"))
tos_label.grid(column=0, row=0, pady=30, padx=15, sticky=NSEW)
pc_label = RegisterObject(reg_frame, bg="grey", text="pc", font=("haveltica 26 bold"))
pc_label.grid(column=0, row=1, pady=30, padx=15, sticky=NSEW)

act_label = RegisterObject(reg_frame, bg="grey", text="act",
                  font=("haveltica 26 bold"))
act_label.grid(column=0, row=2, pady=30, padx=15, sticky=NSEW)



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


root.bind("<Return>", enter_pressed)


v.terminal = output
v.editor = editor
v.stack = stack
v.act_label = act_label
v.pc_label = pc_label
v.tos_label = tos_label
v.root = root

vm.view = v
speed_slider.set(0.5)
new_file()


root.mainloop()
