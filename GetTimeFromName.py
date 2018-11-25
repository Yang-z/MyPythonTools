import os, time
import tkFileDialog

targetDir = tkFileDialog.askdirectory()
filesInDir = os.listdir(targetDir)

count = 0
for eachFile in filesInDir:
    print '*******************************'

    fileDir = os.path.join(targetDir, eachFile)
    print fileDir

    modifiedTime = os.path.getmtime(fileDir)
    print ' Current MTime: ' + time.strftime('%Y%m%d %H%M%S', time.localtime(modifiedTime))

    fileDeclaimData = eachFile[0:15]
    print '  Target MTime: ' + fileDeclaimData
    timeArray = time.strptime(fileDeclaimData, "%Y%m%d %H%M%S")
    timeStamp = time.mktime(timeArray)
    os.utime(fileDir, (timeStamp, timeStamp))

    modifiedTime = os.path.getmtime(fileDir)
    print 'Modified MTime: ' + time.strftime('%Y%m%d %H%M%S', time.localtime(modifiedTime))

    count += 1

    print count




