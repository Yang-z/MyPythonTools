import os
import time
import re
import hashlib

from Timestamp.timestamp_helper import TimestampHelper as TSHelper


class TimestampRecoverer4Files(object):
    p_timestamp = re.compile(r"(\d{13})\D")
    p_datetime = re.compile(
        r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])[ _]([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)")

    @staticmethod
    def get_timestamp_from_name(file_name):

        timestamp = None
        timestamp_from_dt = None

        m_ts = re.search(TimestampRecoverer4Files.p_timestamp, file_name)
        if m_ts:
            str_ts = m_ts.group(1)
            timestamp = int(str_ts) * 1000 * 1000

        m_dt = re.search(TimestampRecoverer4Files.p_datetime, file_name)
        if m_dt:
            str_dt = m_dt.group(0)
            time_array = time.strptime(
                m_dt.group(1) +
                m_dt.group(2) +
                m_dt.group(3) +
                " " +
                m_dt.group(4) +
                m_dt.group(5) +
                m_dt.group(6), "%Y%m%d %H%M%S")
            # ⚠️ local time is involved, not timezone safe
            timestamp_from_dt = time.mktime(time_array) * 1000 * 1000 * 1000

        print("Timestamp_str: ", str_ts, "  |   timestamp: ", timestamp)
        print("Datetime_str: ", str_dt, "   |   timestamp: ", timestamp_from_dt)

        return timestamp, timestamp_from_dt

    @staticmethod
    def recover_by_name(path):
        print(path)
        print("Current MTime: " + time.strftime('%Y%m%d %H%M%S',
              time.localtime(os.path.getmtime(path))))

        dir, name = os.path.split(path)
        timestamp, timestamp_from_dt \
            = TimestampRecoverer4Files.get_timestamp_from_name(name)
        ts = timestamp if timestamp is not None else timestamp_from_dt
        if ts is not None:
            TSHelper.set(path, ts)
            print("New MTime: " + time.strftime('%Y%m%d %H%M%S',
                                                time.localtime(os.path.getmtime(path))))

        if os.listdir(path):
            print(path, r"\...")
            for name in os.listdir(path):
                sub_path = os.path.join(path, name)
                # 递归
                TimestampRecoverer4Files.recover_by_name(sub_path)

    @staticmethod
    def get_hash_from_file(file_path):
        with open(file_path, 'rb') as f:
            _md5obj = hashlib.md5()
            _md5obj.update(f.read())
            _hash = _md5obj.hexdigest()
            return _hash

    @staticmethod
    def recover_by_hash(target_dir, source_dir, dry_run=False):
        # source
        source_hash = {}
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = TimestampRecoverer4Files.get_hash_from_file(
                    file_path)
                if file_hash not in source_hash.keys():
                    source_hash[file_hash] = file_path
                else:
                    mtime = TSHelper.get(source_hash[file_hash])
                    mtime2 = TSHelper.get(file_path)
                    # record the earliest one
                    if mtime2 < mtime:
                        source_hash[file_hash] = file_path

        # target
        count = 0
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash \
                    = TimestampRecoverer4Files.get_hash_from_file(file_path)
                if file_hash in source_hash.keys():
                    mtime_source, atime_source \
                        = TSHelper.get(source_hash[file_hash], atime=True)
                    mtime_target = TSHelper.get(file_path)
                    if mtime_source < mtime_target:
                        # atime_source = os.path.getatime(source_hash[file_hash])
                        if dry_run is False:
                            TSHelper.set(file_path, mtime_source, atime_ns=atime_source)
                        count += 1
                        print(count)
                        print(file_hash)
                        print(file_path)
                        print("↑↑↑mtime_target: ", mtime_target)
                        print(source_hash[file_hash])
                        print("↑↑↑mtime_source: ", mtime_source)


def shell():
    from tkinter import filedialog
    from common.Shell import yes_or_no, choose_one

    i = choose_one(
        "TimestampRecoverer4Files Shell: ",
        [
            'recover by name',
            'recover by hash'
        ],
        -1,
        True
    )

    if(i == 0):
        TimestampRecoverer4Files.recover_by_name(filedialog.askdirectory())
    elif(i == 1):
        TimestampRecoverer4Files.recover_by_hash(
            filedialog.askdirectory(title="target"),
            filedialog.askdirectory(title="source"),
            yes_or_no(title="dry run?", default=True)
        )
    else:
        print("function not find")


if __name__ == "__main__":
    shell()
