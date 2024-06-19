from OCRDetector import OCRDetector
from OCRVisualizer import OCRVisualizer
from UIClipSide import ClipboardUI
from ImageHelper import *
import time

# CONSTANT DEFINITIONS
DO_IMAGE_RESIZING = False
IMAGE_RESIZING_WIDTH = 1920


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
    if DO_IMAGE_RESIZING:
        img_path = ResizeImage(img_path, IMAGE_RESIZING_WIDTH)

    # Detect
    ocrDetector = OCRDetector()
    result = ocrDetector.Detect(img_path)

    # Visualize
    ocrVisualizer = OCRVisualizer(result, img_path)
    ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()
