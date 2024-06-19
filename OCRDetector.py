from paddleocr import PaddleOCR
from ImageHelper import *


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
        # Do OCR Detection
        result_array = self.ocr.ocr(img_path, cls=True)
        assert len(result_array) == 1

        # 进行文字检测和识别
        return result_array[0]
