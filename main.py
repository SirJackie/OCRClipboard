from OCRDetector import OCRDetector
from UIClipSide import UIClipSide
from UIOCRSide import UIOCRSide

from SubprocessHelper import Subprocess
from ImageHelper import *

import time
import json

# CONSTANT DEFINITIONS
DO_IMAGE_RESIZING = False
IMAGE_RESIZING_WIDTH = 1920


# def MyExternalCallback(string):
#     clpUi.Send(string)


if __name__ == "__main__":

    # Image
    img_path = "./Images/师兄啊师兄优酷目录.png"

    # OCR Detect
    ocrDetector = OCRDetector()
    ocr_result = ocrDetector.Detect(img_path)

    # UI OCR Side
    uiOCRSide = Subprocess(UIOCRSide)
    uiOCRSide.Send(json.dumps(ocr_result))
    uiOCRSide.Send(img_path)
    # time.sleep(0.5)

    # UI Clip Side
    uiClipSide = Subprocess(UIClipSide)
    uiClipSide.Send("Hello, World!")
    # time.sleep(0.5)

    while True:
        # myStr = input("请输入要发送的字符串：")
        myStr = "xxx"
        uiClipSide.Send(myStr)

        if myStr == "exit":
            break

















    # global clpUI
    #
    # # UI
    # clpUi = ClipboardUI()
    # clpUi.Send("<鼠标拖动，框选要识别的文字>")
    # time.sleep(0.1)  # Wait for UI Process to Create Window.
    #
    # # Image
    # img_path = "./Images/师兄啊师兄优酷目录.png"
    # if DO_IMAGE_RESIZING:
    #     img_path = ResizeImage(img_path, IMAGE_RESIZING_WIDTH)
    #
    # # Detect
    # ocrDetector = OCRDetector()
    # result = ocrDetector.Detect(img_path)
    #
    # # Visualize
    # ocrVisualizer = OCRVisualizer(result, img_path)
    # ocrVisualizer.BindExternalCallback(MyExternalCallback)
    # ocrVisualizer.Visualize()
