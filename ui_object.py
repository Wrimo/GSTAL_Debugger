# ---------------------------------------------------------
# File--------ui_object.py
# Developer---B. Cottrell
# Date--------February, 4 2023
#
# Custom UI widgets to allow for features not provided by default in
# tkinter.
# -------------------------------------------------------------------

from collections import defaultdict
from tkinter import *
from tkinter import ttk
import tkinter as tk
from textwrap import TextWrapper
import tkinter
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

    class StackItem:
        def __init__(self, canvas, index, value, coord, font_size):
            self.background = canvas.create_rectangle(coord[0] - 50, coord[1] - 15, coord[0] + 350,  coord[1] + 25, fill="#484848")
            self.in_text = canvas.create_text(2, coord[1] + 25, anchor=SW, font=f"courier 20 bold")
            canvas.itemconfig(self.in_text, text=f"{index}")
            self.value_text = canvas.create_text(80, coord[1] + 25, anchor=SW, font=f"courier {font_size} bold")
            self.line = canvas.create_line(60, coord[1] + 25, 60, coord[1] - 15)
            canvas.itemconfig(self.value_text, text=f"{value}")
            self.canvas = canvas

        def update_value(self, value, font_size):
            self.canvas.itemconfig(self.value_text, font=f"courier {font_size} bold", text=f"{value}")

        def highlight(self):
            self.canvas.itemconfig(self.in_text, fill="red")

        def unhighlight(self):
            self.canvas.itemconfig(self.in_text, fill="black")

        def __del__(self):
            try:
                self.canvas.delete(self.background)
                self.canvas.delete(self.in_text)
                self.canvas.delete(self.value_text)
                self.canvas.delete(self.line)
            except:
                pass  # the only issue here occurs when the program is being exited and the destruction of root destroyed these widgets before this code runs.

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(
            self, bg="grey", height=kwargs["height"], width=kwargs["width"])

        self.vbar = Scrollbar(self, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=BOTH)
        self.canvas.pack(anchor=tk.CENTER, expand=True, fill=BOTH)

        self.height = kwargs["height"]
        self.x = 10
        self.y = kwargs["height"]
        self.stack = []
        self.state = StackObject.State.INT
        self.font_size = 20
        self.gap = 40
        self.autoscroll = True
        self.highlighted = None  # used to keep track of the highlighted entry to unmark it on change

        def unbind(event): 
            self.canvas.unbind_all("<MouseWheel>")
        def bind(event):
            self.canvas.bind_all("<MouseWheel>", self._mousewheel)

        def _scrolled(*args):
            self.autoscroll = False
            self.canvas.yview(*args)

        self.vbar.config(command=_scrolled)
        self.canvas.config(yscrollcommand= self.vbar.set)

        self.canvas.bind("<Enter>", bind)
        self.canvas.bind("<Leave>", unbind)

    def _mousewheel(self, event):
        self.autoscroll = False
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_text(self, value):
        item = StackObject.StackItem(self.canvas, len(self.stack), value, (self.x, self.y), self.font_size)
        self.y -= self.gap
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.y < 0 and self.autoscroll:
            self.canvas.yview_moveto('0.0')
        return item

    def update_stack(self, stack, act):
        if len(self.stack) == 0:  # needed for the case when fast mode is active, so the stack is empty and many things must be added
            for i in range(0, len(stack)):
                self.push_item(stack[i])
            return

        if self.highlighted is not None:
            self.highlighted.unhighlight()

        for i in range(0, len(stack)):
            if self.stack[i][0] != stack[i]:  # item has changed
                self.stack[i][1].update_value(self.convert_item(stack[i]), self.font_size)
            if i == act:
                self.stack[i][1].highlight()

    def push_item(self, item):  # add an item to the stack
        value = self.convert_item(item)
        slot = self.add_text(value)
        self.stack.append((item, slot))

    def pop_item(self):  # remove last item from the stack
        last = len(self.stack) - 1
        self.y += self.gap
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        del self.stack[last]

    def int_mode(self):
        if self.state == StackObject.State.INT:
            return
        self.state = StackObject.State.INT
        self.font_size = 20
        self.change_existing_items()

    def float_mode(self):
        if self.state == StackObject.State.FLOAT:
            return
        self.state = StackObject.State.FLOAT
        self.font_size = 20
        self.change_existing_items()

    def char_mode(self):
        if self.state == StackObject.State.CHAR:
            return
        self.state = StackObject.State.CHAR
        self.font_size = 25
        self.change_existing_items()

    def bin_mode(self):  # not available in the editor
        if self.state == StackObject.State.BINARY:
            return
        self.state = StackObject.State.BINARY
        self.font_size = 8
        self.change_existing_items()

    def hex_mode(self):
        if self.state == StackObject.State.HEXADECIMAL:
            return
        self.state = StackObject.State.HEXADECIMAL
        self.font_size = 16
        self.change_existing_items()

    def change_existing_items(self):
        y = self.height
        for i in range(0, len(self.stack)):
            value = self.stack[i][0]
            text_item = self.stack[i][1]
            text_item.update_value(self.convert_item(value), self.font_size)

    def convert_item(self, x):
        type = self.state
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
        self.vbar.pack(side=RIGHT, fill=BOTH)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(anchor=tk.CENTER, expand=True, fill=BOTH)

        self.height = self.y = kwargs["height"] - 20
        self.width = kwargs["width"]
        self.x = 25

        self.line = None
        self.entered = IntVar()

        def unbind(event): 
            self.canvas.unbind_all("<MouseWheel>")
        def bind(event):
            self.canvas.bind_all("<MouseWheel>", self._mousewheel)

        self.canvas.bind("<Enter>", bind)
        self.canvas.bind("<Leave>", unbind)

    def _mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_text(self):
        self.y += 25
        self.line = self.canvas.create_text(
            self.x, self.y, anchor=NW, font=("courier 10"))

    def add_text(self, s):
        if self.line is None:
            self.create_text()

        bounds = self.canvas.bbox(self.line)
        width = bounds[2] - bounds[0]
        txt = self.canvas.itemcget(self.line, 'text')
        if width > self.width:
            self.canvas.insert(self.line, len(txt) - 1, "\n")
            self.y += 25

        self.canvas.insert(self.line, len(txt), s)

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto('1.0')

    def add_entry(self):
        self.entry = Entry(self, width=45, bg="grey",
                           disabledbackground="grey",
                           disabledforeground="black",
                           borderwidth=0, highlightthickness=0, font=("courier 10"))
        self.entry.focus_set()
        self.y += 35
        self.canvas.create_window(self.x, self.y, window=self.entry, anchor=SW)
        self.create_text()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto('1.0')

    def get_entry(self):
        self.add_entry()
        self.wait_variable(self.entered)
        self.entry.configure(state=DISABLED)
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


