import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Style
import ttkbootstrap.scrolled as ttks
import threading
import windnd
from ffmpeg import FFmpeg
import asyncio
import re
import os

# import compress_video_ffmpeg as cvf

b1 = ttk.Floodgauge

terminal_text = ""
files = []

newSet = {}
scroll_terminal = ttks.ScrolledText

terminal_lines = 0

newName = ""
select = ttk.IntVar

scroll_renhua = ttks.ScrolledText


def vi(frame):
    global b1
    global terminal_text
    global scroll_terminal
    global scroll_renhua
    global select

    # 开始按钮

    # 逻辑核心-----------------------------------------------------------
    def click(e):
        # t2 = threading.Thread(target=start_thr, args=(files[0]))
        # t2.start()
        ffmpeg2 = FFmpeg().option('y').input(files[0])
        asyncio.run(ffmpeg2.execute())

    b1 = ttk.Floodgauge(frame, cursor='rtl_logo', mask="当前进度{}%", font=("微软雅黑", 12))
    b1.bind("<Button>", click)
    b1.pack(fill=ttk.X, side=ttk.BOTTOM)

    # 文件列表框
    # state = 'disable' normal
    scroll_files = ttks.ScrolledText(frame, autohide=False, padding=12)
    scroll_files.insert(ttk.END, '该功能尚未完成!\n该功能尚未完成!\n该功能尚未完成!')
    # print(scroll_files.get('1.0', 'end-1c'))
    scroll_files.place(width=400, height=90, x=-2, y=10)

    # 必填项
    necessary1 = ttk.Labelframe(frame, text="  输出设置  ", width=200, height=135, bootstyle="danger")
    necessary1.place(x=10, y=100)

    def new_name_click():
        messagebox_thr('帮助', '给处理后的视频起个名字吧!\n顺便，不改变播放速度即通过抽帧来达到目的\n改变播放速度会自动删除音频且不会影响画质', 'info')

    new_name = ttk.Button(necessary1, text="名称", command=new_name_click)
    new_name.place(x=13, y=6, width=50, height=28)
    # 输入框
    new_name_entry = ttk.Entry(necessary1)
    new_name_entry.insert('end', '输出文件名')

    def click_del_name_entry(e):
        if new_name_entry.get() == '输出文件名':
            new_name_entry.delete(0, ttk.END)

    new_name_entry.bind("<Button>", click_del_name_entry)
    new_name_entry.place(x=63, y=6, width=123, height=28)
    # 模式选择
    select = ttk.IntVar()
    select.set(1)

    def no_change_speed_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“不改变播放速度”\n这需要重新编码，并可能损失些许画质。慎用极低帧率\n音频不受影响")

    def change_speed_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“改变播放速度”\n不需要重新编码且速度极快，用于配合压制面板处理图片序列\n但音频会被删除，毕竟这会导致音画不同步")

    no_change_speed = ttk.Radiobutton(necessary1, text="不改变播放速度", value=1, variable=select,
                                      bootstyle="outline-toolbutton", command=no_change_speed_click)

    no_change_speed.place(x=13, y=42, width=173, height=28)

    change_speed = ttk.Radiobutton(necessary1, text="改变播放速度", value=2, variable=select,
                                   bootstyle="danger-outline-toolbutton", command=change_speed_click)
    change_speed.place(x=13, y=79, width=173, height=28)

    # 帧数选择
    necessary2 = ttk.Labelframe(frame, text="  目标帧数及编码类型  ", width=165, height=135, bootstyle="danger")
    necessary2.place(x=220, y=100)

    # 滑块
    def scale_change_value(v):
        # print(v)
        v2 = str(round(float(v)))
        new_frames.delete(0, ttk.END)
        new_frames.insert('end', v2)
        # frames_v.set(str(round(float(v))))

    scale1 = ttk.Scale(necessary2, from_=1, to=240, command=scale_change_value)
    scale1.place(x=13, y=6, width=140, height=30)

    # 帧数选择输入框
    # frames_v = ttk.IntVar()
    new_frames = ttk.Entry(necessary2)
    new_frames.insert('end', '在此输入')

    def click_del_new_frames(e):
        if new_frames.get() == '在此输入':
            new_frames.delete(0, ttk.END)

    def new_frames_button_click():
        messagebox_thr('帮助', '在右边填入目标帧数吧\n可以用滑块来选择，但不建议这么做', 'info')

    new_frames.bind("<Button>", click_del_new_frames)
    new_frames.place(x=63, y=42, width=90, height=28)
    new_frames_button = ttk.Button(necessary2, text="帧数", command=new_frames_button_click)
    new_frames_button.place(x=13, y=42, width=50, height=28)

    # 编码类型
    select_code = ttk.Combobox(necessary2)
    select_code['value'] = ['h.264', 'h.265']
    select_code.current(0)
    select_code.place(x=63, y=79, width=90, height=28)

    def new_name_click():
        messagebox_thr('帮助', '请选择原视频的编码格式\n如果不知道原视频的编码格式，可以去视频信息窗口查看\n如果选择了“不改变播放速度”则无需更改此项', 'info')

    select_code_button = ttk.Button(necessary2, text="编码", command=new_name_click)
    select_code_button.place(x=13, y=79, width=50, height=28)

    # 仪表盘
    # meter2 = ttk.Meter(
    #     frame,
    #     metersize=110,
    #     amountused=23,
    #     amounttotal=51,
    #     textfont="-size 13",
    #     metertype="semi",
    #     subtext="快速调节",
    #     interactive=True,
    # )
    # meter2.place(x=225, y=145)

    # 控制台输出
    scroll_terminal = ttks.ScrolledText(frame, autohide=True, padding=12)
    scroll_terminal.insert(ttk.END, terminal_text)
    scroll_terminal.place(width=400, height=200, x=-2, y=240)

    # 人话输出
    scroll_renhua = ttks.ScrolledText(frame, autohide=True, padding=(12, 12, 12, 0), font="微软雅黑 100")
    scroll_renhua.insert(ttk.END, terminal_text)
    scroll_renhua.insert(1.0, "欢迎使用草工具箱 beta v0.2.9")
    scroll_renhua.place(width=400, height=75, x=-2, y=430)

    # 拖拽文件
    def dragged_files(f):
        global files
        files = []
        apps = []
        for file in f:
            apps.append(file.decode('gbk'))
        files = apps
        # print(files[0])
        files_line = ""
        for f in files:
            files_line = files_line + f + "\n"

        scroll_files.delete(1.0, ttk.END)
        scroll_files.insert(ttk.END, files_line)

    def dropfiles_thread(f):
        t = threading.Thread(target=dragged_files, args=(f,))
        t.start()

    windnd.hook_dropfiles(frame, func=dropfiles_thread)

    def messagebox_thr(tit, msg, typ):
        def run_messagebox_thr_info(t, m):
            tkinter.messagebox.showinfo(t, m)

        def run_messagebox_thr_warning(t, m):
            tkinter.messagebox.showwarning(t, m)

        if typ == "info":
            t = threading.Thread(target=run_messagebox_thr_info, args=(tit, msg))
            t.start()
        else:
            t = threading.Thread(target=run_messagebox_thr_warning, args=(tit, msg))
            t.start()

    # zhu=ttk.Label(frame,text="朱天成",font="仿宋 100")
    # zhu.place(width=400, height=200, x=-2, y=280)
    # b1 = ttk.Button(frame, text='1', width=3)
    # b1.pack(fill=ttk.Y, side=ttk.LEFT)
    #
    # b2 = ttk.Button(frame, text='2')
    # b2.pack(fill=ttk.X, side=ttk.TOP)


def testdef():
    scroll_terminal.delete(1.0, ttk.END)
    scroll_terminal.insert(ttk.END, "test!")


def time2seconds(time):
    h = int(time[0:2])
    # print("时：" + str(h))
    m = int(time[3:5])
    # print("分：" + str(m))
    s = int(time[6:8])
    # print("秒：" + str(s))
    ms = int(time[9:12])
    # print("毫秒：" + str(ms))
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    return False


def export_raw_url(p):
    return os.path.dirname(p) + '\\' + os.path.splitext(os.path.basename(p))[0] + '.h264'
