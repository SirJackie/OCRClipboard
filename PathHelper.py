import os
import tempfile


def DeQuoteIze(path):
    if path.startswith("\""):
        return path[1:-1]
    else:
        return path


def QuoteIze(path):
    if path.startswith("\""):
        return path
    else:
        return "\"" + path + "\""


class WorkingDir:
    def __init__(self, original_file_path):
        self.dir_name, file_full_name = os.path.split(original_file_path)
        self.file_name, self.file_extension = os.path.splitext(file_full_name)

    def At(self, file, extension):
        return os.path.join(self.dir_name, file + extension)


class TempDir:
    def __init__(self):
        self.dir_name = DeQuoteIze(tempfile.gettempdir())  # This result of the API comes with quotes.

    def At(self, file, extension):
        return os.path.join(self.dir_name, file + extension)


def DropFiles():
    input_string = input("拖动文件到此窗口即可，可以一次拖动多个文件进来：")
    input_list = []

    if input_string[0] == "\"":
        # Multiple "path" with quotes
        input_string = input_string.strip("\"")
        input_list = input_string.split('" "')
    else:
        # Multiple path with no quotes
        input_list = input_string.split(' ')

    return input_list
