"""
    Copy exif from one file to another.
    Or you can use:
        https://exiftool.org/gui/
"""

import piexif
import os.path


def copy_exif(origin=None, target=None):
    origin = origin if origin else input("Origin file: ")
    target = target if target else input("Target file: ")
    if origin == target: return
    
    if os.path.isfile(origin) and os.path.isfile(target):
        piexif.transplant(origin, target)
        print_info(origin, target)

    elif os.path.isdir(origin) and os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file_ in files:
                target_file_path = os.path.join(root, file_)
                origin_file_path = target_file_path.replace(target, origin)
                if os.path.isfile(origin_file_path):
                    piexif.transplant(origin_file_path, target_file_path)
                    print_info(origin_file_path, target_file_path)

    else: 
        return

def print_info(origin, target):
    print(target)
    print(" <- " + origin)
    

if __name__ == "__main__":
    from tkinter import filedialog

    # origin = filedialog.askopenfilename(title="Origin")
    # exif = piexif.load(origin)
    # key = piexif.ImageIFD.Software

    origin = filedialog.askdirectory(title="Origin")
    target = filedialog.askdirectory(title="Target")
    copy_exif(origin, target)

    print('0')
