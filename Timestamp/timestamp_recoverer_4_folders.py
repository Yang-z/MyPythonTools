"""
usage:

    -Recover the modified date of folders according to the files within.
     i.e, the modified date of a folder could be set to be the latest(or earliest) modified date of the files within.

    -Help to sync the timestamp of folders with a cloud storage by renaming the folders.
     e.g. google drive doesn't sync the timestamp of folders until a name-changing is detected. Thus, we can rename
     folders to force google drive to sync the timestamp. After the sync is completed, rename the folders back to its
     original name, and sync with google drive again. Note, when use this script to rename folders, google drive sync
     process should be paused to prevent unexpected conflicts.

"""


import os
from Timestamp.timestamp_helper import TimestampHelper as TSHelper


class TimestampRecoverer4Folders(object):

    @staticmethod
    def recover(target_dir, strategy='latest', refresh=None, is_root=True):
        ts_earliest = None
        ts_latest = None

        for f in os.listdir(target_dir):
            path = os.path.join(target_dir, f)

            # ts_earliest_current = None
            # ts_latest_current = None

            if os.path.isdir(path):
                # recursion 递归
                ts_earliest_current, ts_latest_current \
                    = TimestampRecoverer4Folders.recover(path, strategy, refresh, False)
            else:
                ts_earliest_current = TSHelper.get(path)
                ts_latest_current = ts_earliest_current

            if ts_earliest_current is not None:
                if ts_earliest is None or ts_earliest > ts_earliest_current:
                    ts_earliest = ts_earliest_current

            if ts_latest_current is not None:
                if ts_latest is None or ts_latest < ts_latest_current:
                    ts_latest = ts_latest_current

        if ts_earliest is not None and ts_latest is not None:
            if strategy == 'earliest':
                TSHelper.set(target_dir, ts_earliest)
            elif strategy == 'latest':
                TSHelper.set(target_dir, ts_latest, decrease_only=False)

        # None: do nothing
        # True: rename folder to include refresh key
        # False: rename folder back to its original name
        if refresh is not None:
            refresh_key = r"[$SyncMyTimestamp!$]"
            up_dir, target_folder = os.path.split(target_dir)
            new_target_folder = None

            if refresh is True:
                if refresh_key not in target_folder:
                    new_target_folder = refresh_key + target_folder
            elif refresh is False:
                if refresh_key in target_folder:
                    new_target_folder = str.replace(
                        target_folder, refresh_key, "")

            if new_target_folder is not None:
                new_target_dir = os.path.join(up_dir, new_target_folder)
                os.rename(target_dir, new_target_dir)

        if is_root:
            print("earliest:", ts_earliest, "\nlatest:", ts_latest)

        return ts_earliest, ts_latest


def shell():
    from tkinter import filedialog
    from common.Shell import choose_one

    i = choose_one(
        "TimestampRecoverer4Folders Shell: ",
        [
            'recover'
        ],
        -1,
        True
    )

    if(i == 0):
        path = filedialog.askdirectory()
        strategy = choose_one(
            "strategy: ",
            [
                'latest',
                'earliest'
            ],
            0
        )
        refresh = choose_one(
            "refresh:\n" +
            "# None: do nothing\n" +
            "# True: rename folder to include refresh key\n" +
            "# False: rename folder back to its original name",
            [
                None,
                True,
                False
            ],
            0
        )

        TimestampRecoverer4Folders.recover(path, strategy, refresh)
    else:
        print("function not find")


if __name__ == "__main__":
    shell()
