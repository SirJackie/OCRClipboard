import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import RectangleSelector
from HelperImage import *


class OCRVisualizer:
    def __init__(self, result, img_path):
        self.selected_texts = None
        self.patches_list = None
        self.mergeStr = None
        self.externalCallback = None
        self.img = LoadImage(img_path)

        # 输出识别结果
        self.boxes = []
        self.texts = []
        print("------------------------------")
        for line in result:
            coordinate = line[0]
            text = line[1]
            print(coordinate, text)
            self.boxes.append(coordinate)
            self.texts.append(text[0])  # 只取识别的文本内容，不包括置信度

    def Visualize(self):
        # 绘制数据
        fig, ax = plt.subplots(1, figsize=(12, 12))
        ax.imshow(self.img)

        # 绘制检测框
        self.patches_list = []
        for box in self.boxes:
            polygon = patches.Polygon(box, closed=True, edgecolor='red', linewidth=2, fill=False)
            self.patches_list.append(polygon)
            ax.add_patch(polygon)

        self.selected_texts = []

        # 创建一个矩形选择器
        toggle_selector = RectangleSelector(ax, self.OnSelectCallback, useblit=True,
                                            button=[1], minspanx=5, minspany=5, spancoords='data',
                                            interactive=True)

        plt.axis('off')
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.show()

    def BindExternalCallback(self, func):
        self.externalCallback = func

    def OnSelectCallback(self, eclick, erelease):
        self.selected_texts.clear()
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        for i, box in enumerate(self.boxes):
            # 检查检测框的四个顶点是否在选择区域内
            in_selection = any(
                (min(x1, x2) <= point[0] <= max(x1, x2) and min(y1, y2) <= point[1] <= max(y1, y2)) for point in box)
            if in_selection:
                self.selected_texts.append(self.texts[i])

        self.mergeStr = ""
        for text in self.selected_texts:
            self.mergeStr += text

        if self.externalCallback is not None:
            self.externalCallback(self.mergeStr)
