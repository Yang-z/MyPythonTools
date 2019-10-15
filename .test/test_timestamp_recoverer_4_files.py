import re
import os, time

k1 = r"20181204 061530"
p1s = r"(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1]) ([0-1]\d|2[0-3])([0-5]\d){2}"
p1 = re.compile(p1s)
m1 = re.search(p1, k1)
print(m1.group(0))

k1 = r"mmexport1444352908196"
p1s = r"mmexport(\d{13})"
p1 = re.compile(p1s)
m1 = re.search(p1, k1)
print(m1.group(1))
ts = float(m1.group(1)) / 1000
print(time.strftime('%Y%m%d %H%M%S', time.localtime(ts)))

