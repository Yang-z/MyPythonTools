import os
from Timestamp.timestamp_helper import TimestampHelper as TSHelper
from common.Data import Data


class TimestampRecorder(object):
    @staticmethod
    def record(target_dir):
        target_dir_len = len(target_dir)
        dic = {}
        save_dir = os.path.join(target_dir, "timestamp.txt")
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                mtime_ns = TSHelper.get(file_path)
                dic[file_path[target_dir_len:]] = mtime_ns
        Data.save(dic, save_dir)


if __name__ == "__main__":
    from tkinter import filedialog
    TimestampRecorder.record(
        filedialog.askdirectory(title="TimestampRecorder"))
