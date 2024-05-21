from PIL import Image
from paddleocr import PaddleOCR
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as font_man

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

# 设置自定义字体路径
custom_font_path = '.\\ChineseSupport\\SourceHanSans_Normal.ttf'

# 定义自定义字体对象
custom_font = font_man.FontProperties(fname=custom_font_path)

# 绘制检测框和文本
for i, box in enumerate(boxes):
    # 创建一个多边形对象
    polygon = patches.Polygon(box, closed=True, edgecolor='red', linewidth=2, fill=False)
    ax.add_patch(polygon)

plt.axis('off')
plt.show()
