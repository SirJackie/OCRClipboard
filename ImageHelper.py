from PIL import Image
from PathHelper import *


def LoadImage(img_path):
    # 打开图像并调整分辨率
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    return img


def ResizeImage(img_path, new_width=1920):
    workingDir = WorkingDir(img_path)
    original_img_file_name = workingDir.file_name

    # 打开图像并调整分辨率
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    width, height = img.size

    new_height = int(height * (new_width / width))
    img_resized = img.resize((new_width, new_height))  # 保持宽高比例调整分辨率

    # 保存调整后的图像
    tempDir = TempDir()
    resized_img_path = tempDir.At(original_img_file_name, ".jpg")
    img_resized.save(resized_img_path)

    return resized_img_path
