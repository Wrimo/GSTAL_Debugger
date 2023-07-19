# ---------------------------------------------------------
# File--------debugger.py
# Developer---B.            Cottrell
# Date--------January, 14 2023
#
# A program to allow the writing and debugging of
# GSTAL programs.
# -------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from GSTAL_Virtual_Machine import GSTALVM

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


def stop(event=None):
    play_button.config(image=play_img)
    play_button_tip.changetext("Start program")
    vm.stop()


def step_run(event=None):
    pause()
    vm.execute()


def run_end(event=None):
    vm.start()
    vm.run()


def no_break_run_end(event=None):
    vm.run_without_stopping()
    vm.run()


def slider_change(event=None):
    v.delay = int(speed_slider.get() * 1000)


def run_button(event=None):
    print(root.winfo_width(), root.winfo_height())
    if not vm.finished_execution():
        pause()
    else:
        run()
    return


def about(event=None):
    new_win = Toplevel(root)
    new_win.title("About")
    Label(new_win, text="ABOUT",
          font=("haveltica 16 bold")).grid(row=0, column=0, sticky=N, pady=25)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The BC GSTAL Debugger is a tool created at Lipscomb University in Nashville, Tenesse.",
          font=("haveltica 12")).grid(row=1, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="GSTAL is the target language for the compiler construction course. This program intends to make debugging GSTAL code simpler and less painful.", font=("haveltica 12")).grid(row=2, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="Credits:\n-Bethany Cadena (GSTAL virtual machine)\n-Brennan Curtis Cottrell (GUI debugger)\n-Dr. Bryan Crawley (advisor)",
          font=("haveltica 12")).grid(row=3, column=0, sticky=W, pady=10, padx=10)


def help(event=None):
    new_win = Toplevel(root)
    new_win.title("Help")
    Label(new_win, text="HELP",
          font=("haveltica 16 bold")).grid(row=0, column=0, sticky=N, pady=25)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The main purpose of the The BC GSTAL Debugger is debugging GSTAL code, but it can also be used to create and write new GSTAL programs.",
          font=("haveltica 12")).grid(row=1, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="SECTIONS",
          font=("haveltica 14")).grid(row=2, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="There are five main sections to the BC GSTAL Debugger that work together to create the ultimate GSTAL programming experience",
          font=("haveltica 12")).grid(row=3, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The editor is used for editing GSTAL code and setting breakpoints.",
          font=("haveltica 12")).grid(row=4, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The stack shows values stored in the GSTAL Virtual Machine stack during runtime.",
          font=("haveltica 12")).grid(row=4, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The register view shows the current values of GSTAL's three registers.",
          font=("haveltica 12")).grid(row=5, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The output window displays program ouput and prompts the user for input.",
          font=("haveltica 12")).grid(row=6, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="The control bar offers control of program execution. The play/pause button is for starting and stopping execution. Stop stops the program. "
          "Run to next breakpoint resumes normal execution from a pause, while run to end will continue executing but skip breakpoints. "
          "Step run executes the only the next instruction",
          font=("haveltica 12")).grid(row=6, column=0, sticky=W, pady=10, padx=10)

    Label(new_win, justify=LEFT, wraplength=500,
          text="OTHER FEATURES",
          font=("haveltica 14")).grid(row=7, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="Disable debugging option - turns off all debugging features and runs the program as fast as possible. Cannot be changed during program execution.",
          font=("haveltica 12")).grid(row=8, column=0, sticky=W, pady=10, padx=10)
    Label(new_win, justify=LEFT, wraplength=500,
          text="Clear all breakpoints - option in the Debug menu to clear all current breakpoints.",
          font=("haveltica 12")).grid(row=9, column=0, sticky=W, pady=10, padx=10)


def exit(event=None):
    on_exit()


def clear_breakpoints(event=None):
    v.clear_all_breakpoints()


def enter_pressed(event):
    v.input_done()


# HELPER FUNCTIONS
def run():
    config_start()
    vm.run()


def pause():
    vm.pause()


def config_start():
    v.program_start()
    vm.load(file_path)
    vm.start()
    play_button.config(image=pause_img)
    play_button_tip.changetext("Pause program")


def on_exit():
    vm.entered.set(vm.entered.get())
    root.destroy()
    exit()

# WINDOW CONFIGURATION

root = Tk()
root.title("The BC Gstal Debugger")
root.minsize(825, 420)
root.geometry("850x700")

root.iconbitmap("Assets/bison-icon.ico")

vm = GSTALVM()
v = View()

menu = Menu(root)
root.config(menu=menu)
root.focus()

# KEYBOARD SHORTCUTS

root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_as)
root.bind("<Control-q>", close)
root.bind("<Return>", enter_pressed)


# FRAME CREATION
control_frame = Frame(root, width=400, height=10)
control_frame.grid(column=0, row=0, columnspan=2, sticky=NSEW, pady=10)

editor_frame = Frame(root, width=400, height=200)
editor_frame.grid(column=0, row=1, sticky=NSEW, rowspan=2)


output_frame = Frame(root, width=400, height=200)
output_frame.grid(column=1, row=1, sticky=NSEW)

stack_reg_frame = Frame(root, width=400, height=200)
stack_reg_frame.grid(column=1, row=2, sticky=NSEW)

stack_frame = Frame(stack_reg_frame, width=300, height=200)
stack_frame.grid(column=0, row=0, sticky=NSEW, columnspan=1)

