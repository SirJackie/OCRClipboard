import tkinter as tk
import ctypes

# 启用高DPI支持
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print(f"Failed to set DPI awareness: {e}")

# 创建主窗口
root = tk.Tk()

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

# 启动主循环
root.mainloop()
