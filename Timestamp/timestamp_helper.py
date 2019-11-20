import os


class TimestampHelper(object):
    @staticmethod
    def show(path):
        print(path)
        # print("atime:", os.path.getatime(path))
        print("mtime:", os.path.getmtime(path))

    @staticmethod
    def set(path, timestamp, sub=False):
        timestamp_o = os.path.getmtime(path)

        # only bring time ahead，no delay
        if timestamp < timestamp_o:
            os.utime(path, (timestamp, timestamp))
            TimestampHelper.show(path)

        # do for the sub path
        if sub and os.path.isdir(path):
            for f in os.listdir(path):
                sub_path = os.path.join(path, f)
                TimestampHelper.set(sub_path, timestamp, sub)

    @staticmethod
    def copy(target_path, source_path, sub=False):
        source_mt = os.path.getmtime(source_path)
        TimestampHelper.set(target_path, source_mt, sub)

    @staticmethod
    def shift(path, shift_sec, sub=False):
        ts = os.path.getmtime(path) + shift_sec
        os.utime(path, (ts, ts))
        TimestampHelper.show(path)

        # do for the sub path
        if sub and os.path.isdir(path):
            for f in os.listdir(path):
                sub_path = os.path.join(path, f)
                TimestampHelper.shift(sub_path, shift_sec, sub)




if __name__ == "__main__":
    from tkinter import filedialog

    # filedialog.askopenfilename()
    # filedialog.askdirectory()

    # TimestampHelper.show(filedialog.askopenfilename())
    # TimestampHelper.set(filedialog.askopenfilename(), float(input('timestamp: ')), False)
    # TimestampHelper.copy(filedialog.askopenfilename(), filedialog.askopenfilename(), False)
    # TimestampHelper.shift(filedialog.askdirectory(), -1*365*24*60*60, True)
