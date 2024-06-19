from ClipboardOCR import OCRDetector, OCRVisualizer
from ClipboardUI import ClipboardUI
from ImageHelper import *
import time


def MyExternalCallback(string):
    clpUi.Send(string)


if __name__ == "__main__":
    global clpUI

    # UI
    clpUi = ClipboardUI()
    clpUi.Send("<鼠标拖动，框选要识别的文字>")
    time.sleep(0.1)  # Wait for UI Process to Create Window.

    # Image
    img_path = "./Images/师兄啊师兄优酷目录.png"
    img_resized_path = ResizeImage(img_path, 1920)

    # Detect
    ocrDetector = OCRDetector()
    result = ocrDetector.Detect(img_resized_path)

    # Visualize
    ocrVisualizer = OCRVisualizer(result, img_resized_path)
    ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()
