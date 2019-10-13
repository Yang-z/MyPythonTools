import os


class TimestampHelper(object):

    @staticmethod
    def show(path):
        print("atime:", os.path.getatime(path))
        print("mtime:", os.path.getmtime(path))

    @staticmethod
    def copy(to_path, from_path):
        os.utime(to_path, (
            os.path.getatime(from_path),
            os.path.getmtime(from_path),
        ))
        TimestampHelper.show(to_path)

    @staticmethod
    def shift(path, sec):
        ts = os.path.getmtime(path)
        ts += sec
        os.utime(path, (ts, ts))


if __name__ == "__main__":
    from tkinter import filedialog

    # filedialog.askopenfilename()
    # filedialog.askdirectory()

    # TimestampHelper.show(filedialog.askopenfilename())
    # TimestampHelper.copy(filedialog.askopenfilename(), filedialog.askopenfilename())
    # TimestampHelper.shift(filedialog.askdirectory(), -365*24*60*60)
