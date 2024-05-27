from PIL import Image
from paddleocr import PaddleOCR
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import RectangleSelector
import tempfile


class OCRDetector:
    def __init__(self):
        # 获取当前脚本所在目录的路径
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置模型文件的相对路径
        det_model_path = os.path.join(script_dir, 'Models', 'det_model')
        det_params_path = os.path.join(script_dir, 'Models', 'det_params')
        rec_model_path = os.path.join(script_dir, 'Models', 'rec_model')
        rec_params_path = os.path.join(script_dir, 'Models', 'rec_params')
        cls_model_path = os.path.join(script_dir, 'Models', 'cls_model')
        cls_params_path = os.path.join(script_dir, 'Models', 'cls_params')

        # 初始化 PaddleOCR
        # det、rec、cls 分别代表检测（detection）、识别（recognition）、分类（classification）
        self.ocr = PaddleOCR(det_model_dir=det_model_path, det_params_path=det_params_path,
                             rec_model_dir=rec_model_path, rec_params_path=rec_params_path,
                             cls_model_dir=cls_model_path, cls_params_path=cls_params_path)

    def Detect(self, img_path):
        # 打开图像并调整分辨率
        img = Image.open(img_path)
        width, height = img.size
        new_width = 1920
        new_height = int(height * (new_width / width))
        img_resized = img.resize((new_width, new_height))  # 保持宽高比例调整分辨率

        # 保存调整后的图像
        resized_img_path = os.path.join(tempfile.gettempdir(), "resized_image.jpg")
        img_resized.save(resized_img_path)

        # Do OCR Detection
        result_array = self.ocr.ocr(resized_img_path, cls=True)
        assert len(result_array) == 1

        # 进行文字检测和识别
        return result_array[0], img_resized


class OCRVisualizer:
    def __init__(self, result, img_resized):
        self.selected_texts = None
        self.patches_list = None
        self.mergeStr = None
        self.externalCallback = None

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
        ax.imshow(img_resized)

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


def MyExternalCallback(string):
    print(string)


if __name__ == "__main__":
    img_path = "./Images/01/IMG_20240517_094904.jpg"

    # Detect
    ocrDetector = OCRDetector()
    result, img_resized = ocrDetector.Detect(img_path)

    # Visualize
    ocrVisualizer = OCRVisualizer(result, img_resized)
    ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()