reg_frame = Frame(stack_reg_frame, bg="grey", width=100, height=200)
reg_frame.grid(column=1, row=0, sticky=NSEW, columnspan=2)

stack_reg_frame.columnconfigure(0, weight=1)
stack_reg_frame.rowconfigure(0, weight=1)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)


# CONTROL BAR
play_img = tk.PhotoImage(file="Assets/play.png")
pause_img = tk.PhotoImage(file="Assets/pause.png")
stop_img = tk.PhotoImage(file="Assets/stop.png")
continue_img = tk.PhotoImage(file="Assets/continue.png")
fastforward_img = tk.PhotoImage(file="Assets/forward-icon.png")
arrow_img = tk.PhotoImage(file="Assets/stair.png")


play_button = tk.Button(control_frame, image=play_img, command=run_button, compound=CENTER)
play_button.grid(column=0, row=0, padx=1, pady=1, sticky=W)
play_button_tip = ToolTip(play_button, "Start program")

stop_button = tk.Button(control_frame, image=stop_img, command=stop, compound=CENTER)
stop_button.grid(column=1, row=0, padx=1, pady=1, sticky=E)
stop_button_tip = ToolTip(stop_button, "Stop program")

runend_button = tk.Button(control_frame, image=continue_img, command=run_end, compound=CENTER)
runend_button.grid(column=2, row=0, padx=1, pady=1, sticky=W)
run_end_tip = ToolTip(runend_button, "Run to next breakpoint")

run_nobreak = tk.Button(control_frame, image=fastforward_img, command=no_break_run_end, compound=CENTER)
run_nobreak.grid(column=3, row=0, padx=1, pady=1, sticky=W)
run_nobreak_tip = ToolTip(run_nobreak, "Run to end of program")

step_button = tk.Button(control_frame, image=arrow_img, command=step_run, compound=CENTER)
step_button.grid(column=4, row=0, padx=1, sticky=W)
step_button_tip = ToolTip(step_button, "Execute next instruction")

button_contain = ButtonContainer(play_button, stop_button, runend_button, run_nobreak, step_button)

speed_label = Label(control_frame, text="Speed -", font=("courier 9 bold"))
speed_label.grid(column=5, row=0, padx=1, pady=1, sticky=W)

speed_slider = ttk.Scale(control_frame, from_=1, to=0, orient="horizontal", command=slider_change)
speed_slider.grid(column=6, row=0, padx=1, pady=1, sticky=W)

minus_label = Label(control_frame, text="+", font=("courier 9 bold"))
minus_label.grid(column=7, row=0, padx=1, pady=1, sticky=W)

control_frame.rowconfigure(0, weight=4)

# EDITOR
editor = EditorBox(editor_frame)
editor.grid(column=0, row=0, sticky=NSEW)
editor_frame.columnconfigure(0, weight=1)
editor_frame.rowconfigure(0, weight=1)

# OUTPUT
output = TerminalObject(output_frame, width=550, height=350)
output.grid(column=0, row=0, sticky=NSEW)
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)

# STACK AND REGISTER VIEW
stack = StackObject(stack_frame, width=300, height=300)
stack.grid(column=0, row=0, sticky=NSEW)

stack_buttons = Frame(stack_frame, width=10, height=100)
stack_buttons.grid(column=0, row=1)

stack_frame.columnconfigure(0, weight=1)
stack_frame.rowconfigure(0, weight=1)


button_font = "courier 9"
int_button = Button(stack_buttons, text="INT", command=v.stack_int, font=button_font, width=5)
int_button.grid(column=0, row=0, padx=5) 

float_button = Button(stack_buttons, text="FLOAT", command=v.stack_float, font=button_font, width=5)
float_button.grid(column=1, row=0, padx=5

char_button = Button(stack_buttons, text="CHAR", command=v.stack_char, font=button_font, width=5)
char_button.grid(column=2, row=0, padx=5)

hex_button = Button(stack_buttons, text="HEX", command=v.stack_hex, font=button_font, width=5)
hex_button.grid(column=3, row=0, padx=5) 

label_font = "courier 16"
tos_label = RegisterObject(reg_frame, width=7, bg="grey", text="tos",
                           font=label_font, anchor=W)
tos_label.grid(column=0, row=0, pady=15, padx=10, sticky=W)
pc_label = RegisterObject(reg_frame, bg="grey",  width=7,
                          text="pc", font=label_font, anchor=W)
pc_label.grid(column=0, row=1, pady=15, padx=10, sticky=W)

act_label = RegisterObject(reg_frame, bg="grey", text="act",  width=7,
                           font=label_font, anchor=W)
act_label.grid(column=0, row=2, pady=15, padx=10, sticky=W)

# reg_frame.columnconfigure(0, weight=1)
reg_frame.rowconfigure(0, weight=1)
reg_frame.rowconfigure(1, weight=1)
reg_frame.rowconfigure(2, weight=1)


# MENU CREATION

file_menu = Menu(menu, tearoff=0)
debug_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
more_menu = Menu(menu, tearoff=0)


v.fast_mode = BooleanVar()
v.fast_mode.set(False)
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label="Debug", menu=debug_menu)
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


# SETUP VIEW
# views hold the ui objects and has functions to interact with them

v.terminal = output
v.editor = editor
v.stack = stack
v.act_label = act_label
v.pc_label = pc_label
v.tos_label = tos_label
v.play_button = play_button
v.play_image = play_img
v.root = root
v.buttons = button_contain

vm.view = v
speed_slider.set(0.5)
new_file()
root.mainloop()
