from SubprocessHelper import Subprocess
import json
import time
import os

# CONSTANT DEFINITIONS
DO_IMAGE_RESIZING = False
IMAGE_RESIZING_WIDTH = 1920


if __name__ == "__main__":

    os.system("chcp 65001")
    os.system("cls")

    # Greeting
    print("------------------------------")
    print("OCRClipboard by SirJackie")
    print("一款好用简单的光学文字识别工具，基于PaddleOCR开发。")
    print("GitHub: https://github.com/SirJackie")
    print("------------------------------")

    # Image
    img_path = input("要识别的图片，拖进来：")

    # Lazy Loading, Ensure the Minimal Memory Occupation when fork()
    from UIMainWindow import UIMainWindow

    # Create Main Window First
    uiMainWindow = Subprocess(UIMainWindow)

    # Lazy Loading, Ensure the Minimal Memory Occupation when fork()
    from UIClipSide import UIClipSide

    # UI Clip Side
    uiClipSide = Subprocess(UIClipSide)
    uiClipSide.Send("<鼠标拖动，框选要识别的文字>")

    # Lazy Loading, Ensure the Minimal Memory Occupation when fork()
    from OCRDetector import OCRDetector
    from UIOCRSide import UIOCRSide

    # OCR Detect
    ocrDetector = OCRDetector()
    ocr_result = ocrDetector.Detect(img_path)

    # UI OCR Side
    uiOCRSide = Subprocess(UIOCRSide)
    uiOCRSide.Send(json.dumps(ocr_result))
    uiOCRSide.Send(img_path)

    while True:
        if uiMainWindow.CanRecv():
            message = uiMainWindow.Recv()
            if message == "Close":
                break
        elif uiOCRSide.CanRecv():
            str = uiOCRSide.Recv()  # Not Async, It's Synced.
            uiClipSide.Send(str)
        else:
            time.sleep(0.01)
