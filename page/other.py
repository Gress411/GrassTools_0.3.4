import ttkbootstrap as ttk
import ttkbootstrap.scrolled as ttks

import page.others.audio as audio


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


def other(frame):
    tab = ttk.Notebook(frame)

    F1 = ttk.Frame(tab, borderwidth=1, border=0)
    audio.audio(F1)
    tab.add(F1, text="音频处理")

    F1 = ttk.Frame(tab, borderwidth=1, border=0)
    tab.add(F1, text="镜像")

    F1 = ttk.Frame(tab, borderwidth=1, border=0)
    tab.add(F1, text="水印")

    tab.pack(expand=True, fill=ttk.BOTH)