import piexif

while 1:
    fo = input("Original file: ")
    ft = input("Target file: ")
    if fo != "" and ft != "":
        piexif.transplant(fo, ft)
