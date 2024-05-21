from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import os

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

# 输出识别结果
boxes = []
print("------------------------------")
for line in result[0]:
    coordinate = line[0]
    text = line[1]
    print(coordinate, text)
    boxes.append(coordinate)

# 将识别结果绘制在图片上并显示
image_drawn = draw_ocr(img_resized, boxes)

# 转换为 PIL 图像对象并显示
image_pil = Image.fromarray(image_drawn)
image_pil.show()
