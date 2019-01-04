import os
import re
import tkinter.filedialog

import piexif

targetDir = tkinter.filedialog.askdirectory()
filesInDir = os.listdir(targetDir)

pSupportedExtensions = re.compile(r".([jJ][pP][eE][gG]|[jJ][pP][gG])$")
pDateFormat = re.compile(r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])[ _]?([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)")

count = 0
for fileName in filesInDir:
    name, extension = os.path.splitext(fileName)
    # exam the file type
    if not re.search(pSupportedExtensions, fileName):
        continue

    print('*******************************')
    fileDir = os.path.join(targetDir, fileName)
    print(fileDir)

    # get original time
    exif = piexif.load(fileDir)
    if not exif or "Exif" not in exif.keys() or piexif.ExifIFD.DateTimeOriginal not in exif["Exif"].keys() or not exif["Exif"][piexif.ExifIFD.DateTimeOriginal]:
        continue
    dateTimeOriginal = bytes.decode(exif["Exif"][piexif.ExifIFD.DateTimeOriginal]).replace(":", "")
    print(dateTimeOriginal)

    # format dateTime for file Name
    dateTime4FileName = ('IMG ' + dateTimeOriginal).replace(' ', '_')

    rDateFormat = re.search(pDateFormat, fileName)
    fileName_New = ""
    if not rDateFormat:
        fileName_New = dateTimeOriginal + " " + fileName
        print('Date in File Name added ')
    else:
        if dateTimeOriginal != rDateFormat.group(0):
            fileName_New = re.sub(pDateFormat, dateTimeOriginal, fileName)
            print('Date in File Name updated')
    if fileName_New != "":
        fileDir_New = os.path.join(targetDir, fileName_New)
        print(fileDir_New)
        os.rename(fileDir, fileDir_New)
        count += 1
        print(count)
print(count)