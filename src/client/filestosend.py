"""filelist = []
x = "Users/cenker/Documents/CS/cs492/try/readdocker.py"
y = "Users/cenker/Documents/CS/cs492/try/cenk.py"

def s_break(x):
    filelist.append(x)
    filelist.append(y)
    print(filelist[1])
    print(filelist[0])
    print(filelist)

s_break(x)"""

import os
filelist = []
x = "Users/cenker/Documents/CS/cs492/try/readdocker.py"
y = "Users/cenker/Documents/CS/cs492/try/cenk.py"
print(os.path.basename(y))
def s_break():
    filelist.append(x)
    filelist.append(y)
    print(filelist)

s_break() 