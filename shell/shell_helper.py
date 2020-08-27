from tkinter import filedialog


def file_or_dir(title=None):
    if(title): print(title)

    t = input(
'''file or directory: 
f) file (default)
d) directory
f/d> '''
    )
    
    if(t == '' or t == 'f'):
        path = filedialog.askopenfilename(title=title)
    elif(t == 'd'):
        path = filedialog.askdirectory(title=title)
    else:
        print("a a ...")
        return file_or_dir(title=title)
    
    print("path> " + path)
    return path

def yes_or_no(title=None, default=True):
    if(title): print(title)

    print(
'''yes or no: 
y) yes
n) no'''
    )

    if default:
        print("default (yes)")
    else:
        print("default (no)")

    i = input("y/n> ")

    if(i == ''):
        return default
    if(i == 'y'):
        return True
    elif(i == 'n'):
        return False
    else:
        print("a a ...")
        return yes_or_no(default=default)

def choose_one(title=None, options=[], default=0, should_return_index=False):
    if title: print(title)
    for i in range(0, len(options)):
        is_default = "(default)" if i == default else ""
        print(f"{i}) {options[i]} {is_default}")
    choice = input("choose an option> ")
    c = default if choice == '' else int(choice)
    if c in range(0, len(options)):
        return c if should_return_index else options[c]
    else:
        print("a a ...")
        return choose_one(title, options, default, should_return_index)

     

if __name__ == "__main__":
    # file_or_dir(title="open")
    # print(yes_or_no(title="R U OK?", default=False))
    print(
        choose_one(
            "options:",
            [
                "zero",
                "one",
                'two',
                'three'
            ],
            0
        )
    )
