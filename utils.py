import os


class File:
    def __init__(self, filename):
        self.name = filename
        self.is_hidden = False
        self.extension = None
        self.is_folder = False
        if self.filename is not None:
            for data in self.filename.split("/"):
                if data.startswith("."):
                    self.is_hidden = True
                    break
            ext = os.path.splitext(self.filename)[-1].lower()
            self.extension = ext if ext is not None and ext != "" else "no"
        self.is_code_file = True if ext == ".py" else False
        self.ignore = True if ("readme" in self.filename) or ("requirement" in self.filename) or ("setup" in self.filename) else False


class Folder:
    def __init__(self, filename):
        self.filename = filename
        self.is_hidden = False
        self.extension = None
        self.is_folder = False
        if self.filename is not None:
            for data in self.filename.split("/"):
                if data.startswith("."):
                    self.is_hidden = True
                    break
            ext = os.path.splitext(self.filename)[-1].lower()
            self.extension = ext if ext is not None and ext != "" else "no"
        self.is_code_file = True if ext == ".py" else False
        self.ignore = True if ("readme" in self.filename) or ("requirement" in self.filename) or (
                    "setup" in self.filename) else False
