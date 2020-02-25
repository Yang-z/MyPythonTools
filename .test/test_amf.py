import os
from tkinter import filedialog
import pyamf
from pyamf import remoting as pyamf_remoting

with open(filedialog.askopenfilename(), 'rb') as f:
    content: bytes = f.read()
    try:
        decoded = pyamf_remoting.decode(content)
    except Exception as e:
        print(e)

    print("done!")
