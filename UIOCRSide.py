from OCRDetector import OCRDetector
from OCRVisualizer import OCRVisualizer
from SubprocessHelper import Subprocess
import time
import json


def UIOCRSide(pipe_conn):
    # Get OCR Result from Pipe
    ocr_result = None
    while True:
        if pipe_conn.poll():
            ocr_result = pipe_conn.recv()
            break

    # Get Image Path from Pipe
    img_path = None
    while True:
        if pipe_conn.poll():
            img_path = pipe_conn.recv()
            break

    # Read JSON
    ocr_result = json.loads(ocr_result)

    # OCR Visualize
    ocrVisualizer = OCRVisualizer(ocr_result, img_path)
    # ocrVisualizer.BindExternalCallback(MyExternalCallback)
    ocrVisualizer.Visualize()


if __name__ == "__main__":

    # Image
    img_path = "./Images/师兄啊师兄优酷目录.png"

    # OCR Detect
    ocrDetector = OCRDetector()
    ocr_result = ocrDetector.Detect(img_path)

    # OCR Visualize
    uiOCRSide = Subprocess(UIOCRSide)
    uiOCRSide.Send(json.dumps(ocr_result))
    uiOCRSide.Send(img_path)

    while True:
        print("Loop")
        time.sleep(0.1)
