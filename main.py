from ClipboardOCR import OCRDetector, OCRVisualizer
from ClipboardUI import ClipboardUI
import time


def MyExternalCallback(string):
    clpUi.Send(string)


if __name__ == "__main__":
    global clpUI

    # UI
    clpUi = ClipboardUI()
    clpUi.Send("<鼠标拖动，框选要识别的文字>")
    time.sleep(0.1)  # Wait for UI Process to Create Window.

    # Image Path
    img_path = "./Images/师兄啊师兄优酷目录.jpg"

    # Detect
    ocrDetector = OCRDetector()
    result, img_resized = ocrDetector.Detect(img_path)

    # Visualize
    ocrVisualizer = OCRVisualizer(result, img_resized)
    ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()
