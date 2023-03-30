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
from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from GSTAL_Virtual_Machine import GSTALVM
import os

from uimanager import *

# USER ACTIONS
def open_file(event=None):
    global file_path
    stop()
    old_path = file_path
    path = askopenfilename()
    file_path = path
    try:
        with open(path, "r") as file:
            code = file.read()
            editor.clear()
            editor.insert(code)
            clear_breakpoints()
    except:
        v.write_terminal("An error occurred opening the file")
        file_path = old_path

    root.title("The BC GSTAL Debugger")


def new_file(event=None):
    global file_path
    file_path = ""
    vm.full_reset()
    editor.clear()
    editor.insert("NOP ;WELCOME TO THE BC GSTAL Debugger")


def save_file(event=None):
    global file_path
    if file_path == '':
        save_path = asksaveasfilename()
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get()
        file.write(code)

    root.title("The BC GSTAL Debugger") 


def save_as(event=None):
    global file_path
    save_path = asksaveasfilename()
    file_path = save_path
    with open(save_path, "w") as file:
        code = editor.get()
        file.write(code)
    root.title("The BC GSTAL Debugger") 


def close(event=None):
    root.destroy()


def run(event=None):
    config_start()
    vm.run()


def stop(event=None):
    play_button.config(image=play_img)
    vm.stop()


def step_run(event=None):
    if vm.finished_execution():
        config_start()
    vm.execute()


def run_end(event=None):
    if vm.finished_execution():
        vm.stack_reset()
        play_button.config(image=stop_img)
    vm.run()


def slider_change(event=None):
    v.delay = int(speed_slider.get() * 1000)


def run_button(event=None):
    if not vm.finished_execution():
        vm.stop()
    else:
        run()
    return


def about(event=None):
    new_win = Toplevel(root)
    new_win.geometry("+1+1")
    new_win.title("About")
    new_win.resizable(0, 0)
    can = Canvas(new_win, width=400, height=400)
    can.grid(column=0, row=0)
    can.create_text(45, 50, text="ABOUT", font=("haveltica 16 bold"))
    can.create_text(45, 100, anchor=W, text="The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse. The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse.The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse.The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse.")
    
    # Label(new_win, text="The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse.", font=("haveltica 9 bold")).grid(column=0, row=0, sticky=W)
    # Label(new_win, text="GSTAL is the target language used in the Lipscomb Compiler course, and this program was created to make debugging it easier.", font=("haveltica 9 bold")).grid(column=0, row=1, sticky=W)
    # Label(new_win, text="").grid(column=0, row=2)
    # Label(new_win, text="Credits:\n Dr. Bryan Crawley (advisor) \n Bethany Cadena (GSTAL virtual machine) \n Brennan Curtis Cottrell (GUI debugger)", font=("haveltica 9 bold")).grid(column=0, row=3, sticky=W)

    
def help(event=None):
    showinfo("Help", "Here's some help on how to use the BC GSTAL Debugger")

def exit(event=None):
    on_exit()

def clear_breakpoints(event=None): 
    v.clear_all_breakpoints()

def enter_pressed(event):
    v.input_done()


# HELPER FUNCTIONS
def config_start():
    v.program_start()
    vm.load(file_path)
    play_button.config(image=stop_img)

def on_exit():
    vm.entered.set(vm.entered.get())
    root.destroy()
    exit()


root = Tk()
root.title("The BC Gstal Debugger")
root.geometry("+1+1")
root.resizable(0, 0)
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

control_frame = Frame(root, width=400, height=10)
control_frame.grid(column=0, row=0, columnspan=2, sticky=NSEW)


editor_frame = Frame(root, width=400, height=400)
editor_frame.grid(column=0, row=1, sticky=NSEW, rowspan=2)

root.grid_columnconfigure(0, weight=1)

output_frame = Frame(root, width=400, height=400)
output_frame.grid(column=1, row=1, sticky=NSEW)

stack_reg_frame = Frame(root, width=400, height=400)
stack_reg_frame.grid(column=1, row=2, sticky=NSEW)

stack_frame = Frame(stack_reg_frame, width=350, height=400)
stack_frame.grid(column=0, row=0, sticky=NSEW)

