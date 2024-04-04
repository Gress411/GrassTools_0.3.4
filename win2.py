import tkinter as tk
from ttkbootstrap import Style
import win


def create_win2():
    win2 = tk.Toplevel(win.win)
    win2.geometry('400x300')
    win2.title('win2')

    # win2.destroy()

    def c1():
        style = Style(theme="journal")
        win.win = style.master

    def c2():
        style = Style(theme="superhero")
        win.win = style.master

    def c3():
        style = Style(theme="solar")
        win.win = style.master

    # btn = tk.Button(win2, text='win2', command=off)
    # btn.pack()
    tk.Button(win2, text='1', command=c1).pack()
    tk.Button(win2, text='2', command=c2).pack()
    tk.Button(win2, text='3', command=c3).pack()

    win2.mainloop()
