import os
from tkinter import filedialog
import pyamf
from pyamf import remoting as pyamf_remoting

with open(filedialog.askopenfilename(), 'rb') as f:
    content: bytes = f.read()
    decoded = pyamf_remoting.decode(content)  # ✔️
    decoded2 = pyamf.decode(f)  # ⚠️

    print("done!")
