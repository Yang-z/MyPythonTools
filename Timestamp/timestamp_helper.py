"""
    Ref:
        https://docs.python.org/3/library/os.html
        https://unix.stackexchange.com/questions/11599/determine-file-system-timestamp-precision
        https://www.cnblogs.com/chezxiaoqiang/archive/2012/03/23/2674386.html
    ways to get and set timestamp:
        ❌mtime = os.path.getmtime(path)
        ✔️mtime_ns = os.stat(path).st_mtime_ns
        ✔️os.utime(path, ns=(time.time_ns(), mtime_ns))
    In order to preserve exact times, this script only dealing with nanoseconds
"""

import os
import time


class TimestampHelper(object):
    @staticmethod
    def get(path, atime=False):
        print(path)
        stat_result = os.stat(path)
        mtime_ns = stat_result.st_mtime_ns
        print("mtime_ns: ", mtime_ns)
        if not atime:
            return mtime_ns
        else:
            atime_ns = stat_result.st_atime_ns
            print("atime_ns: ", atime_ns)
            return mtime_ns, atime_ns

    @staticmethod
    def set(path, mtime_ns, sub=False, decrease_only=True, delt_ns=0, atime_ns=None):
        mtime_ns_o = TimestampHelper.get(path)
        # only decrease timestamp，not increase
        if mtime_ns < mtime_ns_o or decrease_only == False:
            os.utime(
                path,
                ns=(
                    time.time_ns() if atime_ns is None else atime_ns,
                    mtime_ns
                )
            )
            mtime_ns += delt_ns
            TimestampHelper.get(path)
        else:
            print("❌ set denied (try to increase timestamp)")

        # do for the sub path
        if sub and os.path.isdir(path):
            for f in os.listdir(path):
                path_sub = os.path.join(path, f)
                mtime_ns = TimestampHelper.set(
                    path_sub, mtime_ns, sub, decrease_only, delt_ns)

        return mtime_ns

    @staticmethod
    def copy(path_target, path_source, sub=False):
        mtime_source = TimestampHelper.get(path_source)
        TimestampHelper.set(path_target, mtime_source, sub)

    @staticmethod
    def shift(path, delt_ns, sub=False):
        mtime_ns = TimestampHelper.get(path) + delt_ns
        os.utime(path, ns=(mtime_ns, mtime_ns))
        TimestampHelper.get(path)

        # do for the sub path
        if sub and os.path.isdir(path):
            for f in os.listdir(path):
                path_sub = os.path.join(path, f)
                TimestampHelper.shift(path_sub, delt_ns, sub)


def shell():
    from common.Shell import file_or_dir, yes_or_no, choose_one

    i = choose_one(
        "TimestampHelper Shell: ",
        [
            'get',  # 0
            'set',  # 1
            'copy',  # 2
            'shift'  # 3
        ],
        -1,
        True
    )

    if(i == 0):  # get
        path = file_or_dir()
        TimestampHelper.get(path)

    elif(i == 1):  # set
        path = file_or_dir()
        mtime_ns = int(input('timestamp (in nanoseconds): '))
        sub = False if not os.path.isdir(path) else yes_or_no(
            title="do for the sub path?", default=False)
        decrease_only = yes_or_no(
            title="only decrease timestamp?", default=True)
        delt_ns = int(input('timestamp shift per file (in nanoseconds): '))
        TimestampHelper.set(path, mtime_ns, sub, decrease_only, delt_ns)

    elif(i == 2):  # copy
        path_target = file_or_dir("target")
        path_source = file_or_dir("source")
        sub = False if not os.path.isdir(path_target) else yes_or_no(
            title="do for the sub path?", default=False)
        TimestampHelper.copy(path_target, path_source, sub)

    elif(i == 3):  # shift
        path = file_or_dir()
        dt_ns = int(input('dt (in nanoseconds): '))
        sub = False if not os.path.isdir(path) else yes_or_no(
            title="do for the sub path?", default=False)
        TimestampHelper.shift(path, dt_ns, sub)

    else:
        print("❌ function not find")


if __name__ == "__main__":
    shell()
