import os, time, re


class TimestampRecoverer4Files(object):
    p_timestamp = re.compile(r"(\d{13})\D")
    p_datetime = re.compile(r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])[ _]([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)")

    @staticmethod
    def get_timestamp_from_name(file_name):

        timestamp = None
        timestamp_from_dt = None

        m_ts = re.search(TimestampRecoverer4Files.p_timestamp, file_name)
        if m_ts:
            str_ts = m_ts.group(1)
            timestamp = float(str_ts) / 1000

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
                m_dt.group(6)
            , "%Y%m%d %H%M%S")
            timestamp_from_dt = time.mktime(time_array)

        print("Timestamp_str: ", str_ts, "  |   timestamp: ", timestamp)
        print("Datetime_str: ", str_dt, "   |   timestamp: ", timestamp_from_dt)

        return timestamp, timestamp_from_dt

    @staticmethod
    def recover_by_name(path):
        print(path)
        print("Current MTime: " + time.strftime('%Y%m%d %H%M%S', time.localtime(os.path.getmtime(path))))

        dir, name = os.path.split(path)
        timestamp, timestamp_from_dt = TimestampRecoverer4Files.get_timestamp_from_name(name)
        if timestamp is not None:
            os.utime(path, (timestamp, timestamp))
        elif timestamp_from_dt is not None:
            os.utime(path, (timestamp_from_dt, timestamp_from_dt))

        print("New MTime: " + time.strftime('%Y%m%d %H%M%S', time.localtime(os.path.getmtime(path))))

        if os.listdir(path):
            print(path, r"\...")
            for name in os.listdir(path):
                sub_path = os.path.join(path, name)
                # 递归
                TimestampRecoverer4Files.recover_by_name(sub_path)