# custom widget for the editor box. allows for line numbers and breakpoint selection
class EditorBox(Frame):  # https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        def _scrolled(*args):
            self.autoscroll = False
            self.text.yview(*args)

        self.autoscroll = True
        self.text = EditorBox.CustomText(self, width=40, height=40)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=_scrolled)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("step", background="red")
        self.linenumbers = EditorBox.TextLineNumbers(self, width=50)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.line = 0  # keeps tracks of the last highlighted line so it can cleared. the last hightlighted is not always the last line in sequential order due to jumps
        

    def disable(self):
        self.text.configure(state="disable")

    def enable(self):
        self.text.configure(state="normal")

    def _on_change(self, event):
        self.linenumbers.redraw()

    def get(self):
        return self.text.get(1.0, "end-1c")

    def clear(self):
        self.text.delete(1.0, END)

    def insert(self, text):
        self.text.insert(1.0, text)

    def highlight_line(self, line):
        self.clear_highlight()
        self.text.tag_add("step", float(line), f"{float(line)} lineend")
        if self.autoscroll:
            self.text.see(float(line + 15))
        self.line = line

    def clear_highlight(self):
        self.text.tag_remove("step", float(self.line),
                             f"{float(self.line)} lineend")

    class CustomText(tk.Text):
        def __init__(self, *args, **kwargs):
            tk.Text.__init__(self, *args, **kwargs)

            # create a proxy for the underlying widget
            self._orig = self._w + "_orig"
            self.tk.call("rename", self._w, self._orig)
            self.tk.createcommand(self._w, self._proxy)

        def _proxy(self, *args):
            # let the actual widget perform the requested action
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)

            if(args[0] in ("insert", "replace", "delete")):
                self.winfo_toplevel().title("* The BC GSTAL Debugger")

            # generate an event if something was added or deleted,
            # or the cursor position changed
            if (args[0] in ("insert", "replace", "delete", "see") or
                    args[0:3] == ("mark", "set", "insert") or
                    args[0:2] == ("xview", "moveto") or
                    args[0:2] == ("xview", "scroll") or
                    args[0:2] == ("yview", "moveto") or
                    args[0:2] == ("yview", "scroll")
                ):
                self.event_generate("<<Change>>", when="tail")

            # return what the actual widget returned
            return result

    class TextLineNumbers(tk.Canvas):
        def __init__(self, *args, **kwargs):
            tk.Canvas.__init__(self, *args, **kwargs)
            self.textwidget = None

        def attach(self, text_widget):
            self.textwidget = text_widget
            self.breakpoints = defaultdict(bool)

        def redraw(self, *args):
            '''redraw line numbers'''
            self.delete("all")

            i = self.textwidget.index("@0,0")
            while True:
                dline = self.textwidget.dlineinfo(i)
                if dline is None:
                    break
                y = dline[1]
                linenum = str(i).split(".")[0]
                linenum = int(linenum) - 1

                self.create_text(18, y, anchor=NW, text=linenum)

                if self.breakpoints[linenum]:
                    rect = self.create_rectangle(
                        6, y + 2, 6 + 10, y + 2 + 10, width=0, fill="#db0000")
                else:
                    rect = self.create_rectangle(
                        6, y + 2, 6 + 10, y + 2 + 10, width=0, fill="", activefill="#ff3737")
                self.tag_bind(rect, '<ButtonPress-1>',
                              lambda x,  linenum=linenum: self.breakpoint_click(linenum))
                i = self.textwidget.index("%s+1line" % i)

        def breakpoint_click(self, line):
            self.breakpoints[line] = not self.breakpoints[line]
            self.redraw()

        def clear_breakpoints(self):
            self.breakpoints = defaultdict(bool)
            self.redraw()


