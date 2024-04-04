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

b0 = ttk.Floodgauge

terminal_text = ""
files = []
default_set = {"pix_fmt": "yuv420p", "vcodec": "libx264", "preset": "medium",
               "crf": "23"}
newSet = {"pix_fmt": "yuv420p", "vcodec": "libx264", "preset": "medium",
          "crf": "23"}
scroll_terminal = ttks.ScrolledText

terminal_lines = 0

# new_name_entry = ttk.Entry
# new_accuracy_combobox = ttk.Combobox
# new_ext_entry = ttk.Entry

newName = ""
newCode = ""
nCrf = 23

scroll_renhua = ttks.ScrolledText


def cv(frame):
    global b0
    global terminal_text
    global scroll_terminal
    global scroll_renhua

    # 开始按钮
    def start_thr(fin, fout, fset):
        use_ffmpeg(fin, fout, fset)

    # 逻辑核心-----------------------------------------------------------
    def click(e):
        global newName
        global newCode
        global nCrf
        global newSet

        # 获取参数
        try:
            del [newSet['stop']]
        except:
            pass
        newSet['crf'] = meter1.amountusedvar.get()
        if newSet['crf'] >= 40:
            Q1 = tkinter.messagebox.askyesno(title='警告', message='你的crf值有点太高了\n这可能导致视频糊成屎\n是否继续')
            if Q1:
                print('yes')
            else:
                newSet['stop'] = "stop"
        elif newSet['crf'] < 15:
            Q2 = tkinter.messagebox.askyesno(title='警告', message='你的crf值有点太低了\n这可能导致视频非常大\n是否继续')
            if Q2:
                print('yes')
            else:
                newSet['stop'] = "stop"
        newSet['preset'] = new_accuracy_combobox.get()
        nowCode = new_ext_entry.get()
        if nowCode == 'h.265':
            newSet['vcodec'] = "hevc"
        else:
            newSet['vcodec'] = "libx264"

        print(newSet['vcodec'])
        # 获取新名字
        newName = new_name_entry.get()
        # 获取扩展名
        newCode = new_ext_entry.get()
        exportUrl = "error"
        try:
            exportUrl = os.path.dirname(files[0]) + "\\" + newName + ".mp4"
        except:
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "访问文件时出现问题，你把视频拖进来了吗?")
            return
        print(exportUrl)
        # 懒得改了，不触发就不触发吧
        # os.path.basename(files[0])
        # if os.path.basename(files[0]).find('.') != -1:
        #     exportUrl = os.path.dirname(files[0]) + newName
        # else:
        #     exportUrl = os.path.dirname(files[0]) + newName + ".mp4"

        # 也许可以从这里开始写批量压制
        try:
            if (os.path.splitext(files[0])[-1] == '.jpg') | (os.path.splitext(files[0])[-1] == '.png'):
                t2 = threading.Thread(target=start_thr, args=(extract_dir(files[0]), exportUrl, newSet))
                t2.start()
            else:
                t2 = threading.Thread(target=start_thr, args=(files[0], exportUrl, newSet))
                t2.start()
        except:
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "你看看是不是有啥参数没写")
            return

    b0 = ttk.Floodgauge(frame, cursor='rtl_logo', mask="当前进度{}%", font=("微软雅黑", 12))
    b0.bind("<Button>", click)
    b0.pack(fill=ttk.X, side=ttk.BOTTOM)

    # 文件列表框
    # state = 'disable' normal
    scroll_files = ttks.ScrolledText(frame, autohide=False, padding=12)
    scroll_files.insert(ttk.END, '把视频拖进来吧')
    # print(scroll_files.get('1.0', 'end-1c'))
    scroll_files.place(width=400, height=90, x=-2, y=10)

    # 必填项
    necessary1 = ttk.Labelframe(frame, text="  输出设置  ", width=200, height=135, bootstyle="danger")
    necessary1.place(x=10, y=100)

    # new_name = ttk.Label(necessary1, text="新文件名", font="微软雅黑 10")
    # new_name.place(x=7, y=6)
    # new_accuracy = ttk.Label(necessary1, text="压制精度", font="微软雅黑 10")
    # new_accuracy.place(x=7, y=42)
    # new_ext = ttk.Label(necessary1, text="批量后缀", font="微软雅黑 10")
    # new_ext.place(x=7, y=79)

    def new_name_click_threading():
        tkinter.messagebox.showinfo('帮助', '给压制后的视频起个名字吧!\n顺便，右边的表盘是crf值，值越小画质越好')

    def new_name_click():
        t = threading.Thread(target=new_name_click_threading)
        t.start()

    def new_accuracy_click_threading():
        tkinter.messagebox.showinfo('帮助', '精度共有10挡，建议用medium\n这个参数对压制速度的影响很大\n当然，不差时间的话可以考虑veryslow')

    def new_accuracy_click():
        t = threading.Thread(target=new_accuracy_click_threading)
        t.start()

    def new_ext_click_threading():
        tkinter.messagebox.showwarning('注意', '这里是编码选项\nh.265更先进，但并非所有设备和平台都支持,而且编码较慢\n(本软件目前仅支持输出.mp4封装格式)')

    def new_ext_click():
        t = threading.Thread(target=new_ext_click_threading)
        t.start()

    new_name = ttk.Button(necessary1, text="名称", command=new_name_click)
    new_name.place(x=13, y=6, width=50, height=28)
    new_accuracy = ttk.Button(necessary1, text="精度", command=new_accuracy_click)
    new_accuracy.place(x=13, y=42, width=50, height=28)
    new_ext = ttk.Button(necessary1, text="编码", command=new_ext_click)
    new_ext.place(x=13, y=79, width=50, height=28)
    # 输入框
    new_name_entry = ttk.Entry(necessary1)
    new_name_entry.insert('end', '输出文件名')

    def click_del_name_entry(e):
        if new_name_entry.get() == '输出文件名':
            new_name_entry.delete(0, ttk.END)

    new_name_entry.bind("<Button>", click_del_name_entry)
    new_name_entry.pack()
    # 精度选项
    new_name_entry.place(x=63, y=6, width=120, height=28)
    new_accuracy_combobox = ttk.Combobox(necessary1, state='readonly')  # 精度选项
    new_accuracy_combobox['value'] = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow',
                                      'slower', 'veryslow', 'placebo']
    new_accuracy_combobox.current(5)
    new_accuracy_combobox.place(x=63, y=42, width=120, height=28)
    # 编码选项
    # new_ext_entry = ttk.Entry(necessary1)
    # new_ext_entry.insert('end', 'h264')
    new_ext_entry = ttk.Combobox(necessary1, state='readonly')  # 精度选项
    new_ext_entry['value'] = ['h.264', 'h.265']
    new_ext_entry.current(0)
    new_ext_entry.place(x=63, y=42, width=120, height=28)

    def click_del_ext_entry(e):
        if new_ext_entry.get() == 'mp4':
            new_ext_entry.delete(0, ttk.END)

    new_ext_entry.bind("<Button>", click_del_ext_entry)
    new_ext_entry.place(x=63, y=79, width=120, height=28)
    # 仪表盘
    meter1 = ttk.Meter(
        frame,
        metersize=140,
        amountused=23,
        amounttotal=51,
        metertype="semi",
        subtext="建议值23",
        interactive=True,
    )
    meter1.place(x=230, y=110)

    # 控制台输出
    scroll_terminal = ttks.ScrolledText(frame, autohide=True, padding=12)
    scroll_terminal.insert(ttk.END, terminal_text)
    # print(scroll_terminal.get('1.0', 'end-1c'))
    # scroll_terminal.delete(1.0, ttk.END)
    # scroll_terminal.insert(ttk.END, "test!")
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


# ffmpeg
def use_ffmpeg(fin, fout, ffset):
    print("using ffmpeg")
    ffmpeg = FFmpeg().option('y').input(fin).output(fout, ffset)

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
        b0.configure(value=round(bfz))
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


def extract(strs):
    nums = 0
    for i in reversed(strs):
        if i.isdigit():
            nums += 1
        else:
            break
    return strs[:-nums] + '%0' + str(nums) + 'd'


def extract_dir(strs):
    return os.path.dirname(strs) + '\\' + extract(os.path.splitext(os.path.basename(strs))[0]) + os.path.splitext(strs)[
        -1]


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