reg_frame = Frame(stack_reg_frame, bg="grey", width=40, height=400)
reg_frame.grid(column=1, row=0, sticky=NSEW)

stack_reg_frame.grid_columnconfigure(1, weight=1)

# control bar
play_img = tk.PhotoImage(file="Assets/play.png")
stop_img = tk.PhotoImage(file="Assets/stop-button.png")
play_button = tk.Button(control_frame, image=play_img,
                        command=run_button, compound=CENTER)
play_button.grid(column=0, row=0, padx=1, pady=1)

fastforward_img = tk.PhotoImage(file="Assets/fast-forward.png")
runend_button = tk.Button(
    control_frame, image=fastforward_img, command=run_end, compound=CENTER)
runend_button.grid(column=1, row=0, padx=1, pady=1)


arrow_img = tk.PhotoImage(file="Assets/right-arrow.png")
step_button = tk.Button(control_frame, image=arrow_img,
                        command=step_run, compound=CENTER)
step_button.grid(column=2, row=0, padx=1)

speed_label = Label(control_frame, text="Speed", font=("haveltica 9 bold"))
speed_label.grid(column=3, row=0, padx=1, pady=1)

speed_slider = ttk.Scale(control_frame, from_=1, to=0,
                         orient="horizontal", command=slider_change)
speed_slider.grid(column=4, row=0, padx=1, pady=1)


# editor
editor = EditorBox(editor_frame, width=30, height=90)
editor.grid(column=0, row=0, sticky=NSEW)

# output
output = TerminalObject(output_frame, width=550, height=350)
output.grid(column=0, row=0, sticky=NSEW)


# stack and register view
stack = StackObject(stack_frame, width=390, height=300)
stack.grid(column=0, row=0, sticky=NSEW)

stack_buttons = Frame(stack_frame, bg="grey", width=200, height=100)
stack_buttons.grid(column=0, row=1, sticky=EW, padx=1)

int_button = Button(stack_buttons, text="INT", command=v.stack_int)
int_button.grid(column=1, row=0, padx=20, sticky=EW)

float_button = Button(stack_buttons, text="FLOAT", command=v.stack_float)
float_button.grid(column=2, row=0, padx=20, sticky=EW)

char_button = Button(stack_buttons, text="CHAR", command=v.stack_char)
char_button.grid(column=3, row=0, padx=20, sticky=EW)

hex_button = Button(stack_buttons, text="HEX", command=v.stack_hex)
hex_button.grid(column=4, row=0, padx=20, sticky=EW)

# bin_button = Button(stack_buttons, text="BIN", command=v.stack_bin)
# bin_button.grid(column=5, row=0, padx=5)



tos_label = RegisterObject(reg_frame, bg="grey", text="tos",
                           font=("haveltica 26"))
tos_label.grid(column=0, row=0, pady=30, padx=15, sticky=W)
pc_label = RegisterObject(reg_frame, bg="grey",
                          text="pc", font=("haveltica 26"))
pc_label.grid(column=0, row=1, pady=30, padx=15, sticky=W)

act_label = RegisterObject(reg_frame, bg="grey", text="act",
                           font=("haveltica 26"))
act_label.grid(column=0, row=2, pady=30, padx=15, sticky=W)


file_menu = Menu(menu, tearoff=0)
debug_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
more_menu = Menu(menu, tearoff=0)


v.fast_mode = BooleanVar()
v.fast_mode.set(False)
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Debug", menu=debug_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label="More", menu=more_menu)
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
debug_menu.add_command(label="Clear breakpoints", command=clear_breakpoints)
debug_menu.add_checkbutton(label="Disable debugging", variable=v.fast_mode, onvalue=True, offvalue=False)
more_menu.add_command(label="About", command=about)
more_menu.add_command(label="Help", command=help)



root.bind("<Return>", enter_pressed)


v.terminal = output
v.editor = editor
v.stack = stack
v.act_label = act_label
v.pc_label = pc_label
v.tos_label = tos_label
v.play_button = play_button
v.play_image = play_img
v.root = root

vm.view = v
speed_slider.set(0.5)
new_file()
root.mainloop()
