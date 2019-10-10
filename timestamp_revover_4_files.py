import os, time, re
import tkFileDialog

targetDir = tkFileDialog.askdirectory()
filesInDir = os.listdir(targetDir)

p0s = r"(\d{13})\D"
p0 = re.compile(p0s)
p1s = r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])[ _]([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)"
p1 = re.compile(p1s)

count = 0
for fileName in filesInDir:
    print '*******************************'

    fileDir = os.path.join(targetDir, fileName)
    print fileDir

    modifiedTime = os.path.getmtime(fileDir)
    print 'Current MTime: ' + time.strftime('%Y%m%d %H%M%S', time.localtime(modifiedTime))

    strIndicateTime = None
    timeStamp = None
    if strIndicateTime is None:
        m0 = re.search(p0, fileName)
        if m0:
            strIndicateTime = m0.group(1)
            timeStamp = float(m0.group(1)) / 1000
    if strIndicateTime is None:
        m1 = re.search(p1, fileName)
        if m1:
            strIndicateTime = m1.group(0)
            timeArray = time.strptime(
                m1.group(1) +
                m1.group(2) +
                m1.group(3) +
                " " +
                m1.group(4) +
                m1.group(5) +
                m1.group(6)
            , "%Y%m%d %H%M%S")
            timeStamp = time.mktime(timeArray)

    if strIndicateTime:
        print 'strIndicateTime: ' + strIndicateTime
        if timeStamp:
            print 'timeStamp: %.3f' % timeStamp
            print ' Target MTime: ' + time.strftime('%Y%m%d %H%M%S', time.localtime(timeStamp))
            os.utime(fileDir, (timeStamp, timeStamp))
            count += 1
            print count

    modifiedTime = os.path.getmtime(fileDir)
    print '    New MTime: ' + time.strftime('%Y%m%d %H%M%S', time.localtime(modifiedTime))






