import ttkbootstrap as ttk
from ttkbootstrap import Style

# from FFGUI2.FFMain.page import compress_video
import page.compress_video as compress_video
import page.change_frames as change_frames
import page.fast_clip as fast_clip
import page.mix_picture as mix_picture
import page.video_info as video_info
import page.syss as syss
import page.other as other

import random
from threading import Timer

win = ttk.Window(hdpi=False, alpha=1)
win.title('草工具箱')
win.geometry('400x600')
style = Style(theme="journal")
win = style.master
win.resizable(False, False)

t = Timer


def timer1():
    global t
    compress_video.b0.configure(value=random.random() * 100)
    t = Timer(0.5, timer1)
    t.start()


def click1():
    timer1()


def click2():
    t.cancel()


# scroll_files = ttks.ScrolledText(win, autohide=True)
# scroll_files.pack()

# b1 = ttk.Button(win, text="click", command=click1)
# b1.pack()
# b2 = ttk.Button(win, text="click", command=click2)
# b2.pack()

tab = ttk.Notebook(win)
# 第一个板块
F1 = ttk.Frame(tab, borderwidth=1, border=0)
compress_video.cv(F1)
tab.add(F1, text="压缩视频")

# 第二个板块
F2 = ttk.Frame(tab)
fast_clip.fc(F2)
tab.add(F2, text="裁剪合并")

# 第三个板块
F3 = ttk.Frame(tab)
change_frames.cf(F3)
tab.add(F3, text="帧数转换")

# 第四个板块
F4 = ttk.Frame(tab)
video_info.vi(F4)
tab.add(F4, text="视频信息")

# 第五个板块
F5 = ttk.Frame(tab)
mix_picture.mp(F5)
tab.add(F5, text="序列")

# 第六个板块
F6 = ttk.Frame(tab)
other.other(F6)
tab.add(F6, text="小功能")

# 第七个板块
F7 = ttk.Frame(tab)
syss.syss(F7, win)
tab.add(F7, text="设置")

tab.pack(expand=True, fill=ttk.BOTH)
