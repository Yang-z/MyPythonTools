import os
import re
# from datetime import datetime
from dateutil.parser import parse
from tkinter import filedialog


class PhotoNameFormatter(object):
    # jpeg or jpg which is supported by this script
    pattern_photo_extensions_raw = r'.([jJ][pP][eE][gG]|[jJ][pP][gG])$'
    pattern_photo_extensions = re.compile(pattern_photo_extensions_raw)

    # date pattern for input
    # YYYYMMDD HHMMSS ±zzzz
    i_pattern_date_time_raw = r'(?:IMG[ _])?'\
                              r'((?:\d{4})(?:0[1-9]|1[0-2])(?:0[1-9]|[1-2]\d|3[0-1]))'\
                              r'[ _]?'\
                              r'((?:[0-1]\d|2[0-3])(?:[0-5]\d)(?:[0-5]\d))'\
                              r'([ _]?[+-](?:[0-1]\d|2[0-3])(?:[0-5]\d))?'\
                              r'[ _]*'
    i_pattern_date_time = re.compile(i_pattern_date_time_raw)

    # date format for output
    o_format_date_time = 'IMG_%Y%m%d_%H%M%S%z '

    # count
    count_rename = 0

    @staticmethod
    def batch():
        _dir = filedialog.askdirectory()
        _files_in_dir = os.listdir(_dir)

        for _file_name in _files_in_dir:
            print("*******************************")
            _photoNameFormatter = PhotoNameFormatter(_dir, _file_name)
            _photoNameFormatter.reformat()

    def __init__(self, file_dir, file_name):
        self._file_dir = file_dir
        self._file_name = file_name
        self._file_path = os.path.join(self._file_dir, self._file_name)

    def reformat(self):
        print(self._file_path)

        if re.search(PhotoNameFormatter.pattern_photo_extensions, self._file_name) is None:
            return False

        m = re.search(PhotoNameFormatter.i_pattern_date_time, self._file_name)
        if not m:
            return False

        # get organised time string
        time_string_organised = m.group(1) + " " + m.group(2)
        if m.group(3):
            time_string_organised += m.group(3)

        # get datetime
        dt = parse(time_string_organised)
        # or:
        """
        if m.group(3) is None:
            dt = datetime.strptime(time_string_organised, '%Y%m%d %H%M%S')
        else:
            dt = datetime.strptime(time_string_organised, '%Y%m%d %H%M%S%z')
        """

        time_string_reformatted = dt.strftime(PhotoNameFormatter.o_format_date_time)
        file_name_new = re.sub(PhotoNameFormatter.i_pattern_date_time, time_string_reformatted, self._file_name)

        if file_name_new == self._file_name:
            return False

        file_path_new = os.path.join(self._file_dir, file_name_new)
        print(file_path_new)
        os.rename(self._file_path, file_path_new)

        PhotoNameFormatter.count_rename += 1
        print("PhotoNameFormatter.count_rename: %d" % PhotoNameFormatter.count_rename)
        return True


def main():
    # control the output format:
    # PhotoNameFormatter.o_format_date_time = 'IMG_%Y%m%d_%H%M%S%z '  # default
    # PhotoNameFormatter.o_format_date_time = '%Y%m%d %H%M%S%z '
    PhotoNameFormatter.batch()


if __name__ == "__main__":
    main()
