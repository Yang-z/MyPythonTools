"""
usage:
    -recover the modified date of a folder according to the files within in.
     i.e, the modified date of a folder could be set to be the latest(or earliest) modified date of the files within.
"""


import os


class TimestampRecoverer4Folder(object):

    @staticmethod
    def recover(root, strategy='latest'):
        ts_earliest = None
        ts_latest = None

        for f in os.listdir(root):
            path = os.path.join(root, f)

            if os.path.isdir(path):
                TimestampRecoverer4Folder.recover(path, strategy)

            ts_current = os.path.getmtime(path)

            if ts_earliest is None:
                ts_earliest = ts_current
            else:
                if ts_earliest > ts_current:
                    ts_earliest = ts_current

            if ts_latest is None:
                ts_latest = ts_current
            else:
                if ts_latest < ts_current:
                    ts_latest = ts_current

        ts = None
        if strategy == 'earliest':
            ts = ts_earliest
        elif strategy == 'latest':
            ts = ts_latest

        if ts is not None:
            os.utime(root, (ts, ts))


if __name__ == "__main__":
    from tkinter import filedialog

    TimestampRecoverer4Folder.recover(filedialog.askdirectory(), 'earliest')
