import tkinter as tk
from ctypes import windll
import win32gui
import win32con
import pygetwindow as gw

# 启用高DPI支持
windll.shcore.SetProcessDpiAwareness(1)


# 获取窗口句柄
def get_window_handle(title):
    window = gw.getWindowsWithTitle(title)
    if window:
        return window[0]._hWnd
    else:
        raise Exception(f"Window with title '{title}' not found")


# 嵌入窗口
def embed_window(parent, hwnd, x, y, width, height):
    win32gui.SetParent(hwnd, parent)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & ~win32con.WS_CAPTION & ~win32con.WS_THICKFRAME)
    win32gui.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED)


# 主程序
def main():
    root = tk.Tk()
    root.title("主窗口")
    # root.geometry("800x600")  # 设置主窗口初始大小

    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置窗口宽高分别占屏幕的 80%
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    # 计算窗口的位置，使其居中
    position_right = int((screen_width - window_width) / 2)
    position_down = int(((screen_height - window_height) * 0.55) / 2)

    # 设置窗口大小和位置
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    # 获取两个子窗口的句柄（替换成你实际窗口的标题）
    hwnd1 = get_window_handle("Figure 1")
    hwnd2 = get_window_handle("Text Display")

    root.update_idletasks()  # 更新主窗口尺寸信息

    # 嵌入子窗口
    embed_window(root.winfo_id(), hwnd1, 0, 0, root.winfo_width() // 2, root.winfo_height())
    embed_window(root.winfo_id(), hwnd2, root.winfo_width() // 2, 0, root.winfo_width() // 2, root.winfo_height())

    # 将焦点设置回主窗口
    win32gui.SetForegroundWindow(root.winfo_id())

    # 当主窗口尺寸改变时调整子窗口大小
    def on_resize(event):
        pass
        embed_window(root.winfo_id(), hwnd1, 0, 0, root.winfo_width() // 2, root.winfo_height())
        # embed_window(root.winfo_id(), hwnd2, root.winfo_width() // 2, 0, root.winfo_width() // 2, root.winfo_height())
        # # 将焦点设置回主窗口
        # win32gui.SetForegroundWindow(root.winfo_id())

    root.bind("<Configure>", on_resize)

    root.mainloop()


if __name__ == "__main__":
    main()
