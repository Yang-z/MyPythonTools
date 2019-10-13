"""
usage:
    -recover the modified date of a folder according to the files within in.
     i.e, the modified date of a folder could be set to be the latest(or earliest) modified date of the files within.
"""


import os


class TimestampRecoverer4Folder(object):

    @staticmethod
    def recover(target_dir, strategy='latest', is_root=True):
        ts_earliest = None
        ts_latest = None

        for f in os.listdir(target_dir):
            path = os.path.join(target_dir, f)

            # ts_earliest_current = None
            # ts_latest_current = None

            if os.path.isdir(path):
                # 递归
                ts_earliest_current, ts_latest_current = TimestampRecoverer4Folder.recover(path, strategy, False)
            else:
                ts_earliest_current = os.path.getmtime(path)
                ts_latest_current = ts_earliest_current

            if ts_earliest_current is not None:
                if ts_earliest is None or ts_earliest > ts_earliest_current:
                    ts_earliest = ts_earliest_current

            if ts_latest_current is not None:
                if ts_latest is None or ts_latest < ts_latest_current:
                    ts_latest = ts_latest_current

        if ts_earliest is not None and ts_latest is not None:
            if strategy == 'earliest':
                os.utime(target_dir, (ts_earliest, ts_earliest))
            elif strategy == 'latest':
                os.utime(target_dir, (ts_latest, ts_latest))

        if is_root:
            print("earliest:", ts_earliest, "\nlatest:", ts_latest)

        return ts_earliest, ts_latest


if __name__ == "__main__":
    from tkinter import filedialog

    TimestampRecoverer4Folder.recover(filedialog.askdirectory(), 'latest')