class ButtonContainer:  # simple class to handle enabling / disabling buttons based on a state
    def __init__(self, play, stop, run_end, no_break, step):
        self.play = play
        self.stop = stop
        self.run_end = run_end
        self.no_break = no_break
        self.step = step
        self.state_adjust(ProgramState.STOPPED)

    def state_adjust(self, state):
        if state == ProgramState.RUNNING or state == ProgramState.NO_BREAK_RUNNING:
            self.play.configure(state="active")
            self.stop.configure(state="active")
            self.run_end.configure(state="disabled")
            self.no_break.configure(state="disabled")
            self.step.configure(state="disabled")
        elif state == ProgramState.PAUSED:
            self.play.configure(state="disabled")
            self.stop.configure(state="active")
            self.run_end.configure(state="active")
            self.no_break.configure(state="active")
            self.step.configure(state="active")
        elif state == ProgramState.STOPPED:
            self.play.configure(state="active")
            self.stop.configure(state="disabled")
            self.run_end.configure(state="disabled")
            self.no_break.configure(state="disabled")
            self.step.configure(state="disabled")

# Class for tooltips on hover from  https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
class ToolTip(object):

    def __init__(self, widget, text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text = text

        def enter(event):
            self.showtip(self.text)
        def leave(event):
            self.hidetip()

        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 45
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
    def changetext(self, text):
        self.text = text

class ProgramState(Enum):  # simple enum describing state of GSTAL program
    RUNNING = 0
    PAUSED = 1
    STOPPED = 2
    NO_BREAK_RUNNING = 3
