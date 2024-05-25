import multiprocessing
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tk_font
import time
import ctypes
import pyglet
import atexit


def GUIProcess(pipe_conn):
    # 设置DPI感知
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"SetProcessDpiAwareness failed: {e}")

    # 创建Tkinter窗口
    root = tk.Tk()
    root.title("Text Display")

    # 使用pyglet加载自定义字体
    pyglet.options['win32_gdi_font'] = True
    font_path = "./ChineseSupport/SourceHanSans_Normal.ttf"
    pyglet.font.add_file(str(font_path))

    # 创建字体对象
    font = tk_font.Font(family="Source Han Sans Normal", size=24)

    # 创建一个ScrolledText小部件来显示文本
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=font)
    text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def CheckForMessage():
        # 检查管道中是否有消息
        if pipe_conn.poll():
            message = pipe_conn.recv()
            text_area.delete(1.0, tk.END)  # 删除当前文本
            text_area.insert(tk.END, message + '\n')
            text_area.see(tk.END)
        # 设定100毫秒后再次检查
        root.after(100, CheckForMessage)

    CheckForMessage()
    root.mainloop()


class ClipboardUI:
    def __init__(self):
        # Create Pipe Connection
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

        # Create Sub-Process
        self.process = multiprocessing.Process(target=GUIProcess, args=(self.child_conn,))
        self.process.start()

        # Auto Destruction when Exit.
        atexit.register(self.Close)

    def Send(self, string):
        self.parent_conn.send(string)

    def Close(self):
        # Terminate Sub-Process
        self.process.terminate()
        self.process.join()
        print("Clipboard UI Sub-Process Terminated.")


if __name__ == '__main__':
    clpUi = ClipboardUI()
    clpUi.Send("Hello, World!")
    time.sleep(0.5)

    while True:
        myStr = input("请输入要发送的字符串：")
        clpUi.Send(myStr)

        if myStr == "exit":
            break
