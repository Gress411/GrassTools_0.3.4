import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Style
import ttkbootstrap.scrolled as ttks
from ttkbootstrap import Style

import sys


# sys.path.append("..")


def syss(frame, win):
    def click():
        s2 = Style(theme="cyborg")
        win = s2.master

    b1 = ttk.Button(frame, text="click", command=click)
    b1.pack()
