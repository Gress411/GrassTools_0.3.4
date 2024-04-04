import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap import Style
import ttkbootstrap.scrolled as ttks


def sys(frame):
    text = ttk.Label(frame, text="很多功能还没做好，这里是一些功能介绍\n"
                                 "那些长得像按钮的东西确实是按钮，点击会跳出一些提示\n"
                                 "把想要操作的视频拖进来就可以操作了，开始按钮是底下那个大的\n"
                                 "目前还不支持批量压制\n"
                                 "请不要单独解压，把ffmpeg也解压出来，和软件放同一目录下\n"
                                 "最初设计这个软件的目的就是把图片序列变成视频，好方便一下我自己\n"
                                 "注：\n"
                                 "序列面板中需要把所有图片都拖进来，而且只能拖图片进来\n"
                                 "这个软件的意义不大，但如果我闲得慌说不定会继续写\n"
                                 "目前已经可以使用的面板是 压缩视频，帧数转换和序列\n"
                                 "序列目前仅支持英文路径和文件名\n"
                                 "2022_3_3")
    text.pack()
