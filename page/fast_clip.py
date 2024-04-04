import tkinter as tk
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
import codecs

b1 = ttk.Floodgauge

terminal_text = ""
files = []

newName = ""
newSet_cut = {'ss': '00:00:00', 'i': '', 'vcodec': 'copy', 'acodec': 'copy', 't': '00:00:31'}
newSet_mix = {'f': 'concat', 'safe': '0', 'i': '', 'c': 'copy'}

scroll_terminal = ttks.ScrolledText
terminal_lines = 0
scroll_renhua = ttks.ScrolledText




def fc(frame):
    global b1
    global terminal_text
    global scroll_terminal
    global scroll_renhua

    # 开始按钮1
    def start_thr(fout, fset):
        use_ffmpeg(fout, fset)

    # 逻辑核心-----------------------------------------------------------
    def click(e):
        global newName
        global newSet_cut
        global newSet_mix

        # newSet_cut = {}
        # 获取新名字
        newName = new_name_entry.get()
        exportUrl = "error"
        try:
            exportUrl = os.path.dirname(files[0]) + "\\" + newName + ".mp4"
        except IndexError:
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "访问文件时出现问题，你把视频拖进来了吗?")
            return

        if select.get() == 1:
            newSet_cut['i'] = files[0]
            newSet_cut['ss'] = time_from_entry.get()
            newSet_cut['t'] = time_to_entry.get()
            t2 = threading.Thread(target=start_thr, args=(exportUrl, newSet_cut))
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "已执行拆分命令")
            t2.start()
        else:
            file_txt = codecs.open('video_names.txt', 'w', 'UTF-8')
            for f in files:
                file_txt.write('file ' + f'\'{f}\'\n')
            file_txt.close()

            # file_names_txt = open("video_names.txt", "w")
            # file_names_txt.writelines('')
            # for f in files:
            #     file_names_txt.write('file ' + f'\'{f}\'\n')
            # file_names_txt.close()

            newSet_mix['i'] = 'video_names.txt'
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "已创建文件列表")
            t2 = threading.Thread(target=start_thr, args=(exportUrl, newSet_mix))
            t2.start()

    b1 = ttk.Floodgauge(frame, cursor='rtl_logo', mask="当前进度{}%", font=("微软雅黑", 12))
    b1.bind("<Button>", click)
    b1.pack(fill=ttk.X, side=ttk.BOTTOM)

    # 文件列表框
    # state = 'disable' normal
    scroll_files = ttks.ScrolledText(frame, autohide=False, padding=12)
    scroll_files.insert(ttk.END, '把文件拖进来吧')
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
        scroll_renhua.insert(1.0, "你选择了“裁剪视频，这不需要重新编码”\n但有可能出现开头跳帧，毕竟处理速度太快了\n格式是  时:分:秒 如0:0:5表示第5秒，请使用英文冒号")

    def change_speed_click():
        scroll_renhua.delete(1.0, ttk.END)
        # 按顺序重写files=======================================================
        scroll_renhua.insert(1.0, "你选择了“拼接视频”\n这也不需要重新编码，但视频的分辨率和编码必须相同\n把需要拼接的视频按顺序拖进来吧")

    no_change_speed = ttk.Radiobutton(necessary1, text="裁剪视频", value=1, variable=select,
                                      bootstyle="outline-toolbutton", command=no_change_speed_click)

    no_change_speed.place(x=13, y=42, width=173, height=28)

    change_speed = ttk.Radiobutton(necessary1, text="拼接视频", value=2, variable=select,
                                   bootstyle="danger-outline-toolbutton", command=change_speed_click)
    change_speed.place(x=13, y=79, width=173, height=28)

    # ------------裁剪选项--------------
    necessary2 = ttk.Labelframe(frame, text="  裁剪开始/结束时间  ", width=165, height=135, bootstyle="danger")
    necessary2.place(x=220, y=100)

    # 开始时间
    time_from_label = ttk.Label(necessary2, text='从这里开始裁剪')
    time_from_label.place(x=13, y=0, width=140, height=28)
    time_from_entry = ttk.Entry(necessary2)
    time_from_entry.place(x=13, y=28, width=140, height=28)
    # 结束时间
    time_to_label = ttk.Label(necessary2, text='到这里结束')
    time_to_label.place(x=13, y=56, width=140, height=28)
    time_to_entry = ttk.Entry(necessary2)
    time_to_entry.place(x=13, y=84, width=140, height=28)

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
        print(files)
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


# ffmpeg
def use_ffmpeg(fout, ffset):
    print("using ffmpeg")
    ffmpeg = FFmpeg().option('y').output(fout, ffset)

    @ffmpeg.on('start')
    def on_start(arguments):
        print('Arguments:', arguments)

    i = 0

    @ffmpeg.on('stderr')
    def on_stderr(line):
        global i
        global terminal_text
        global terminal_lines
        if re.search(r'\sDuration: (?P<duration>\S+)', line):
            second = re.search(r'\sDuration: (?P<duration>\S+)', line).groupdict()['duration']
            i = time2seconds(second.split(",")[0])
            # sec
            print(time2seconds(second.split(",")[0]))
        linen = line + "\n"
        if terminal_lines > 4:
            terminal_lines = 1
            scroll_terminal.delete(1.0, ttk.END)
            scroll_terminal.insert(1.0, linen)
        else:
            terminal_lines += 1
            scroll_terminal.insert(1.0, linen)

    @ffmpeg.on('progress')
    def on_progress(progress):
        global i
        global scroll_terminal
        bfz = (time2seconds(progress.time) / i * 100)
        b1.configure(value=round(bfz))
        print(bfz, "%")

    @ffmpeg.on('start')
    def on_start(arguments):
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "压制中，请稍后……")

    @ffmpeg.on('completed')
    def on_completed():
        print('压制成功')
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "压制成功！")

    @ffmpeg.on('error')
    def on_error(code):
        scroll_terminal.delete(1.0, ttk.END)
        scroll_terminal.insert(1.0, code)
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "出现了神奇的错误")

    asyncio.run(ffmpeg.execute())


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
