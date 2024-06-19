from SubprocessHelper import Subprocess
import json

# CONSTANT DEFINITIONS
DO_IMAGE_RESIZING = False
IMAGE_RESIZING_WIDTH = 1920


if __name__ == "__main__":

    # Image
    img_path = "./Images/师兄啊师兄优酷目录.png"

    # # Lazy Loading, Ensure the Minimal Memory Occupation when fork()
    # from UIMainWindow import UIMainWindow
    #
    # # Create Main Window First
    # uiMainWindow = Subprocess(UIMainWindow)

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
        str = uiOCRSide.Recv()  # Not Async, It's Synced.
        uiClipSide.Send(str)
