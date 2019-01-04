"""
usage:
    -analyse unix timestamp or formatted date time in file name
    -write the time indicated by file name back to file's modified time
    -rename file to state the date
*Time Zone Independent (Time Zone Safe)*
"""

import os
import re

# import time
from datetime import datetime

from dateutil import tz
# from dateutil.parser import parse

from tkinter import filedialog


class DateInNameAnalyser(object):
    # unix timestamp
    pattern_unix_timestamp_raw = r"(\d{13})\D"
    pattern_unix_timestamp = re.compile(pattern_unix_timestamp_raw)

    # YYYYMMDD HHMMSS ±zzzz
    pattern_date_time_raw = r'((?:\d{4})(?:0[1-9]|1[0-2])(?:0[1-9]|[1-2]\d|3[0-1]))' \
                            r'[ _]?' \
                            r'((?:[0-1]\d|2[0-3])(?:[0-5]\d)(?:[0-5]\d))' \
                            r'([ _]?[+-](?:[0-1]\d|2[0-3])(?:[0-5]\d))?'
    pattern_date_time = re.compile(pattern_date_time_raw)

    # data format for output
    time_string_format = '%Y%m%d %H%M%S%z'

    # count
    count_rename = 0
    count_reMTime = 0

    # controller
    should_rename = True
    should_reMTime = True

    # timezone
    timezone_target = tz.tzlocal()  # default time zone is the local time zone of your machine
    # timezone_target = tz.gettz('America/Los_Angeles)
    # any timezone you want, e.g. 'Asia/Shanghai' 'America/Cayman' 'Pacific/Kiritimati'

    @staticmethod
    def batch():
        _dir = filedialog.askdirectory()
        _files_in_dir = os.listdir(_dir)

        for _file_name in _files_in_dir:
            print("*******************************")
            _dateInNameAnalyser = DateInNameAnalyser(_dir, _file_name)
            print(_dateInNameAnalyser._file_path)
            if _dateInNameAnalyser._match_unix_timestamp:
                _dateInNameAnalyser.for_unix_timestamp()
            elif _dateInNameAnalyser._match_date_time:
                _dateInNameAnalyser.for_date_time()
            else:
                print("No date found in file name.")

    def __init__(self, file_dir, file_name):
        self._file_dir = file_dir

        # self._file_name = None
        # self._file_path = None
        # self._match_unix_timestamp = None
        # self._match_date_time = None
        self.set_file_name(file_name)

        self._timezone = DateInNameAnalyser.timezone_target

    def set_file_name(self, file_name):
        self._file_name = file_name
        self._file_path = os.path.join(self._file_dir, self._file_name)
        self._match_unix_timestamp = re.search(DateInNameAnalyser.pattern_unix_timestamp, self._file_name)
        self._match_date_time = re.search(DateInNameAnalyser.pattern_date_time, self._file_name)

    def for_unix_timestamp(self):
        m = self._match_unix_timestamp
        if m:
            time_string = m.group(1)
            print("time_string: " + time_string)
            timestamp = float(m.group(1)) / 1000
            print('timestamp: %.3f' % timestamp)

            # rewrite file modified time
            if DateInNameAnalyser.should_reMTime:
                self.write_timestamp_2_modified_time(timestamp)

            # rename
            if DateInNameAnalyser.should_rename:
                dt_from_ts = datetime.fromtimestamp(timestamp, self._timezone)
                self.write_datetime_2_filename(dt_from_ts)

    def for_date_time(self):
        m = self._match_date_time
        if m:
            time_string = m.group(0)
            print("time_string: " + time_string)
            time_string_organized = m.group(1) + " " + m.group(2)
            if m.group(3):
                time_string_organized += m.group(3)

            # use {datetime} instead of {time},
            # because {time} only deal with local time of machine.
            # {time.mktime(time_structure)} would ignore timezone info totally,
            # and use local tzinfo even when 'time_structure' has specified one.
            # time_structure = time.strptime(time_string_organized, time_string_format)
            # timestamp = time.mktime(time_structure)
            if m.group(3) is None:
                dt_from_string = datetime.strptime(time_string_organized, '%Y%m%d %H%M%S')
                dt_from_string = dt_from_string.replace(tzinfo=self._timezone)
            else:
                dt_from_string = datetime.strptime(time_string_organized, '%Y%m%d %H%M%S%z')
                self._timezone = dt_from_string.tzinfo
            # or use:
            # dt_from_string = parse(time_string_organized)

            # rewrite file modified time
            if DateInNameAnalyser.should_reMTime:
                timestamp = dt_from_string.timestamp()
                self.write_timestamp_2_modified_time(timestamp)

            # rename
            if DateInNameAnalyser.should_rename:
                self.write_datetime_2_filename(dt_from_string)

    def write_timestamp_2_modified_time(self, timestamp):
        print("Try reMTime...")

        # check the original MTime
        modified_time = os.path.getmtime(self._file_path)
        if modified_time == timestamp:
            return False
        time_string_from_MTime = \
            datetime.fromtimestamp(modified_time, self._timezone)\
                .strftime(DateInNameAnalyser.time_string_format)
            # = time.strftime(time_string_format, time.localtime(modified_time))
        print('Original MTime: %s %f' % (time_string_from_MTime, modified_time))

        # write timeStamp to file MTime
        time_string_from_timestamp = \
            datetime.fromtimestamp(timestamp, self._timezone) \
                .strftime(DateInNameAnalyser.time_string_format)
        print('  Target MTime: %s %f' % (time_string_from_timestamp, timestamp))
        os.utime(self._file_path, (timestamp, timestamp))
        DateInNameAnalyser.count_reMTime += 1
        print("DateInNameAnalyser.count_reMTime: %d" % DateInNameAnalyser.count_reMTime)

        # check the rewrote MTime
        modified_time_new = os.path.getmtime(self._file_path)
        time_string_from_MTime_new = \
            datetime.fromtimestamp(modified_time_new, self._timezone)\
                .strftime(DateInNameAnalyser.time_string_format)
        print('     New MTime: %s %f' % (time_string_from_MTime_new, modified_time_new))
        return True

    def write_datetime_2_filename(self, dt):
        print("Try rename...")

        time_string = dt.strftime(DateInNameAnalyser.time_string_format)

        if not self._match_date_time:
            file_name_new = time_string + " " + self._file_name
        #
        elif self._match_date_time.group(0) != time_string:
            file_name_new = re.sub(DateInNameAnalyser.pattern_date_time, time_string, self._file_name)
            # add or delete space? not here. Maybe in a re-formatter
        else:
            return False

        file_path_new = os.path.join(self._file_dir, file_name_new)
        print(file_path_new)
        os.rename(self._file_path, file_path_new)
        # change file name should be the last part of procedure, otherwise add the following line
        # self.set_file_name(file_name_new)

        DateInNameAnalyser.count_rename += 1
        print("DateInNameAnalyser.count_rename: %d" % DateInNameAnalyser.count_rename)
        return True


# DateInNameAnalyser.timezone_target = tz.gttz('Asia/Shanghai')
# DateInNameAnalyser.should_rename = False
# DateInNameAnalyser.should_reMTime = False
DateInNameAnalyser.batch()
