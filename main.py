from PIL import Image
from paddleocr import PaddleOCR
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import RectangleSelector

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
ocr = PaddleOCR(det_model_dir=det_model_path, det_params_path=det_params_path,
                rec_model_dir=rec_model_path, rec_params_path=rec_params_path,
                cls_model_dir=cls_model_path, cls_params_path=cls_params_path)

# 要识别的图像文件路径
img_path = "./Images/01/IMG_20240517_094904.jpg"

# 打开图像并调整分辨率
img = Image.open(img_path)
width, height = img.size
new_width = 1920
new_height = int(height * (new_width / width))
img_resized = img.resize((new_width, new_height))  # 保持宽高比例调整分辨率

# 保存调整后的图像
resized_img_path = "./Temp/resized_image.jpg"
img_resized.save(resized_img_path)

# 进行文字检测和识别
result = ocr.ocr(resized_img_path, cls=True)

# 输出识别结果并准备绘制数据
boxes = []
texts = []
print("------------------------------")
for line in result[0]:
    coordinate = line[0]
    text = line[1]
    print(coordinate, text)
    boxes.append(coordinate)
    texts.append(text[0])  # 只取识别的文本内容，不包括置信度

# 使用 matplotlib 绘制识别结果
fig, ax = plt.subplots(1, figsize=(12, 12))
ax.imshow(img_resized)

# 绘制检测框
patches_list = []
for box in boxes:
    polygon = patches.Polygon(box, closed=True, edgecolor='red', linewidth=2, fill=False)
    patches_list.append(polygon)
    ax.add_patch(polygon)

selected_texts = []


def on_select(eclick, erelease):
    """ 鼠标框选回调函数 """
    global selected_texts
    selected_texts.clear()
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    for i, box in enumerate(boxes):
        # 检查检测框的四个顶点是否在选择区域内
        in_selection = any(
            (min(x1, x2) <= point[0] <= max(x1, x2) and min(y1, y2) <= point[1] <= max(y1, y2)) for point in box)
        if in_selection:
            selected_texts.append(texts[i])

    print("Selected texts:")
    for text in selected_texts:
        print(text)


# 创建一个矩形选择器
toggle_selector = RectangleSelector(ax, on_select, useblit=True,
                                    button=[1], minspanx=5, minspany=5, spancoords='data',
                                    interactive=True)

plt.axis('off')
plt.show()
