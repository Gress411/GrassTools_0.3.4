import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Style
import ttkbootstrap.scrolled as ttks
import threading
import windnd
import os

import cv2

pic_size = (1920, 1080)
files = []

b0 = ttk.Floodgauge
terminal_text = ""
scroll_terminal = ttks.ScrolledText
terminal_lines = 0
newName = ""
scroll_renhua = ttks.ScrolledText


def mp(frame):
    global b0
    global terminal_text
    global scroll_terminal
    global scroll_renhua

    # 开始按钮
    def start_thr(fin, fout, fset):
        pass

    # 逻辑核心-----------------------------------------------------------
    def click(e):
        global newName
        global pic_size
        global files

        pic_size = (int(new_s_width_entry.get()), int(new_s_height_entry.get()))

        newName = new_name_entry.get()
        try:
            exportUrl = os.path.dirname(files[0]) + "\\" + newName + ".mp4"
        except:
            scroll_renhua.delete(1.0, ttk.END)
            scroll_renhua.insert(1.0, "访问文件时出现问题，你把视频拖进来了吗?帧数改了吗?")
            return
        print(exportUrl)

        t2 = threading.Thread(target=use_cv2, args=((1920, 1080), exportUrl, new_frames.get()))
        t2.start()

    b0 = ttk.Floodgauge(frame, cursor='rtl_logo', mask="当前进度{}%", font=("微软雅黑", 12))
    b0.bind("<Button>", click)
    b0.pack(fill=ttk.X, side=ttk.BOTTOM)

    # 文件列表框
    # state = 'disable' normal
    scroll_files = ttks.ScrolledText(frame, autohide=False, padding=12)
    scroll_files.insert(ttk.END, '把图片全拖进来吧,注意,序列目前仅支持英文路径和文件名')
    # print(scroll_files.get('1.0', 'end-1c'))
    scroll_files.place(width=400, height=90, x=-2, y=10)

    # 必填项
    necessary1 = ttk.Labelframe(frame, text="  输出设置  ", width=200, height=135, bootstyle="danger")
    necessary1.place(x=10, y=100)

    def new_name_click():
        messagebox_thr('帮助', '给处理后的视频起个名字吧!', 'info')

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

    # 分辨率选择
    def new_s_click():
        messagebox_thr('帮助', '请手动把图片序列的分辨率填写在下面\n你问我为什么不识别？因为我懒啊！', 'info')

    new_s = ttk.Button(necessary1, text="在下方填写视频分辨率", command=new_s_click)
    new_s.place(x=13, y=42, width=173, height=28)

    # 宽
    new_s_width_button = ttk.Button(necessary1, text="宽", command=new_s_click)
    new_s_width_button.place(x=13, y=79, width=40, height=28)

    def click_s_width_entry(e):
        if new_s_width_entry.get() == '1920':
            new_s_width_entry.delete(0, ttk.END)

    new_s_width_entry = ttk.Entry(necessary1)
    new_s_width_entry.insert('end', '1920')
    new_s_width_entry.bind("<Button>", click_s_width_entry)
    new_s_width_entry.place(x=53, y=79, width=50, height=28)
    # 高
    new_s_width_button = ttk.Button(necessary1, text="高", command=new_s_click)
    new_s_width_button.place(x=103, y=79, width=40, height=28)

    def click_s_height_entry(e):
        if new_s_height_entry.get() == '1080':
            new_s_height_entry.delete(0, ttk.END)

    new_s_height_entry = ttk.Entry(necessary1)
    new_s_height_entry.insert('end', '1080')
    new_s_height_entry.bind("<Button>", click_s_height_entry)
    new_s_height_entry.place(x=143, y=79, width=50, height=28)

    # 帧数选择
    necessary2 = ttk.Labelframe(frame, text="  目标帧数  ", width=165, height=135, bootstyle="danger")
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
    select_code['value'] = ['弃用', '弃用']
    select_code.current(0)
    select_code.place(x=63, y=79, width=90, height=28)

    def new_name_click():
        messagebox_thr('帮助', '只是为了好看', 'info')

    select_code_button = ttk.Button(necessary2, text="编码", command=new_name_click)
    select_code_button.place(x=13, y=79, width=50, height=28)

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


def use_cv2(size, exp_url, fps):
    global pic_size
    pic_size = size
    img_array = []

    new_video = cv2.VideoWriter(exp_url, -1, int(fps), pic_size)
    for filename in files:
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)
    for i in range(len(files)):
        new_video.write(img_array[i])
    print('end!')
