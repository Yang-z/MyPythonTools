import os
import re

import piexif

import time
from datetime import datetime

# import pytz
# import dateutil
from dateutil import tz
from dateutil.parser import parse

s="1/60"
print(s)
print('/' in s)
(s0, s1) = s.split('/')
print(s0)
print(s1)

"""
# YYYYMMDD HHMMSS ±zzzz
p1s = r'((?:\d{4})(?:0[1-9]|1[0-2])(?:0[1-9]|[1-2]\d|3[0-1]))' \
                            r'[ _]?' \
                            r'((?:[0-1]\d|2[0-3])(?:[0-5]\d)(?:[0-5]\d))' \
                            r'([ _]?[+-](?:[0-1]\d|2[0-3])(?:[0-5]\d))?'
p1 = re.compile(p1s)
fileName = '20190102 223701 +0800 original name'
m1 = re.search(p1, fileName)
timeString_Organized = m1.group(1) + " " + m1.group(2)
if m1.group(3): timeString_Organized += " " + m1.group(3)
dt_from_string = parse(timeString_Organized)
print("end")
"""


"""
d = parse("19700101 080000+07:00")
ts = d.timestamp()
d2 = parse("19700101 080000+0700")
d2_1 = datetime.strptime("19700101 080000+0700", '%Y%m%d %H%M%S%z')
ts2 = d2.timestamp()
s = d2.strftime("IMG_%Y%m%d_%H%M%S%Z%z")
print("end")
"""


"""
fileName = "19700103_080000 apple.jpg"
tz0 = tz.gettz('Asia/Shanghai')
tz1 = tz.gettz('America/Cayman')  # 'America/Los_Angeles'
tz2 = tz.gettz('Pacific/Kiritimati')

# YYYYMMDD HHMMSS
p1s = r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])[ _]([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)"
p1 = re.compile(p1s)

m1 = re.search(p1, fileName)
timeString = m1.group(0)

timeString_Organized = m1.group(1) + m1.group(2) + m1.group(3) + " " + m1.group(4) + m1.group(5) + m1.group(6)
#timeString_Organized_TimeZone = timeString_Organized + " " + tz.tzname()

dt1 = datetime.datetime.strptime(timeString_Organized, "%Y%m%d %H%M%S")
dt1_1 = dt1.replace(tzinfo=tz1)
ts1 = dt1.timestamp()
ts1_1 = dt1_1.timestamp()

dt2 = dt1.astimezone(tz2)
dt2_1 = dt1_1.astimezone(tz2)
ts2 = dt2.timestamp()
ts2_1 = dt2_1.timestamp()

dt3 = datetime.datetime.fromtimestamp(ts2, tz1)
dt3_1 = datetime.datetime.utcfromtimestamp(ts2)
dt3_2 = dt3_1.replace(tzinfo=tz.gettz('UTC'))
dt4 = dt3.astimezone(tz1)
dt4_1 = dt3_1.astimezone(tz1)
dt4_2 = dt3_2.astimezone(tz1)

str = dt1_1.strftime("%Y%m%d %H%M%S")
print("end")
"""


#file_dir = r"C:\Users\Yang\Desktop\IMG_20180618_114344R.jpg"
#exif_in_file = piexif.load(file_dir)
#print(exif_in_file)

#[dirname,filename]=os.path.split('/Users/liuxiaolong/PycharmProjects/untitled/sw724.vaps')
#print(dirname,"\n",filename)


"""
#timeZone = '+07:00'
timeZoneShift = +7
#print(timeZoneShift)

timeString_Organized_M = "19700101 090000"
timeStructure = time.strptime(timeString_Organized_M, "%Y%m%d %H%M%S")
timeStamp = time.mktime(timeStructure)
#timeStamp = time.mktime(timeStructure) - time.timezone - timeZoneShift * 60 * 60  # mktime()只拿本地时间倒推。。。所以。。

timeStructure1 = time.strptime(timeString_Organized_M + ' +02:00', "%Y%m%d %H%M%S %z")
timeStamp1 = time.mktime(timeStructure1)

print(timeStamp)

timeString_FromTimeStamp_UTC = time.strftime('IMG_%Y%m%d_%H%M%S', time.gmtime(timeStamp))
print("timeString_FromTimeStamp_UTC: " + timeString_FromTimeStamp_UTC)

timeString_FromTimeStamp_Local = time.strftime('IMG_%Y%m%d_%H%M%S', time.localtime(timeStamp))
print("timeString_FromTimeStamp_Local: " + timeString_FromTimeStamp_Local)

timeStructure_FromTimeStamp_Timezone = time.gmtime(timeStamp + timeZoneShift * 60 * 60)  # 其实是取巧，结构本身的时区还是指向UTC的！！！
timeString_FromTimeStamp_Timezone = time.strftime('IMG_%Y%m%d_%H%M%S', time.gmtime(timeStamp + timeZoneShift * 60 * 60))
print("timeString_FromTimeStamp_Timezone: " + timeString_FromTimeStamp_Timezone)

"""
