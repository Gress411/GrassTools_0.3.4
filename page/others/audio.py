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

b1 = ttk.Floodgauge
terminal_text = ""

scroll_terminal = ttks.ScrolledText
terminal_lines = 0
scroll_renhua = ttks.ScrolledText


def audio(frame):
    # 开始按钮1
    def start_thr(fout, fset):
        use_ffmpeg(fout, fset)

    # 逻辑核心-----------------------------------------------------------
    def click(e):
        if select.get() == 1:
            print(1)

    b1 = ttk.Floodgauge(frame, cursor='rtl_logo', mask="当前进度{}%", font=("微软雅黑", 12))
    b1.bind("<Button>", click)
    b1.pack(fill=ttk.X, side=ttk.BOTTOM)

    # 文件列表框
    # state = 'disable' normal
    scroll_files = ttks.ScrolledText(frame, autohide=False, padding=12)
    scroll_files.insert(ttk.END, '把文件拖进来吧')
    # print(scroll_files.get('1.0', 'end-1c'))
    scroll_files.place(width=400, height=90, x=-2, y=-10)

    # 必填项
    necessary1 = ttk.Labelframe(frame, text="  功能选择  ", width=375, height=135, bootstyle="danger")
    necessary1.place(x=10, y=75)

    def new_name_click():
        messagebox_thr('帮助',
                       '给处理后的文件起个名字吧!\n提取视频和音频就是字面意思，会直接删除音/视频轨道\n合并音视频可以导入多条音轨，但音轨会被合并\n音画不同步调节实际上是改变音频的位置，单位为毫秒，值可以为负',
                       'info')

    def yanchi_text_click():
        messagebox_thr('帮助',
                       '这是专为第四个功能制作的输入框\n单位是毫秒，可以为负数',
                       'info')

    new_name = ttk.Button(necessary1, text="名称", command=new_name_click)
    new_name.place(x=13, y=6, width=50, height=28)
    # 输入框
    new_name_entry = ttk.Entry(necessary1)
    new_name_entry.insert('end', '输出文件名')

    def click_del_name_entry(e):
        if new_name_entry.get() == '输出文件名':
            new_name_entry.delete(0, ttk.END)

    new_name_entry.bind("<Button>", click_del_name_entry)
    new_name_entry.place(x=63, y=6, width=120, height=28)

    # 延迟选择
    yanchi_text = ttk.Button(necessary1, text="延迟:", command=yanchi_text_click)
    yanchi_text.place(x=188, y=6, width=50, height=28)

    # 延迟输入框
    yanchi_entry = ttk.Entry(necessary1)
    yanchi_entry.insert('end', '请输入延迟(数字)')

    def click_yanchi_entry(e):
        if yanchi_entry.get() == '请输入延迟(数字)':
            yanchi_entry.delete(0, ttk.END)

    yanchi_entry.bind("<Button>", click_yanchi_entry)
    yanchi_entry.place(x=238, y=6, width=120, height=28)

    # 模式选择
    select = ttk.IntVar()
    select.set(1)

    # 选择选项后的提示----------------------------------
    def ext_Video_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“提取视频”，这不需要重新编码\n注意，提取后的视频并非静音，而是没有音轨")

    def ext_Audio_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“提取音频”，这也不需要重新编码\n注意，提取后的音频没有视频(废话)")

    def mix_AV_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“合并视频”，这也不需要重新编码\n可以导入多条音频，但是最终音频会被合并为一条\n注意，请确保音视频是可以对上的")

    def synchro_click():
        scroll_renhua.delete(1.0, ttk.END)
        scroll_renhua.insert(1.0, "你选择了“提取音频”，这也不需要重新编码\n注意，提取后的音频没有视频(废话)")

    ext_Video = ttk.Radiobutton(necessary1, text="提取视频", value=1, variable=select,
                                bootstyle="outline-toolbutton", command=ext_Video_click)

    ext_Video.place(x=13, y=42, width=170, height=28)

    ext_Audio = ttk.Radiobutton(necessary1, text="提取音频", value=2, variable=select,
                                bootstyle="outline-toolbutton", command=ext_Audio_click)
    ext_Audio.place(x=13, y=79, width=170, height=28)

    mix_AV = ttk.Radiobutton(necessary1, text="合并音视频", value=3, variable=select,
                             bootstyle="danger-outline-toolbutton", command=mix_AV_click)

    mix_AV.place(x=188, y=42, width=170, height=28)

    synchro = ttk.Radiobutton(necessary1, text="处理音画不同步", value=4, variable=select,
                              bootstyle="danger-outline-toolbutton", command=synchro_click)
    synchro.place(x=188, y=79, width=170, height=28)

    # 控制台输出
    scroll_terminal = ttks.ScrolledText(frame, autohide=True, padding=12)
    scroll_terminal.insert(ttk.END, terminal_text)
    scroll_terminal.place(width=400, height=200, x=-2, y=210)

    # 人话输出
    scroll_renhua = ttks.ScrolledText(frame, autohide=True, padding=(12, 5, 12, 0), font="微软雅黑 100")
    scroll_renhua.insert(ttk.END, terminal_text)
    scroll_renhua.insert(1.0, "欢迎使用草工具箱 beta v0.4.0")
    scroll_renhua.place(width=400, height=75, x=-2, y=400)

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
