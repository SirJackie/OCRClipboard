from OCRDetector import OCRDetector
from OCRVisualizer import OCRVisualizer
from SubprocessHelper import Subprocess
import time


def UIOCRSide(pipe_conn):
    # Get Image Path from Pipe
    img_path = None
    while True:
        if pipe_conn.poll():
            img_path = pipe_conn.recv()
            break

    # OCR Detect
    ocrDetector = OCRDetector()
    result = ocrDetector.Detect(img_path)

    # OCR Visualize
    ocrVisualizer = OCRVisualizer(result, img_path)
    # ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()

    pipe_conn.send("Success")


if __name__ == "__main__":

    uiOCRSide = Subprocess(UIOCRSide)
    uiOCRSide.Send("./Images/师兄啊师兄优酷目录.png")

    while True:
        if uiOCRSide.parent_conn.poll():
            message = uiOCRSide.parent_conn.recv()
            assert message == "Success"
            break

    while True:
        print("Loop")
        time.sleep(0.1)
