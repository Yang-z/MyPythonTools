"""
usage:
    -analyse unix timestamp or formatted date time in file name (for any file)
    -analyse date time in EXIF (for photos only)
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

import piexif

from tkinter import filedialog


class PhotoDateAnalyser(object):
    # jpeg or jpg which may contains EIXF data
    pattern_photo_extensions_raw = r'.([jJ][pP][eE][gG]|[jJ][pP][gG])$'
    pattern_photo_extensions = re.compile(pattern_photo_extensions_raw)

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
    format_date_time = '%Y%m%d %H%M%S%z'

    # count
    count_reMTime = 0
    count_rename = 0

    @staticmethod
    def batch(strategy_id, tzinfo_default, should_reMTime, should_rename):
        _dir = filedialog.askdirectory()
        _files_in_dir = os.listdir(_dir)

        for _file_name in _files_in_dir:
            print("*******************************")
            _photoDateAnalyser = PhotoDateAnalyser(_dir, _file_name)
            print(_photoDateAnalyser._file_path)
            _photoDateAnalyser.exe(strategy_id, tzinfo_default, should_reMTime, should_rename)

    def __init__(self, file_dir, file_name):
        self._file_dir = file_dir

        self._file_name = None
        self._file_path = None
        self._match_unix_timestamp = None
        self._match_date_time = None
        self.set_file_name(file_name)

        self.time_string_raw = None
        self.timestamp = None
        self.datetime: datetime = None
        # self.reset_time_cash()

    def set_file_name(self, file_name):
        self._file_name = file_name
        self._file_path = os.path.join(self._file_dir, self._file_name)
        self._match_unix_timestamp = re.search(PhotoDateAnalyser.pattern_unix_timestamp, self._file_name)
        self._match_date_time = re.search(PhotoDateAnalyser.pattern_date_time, self._file_name)
        self._match_photo_extensions = re.search(PhotoDateAnalyser.pattern_photo_extensions, self._file_name)

    def reset_time_cash(self):
        self.time_string_raw = None
        self.timestamp = None
        self.datetime: datetime = None

    def exe(self, strategy_id, tzinfo_default, should_reMTime, should_rename):
        if not self.strategy(strategy_id):
            return False
        if not self.analyse(tzinfo_default):
            return False
        if should_reMTime:
            self.write_timestamp_2_modified_time()
        if should_rename:
            self.write_datetime_2_filename()

    # default time zone info
    # Use only when no time zone info is found in the file.
    # In cause time zone info is missing in file of photo,
    # it's better to provide one, if you know where the photo was taken.
    # tzinfo_default = tz.gettz('Asia/Shanghai')
    # e.g. 'Asia/Shanghai' 'America/Los_Angeles 'America/Cayman' 'Pacific/Kiritimati'
    def analyse(self, tzinfo_default):
        if self.timestamp is None and self.datetime is None:
            return False

        if self.datetime is None or (self.datetime.tzinfo is None and self.timestamp is None):
            if tzinfo_default is None:
                print("warning: time zone is not not found in file and not provided by user.")
                return False

        if self.datetime is None:
            self.datetime = datetime.fromtimestamp(self.timestamp, tzinfo_default)
        elif self.timestamp is None:
            if self.datetime is not None and self.datetime.tzinfo is None:
                self.datetime = self.datetime.replace(tzinfo=tzinfo_default)
            self.timestamp = self.datetime.timestamp()
        elif self.datetime.tzinfo is None:
            # timestamp is not None and datetime is not None, but tzinfo is None
            # it is able to calculate the time zone
            # [further research is needed]
            return None
        return True

    # strategy id:
    # 'AUTO' 'EXIF' 'TIMESTAMP_IN_FILE_NAME' 'DATETIME_IN_FILE_NAME'
    def strategy(self, strategy_id):
        if strategy_id == 'AUTO':
            if \
                    not self.from_date_time_in_exif() and \
                    not self.from_unix_timestamp_in_name() and \
                    not self.from_date_time_in_name():
                print("Error: No date found.")
                return False
        elif strategy_id == 'EXIF':
            self.from_date_time_in_exif()
        elif strategy_id == 'TIMESTAMP_IN_FILE_NAME':
            self.from_unix_timestamp_in_name()
        elif strategy_id == 'DATETIME_IN_FILE_NAME':
            self.from_date_time_in_name()
        else:
            print("ERROR: Strategy ID %s is not found." % strategy_id)
            return False
        return True

    def from_unix_timestamp_in_name(self):
        m = self._match_unix_timestamp
        if not m:
            return False

        self.reset_time_cash()

        self.time_string_raw = m.group(1)
        print("time_string: " + self.time_string_raw)
        self.timestamp = float(m.group(1)) / 1000
        print('timestamp: %.3f' % self.timestamp)

        return True

    def from_date_time_in_name(self):
        m = self._match_date_time
        if not m:
            return False

        self.reset_time_cash()

        self.time_string_raw = m.group(0)
        print("time_string: " + self.time_string_raw)
        time_string_organised = m.group(1) + " " + m.group(2)
        if m.group(3):
            time_string_organised += m.group(3)

        # use {datetime} instead of {time},
        # because {time} only deal with local time of machine.
        # {time.mktime(time_structure)} would ignore timezone info totally,
        # and use local tzinfo even when 'time_structure' has specified one.
        # time_structure = time.strptime(time_string_organised, format_date_time)
        # timestamp = time.mktime(time_structure)
        if m.group(3) is None:
            self.datetime = datetime.strptime(time_string_organised, '%Y%m%d %H%M%S')
            # add a timezone info? not here
            # dt_from_string = dt_from_string.replace(tzinfo=self._timezone)
        else:
            self.datetime = datetime.strptime(time_string_organised, '%Y%m%d %H%M%S%z')
        # or use:
        # dt_from_string = parse(time_string_organised)

        return True

    def from_date_time_in_exif(self):
        if not self._match_photo_extensions:
            return False

        self.reset_time_cash()

        # get original time
        exif = piexif.load(self._file_path)
        if not exif \
                or "Exif" not in exif.keys() \
                or piexif.ExifIFD.DateTimeOriginal not in exif["Exif"].keys() \
                or not exif["Exif"][piexif.ExifIFD.DateTimeOriginal]:
            return False
        self.time_string_raw = bytes.decode(exif["Exif"][piexif.ExifIFD.DateTimeOriginal])
        print("time_string_exif: " + self.time_string_raw)
        self.datetime = datetime.strptime(self.time_string_raw.replace(":", ""), '%Y%m%d %H%M%S')

        # there is no time zone tag in standard exif...
        # do something to extract time zone info from exif.
        # GPS coordinates: reflects a time zone info (Google Photos is quite good at it);
        # GPS time (UTC time): with original date it indicates time zone offset (Google Photos just ignores it)
        # gps_timezone = ?
        # self.datetime = dt_from_string.replace(tzinfo=gps_timezone)
        # [further research is needed]

        return True

    def write_timestamp_2_modified_time(self):
        print("Try reMTime...")
        if self.timestamp is None:
            return False

        # check the original MTime
        modified_time = os.path.getmtime(self._file_path)
        if modified_time == self.timestamp:
            return False
        time_string_from_MTime = \
            datetime.fromtimestamp(modified_time, self.datetime.tzinfo)\
                .strftime(PhotoDateAnalyser.format_date_time)
        # time_string_from_MTime = time.strftime(format_date_time, time.localtime(modified_time))
        print('Original MTime: %s %f' % (time_string_from_MTime, modified_time))

        # write timeStamp to file MTime
        time_string_from_timestamp = \
            datetime.fromtimestamp(self.timestamp, self.datetime.tzinfo) \
                .strftime(PhotoDateAnalyser.format_date_time)
        print('  Target MTime: %s %f' % (time_string_from_timestamp, self.timestamp))
        os.utime(self._file_path, (self.timestamp, self.timestamp))
        PhotoDateAnalyser.count_reMTime += 1
        print("PhotoDateAnalyser.count_reMTime: %d" % PhotoDateAnalyser.count_reMTime)

        # check the rewrote MTime
        modified_time_new = os.path.getmtime(self._file_path)
        time_string_from_MTime_new = \
            datetime.fromtimestamp(modified_time_new, self.datetime.tzinfo)\
                .strftime(PhotoDateAnalyser.format_date_time)
        print('     New MTime: %s %f' % (time_string_from_MTime_new, modified_time_new))
        return True

    def write_datetime_2_filename(self):
        print("Try rename...")
        if self.datetime is None:
            return False

        time_string = self.datetime.strftime(PhotoDateAnalyser.format_date_time)

        if not self._match_date_time:
            file_name_new = time_string + " " + self._file_name
        #
        elif self._match_date_time.group(0) != time_string:
            file_name_new = re.sub(PhotoDateAnalyser.pattern_date_time, time_string, self._file_name)
            # add or delete space? not here. Maybe in a re-formatter
        else:
            return False

        file_path_new = os.path.join(self._file_dir, file_name_new)
        print(file_path_new)
        os.rename(self._file_path, file_path_new)
        # change file name should be the last part of procedure, otherwise add the following line
        # self.set_file_name(file_name_new)

        PhotoDateAnalyser.count_rename += 1
        print("PhotoDateAnalyser.count_rename: %d" % PhotoDateAnalyser.count_rename)
        return True


def main():
    # strategy_id:
    # i.e. 'AUTO' 'EXIF' 'TIMESTAMP_IN_FILE_NAME' 'DATETIME_IN_FILE_NAME'

    # tzinfo_default = tz.gettz('Asia/Shanghai')
    # e.g. 'Asia/Shanghai' 'America/Los_Angeles 'America/Cayman' 'Pacific/Kiritimati' and so on

    PhotoDateAnalyser.batch(
        strategy_id='TIMESTAMP_IN_FILE_NAME',
        tzinfo_default=tz.gettz('Asia/Shanghai'),
        should_reMTime=True,
        should_rename=True
    )

    """
    PhotoDateAnalyser.batch(
        strategy_id='EXIF', 
        tzinfo_default=tz.gettz('Asia/Shanghai'), 
        should_reMTime=False, 
        should_rename=True
    )
    """


if __name__ == "__main__":
    main()
