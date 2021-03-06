import os


class TimestampHelper(object):
    @staticmethod
    def show(path):
        print(path)
        # print("atime:", os.path.getatime(path))
        print("mtime:", os.path.getmtime(path))

    @staticmethod
    def set(path, timestamp, sub=False, decrease_only=True, delt = 0):
        timestamp_o = os.path.getmtime(path)

        # only decrease timestamp，not increase
        if timestamp < timestamp_o or decrease_only == False:
            os.utime(path, (timestamp, timestamp))
            timestamp += delt
            TimestampHelper.show(path)
        else:
            print("denied: try to increase timestamp ")

        # do for the sub path
        if sub and os.path.isdir(path):
            for f in os.listdir(path):
                sub_path = os.path.join(path, f)
                timestamp = TimestampHelper.set(sub_path, timestamp, sub, decrease_only, delt)
        
        return timestamp

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



def shell():
    from common.Shell import file_or_dir, yes_or_no, choose_one

    i = choose_one(
        "TimestampHelper Shell: ",
        [
            'show', # 0
            'set',  # 1
            'copy', # 2
            'shift' # 3
        ],
        -1,
        True
    )

    if(i == 0):
        path = file_or_dir()
        TimestampHelper.show(path)
    elif(i == 1):
        path = file_or_dir()
        timestamp = float(input('timestamp (in seconds): '))
        sub = False if not os.path.isdir(path) else yes_or_no(title="do for the sub path?", default=False)
        decrease_only = yes_or_no(title="only decrease timestamp?", default=True)
        delt = float(input('timestamp shift per file (in seconds): '))
        TimestampHelper.set(path, timestamp, sub, decrease_only, delt)
    elif(i == 2):
        path_target = file_or_dir("target")
        path_source = file_or_dir("source")
        sub = False if not os.path.isdir(path_target) else yes_or_no(title="do for the sub path?", default=False)
        TimestampHelper.copy(path_target, path_source, sub)
    elif(i == 3):
        path = file_or_dir()
        dt = float(input('dt (in seconds): '))
        sub = False if not os.path.isdir(path) else yes_or_no(title="do for the sub path?", default=False)
        TimestampHelper.shift(path, dt, sub)
    else:
        print("function not find")


if __name__ == "__main__":
    shell()
