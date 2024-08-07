import subprocess
import time

from os.path import splitext

offset = 0
fn_base = "11_"
fn = "linklist.md"
with open(fn) as openfile:
    while line := openfile.readline():
        line = line.strip()
        offset+=1
        if not (offset % 10) % 5:
            time.sleep(7)        
        else:
            time.sleep(offset % 5)
        _, currext = splitext(line)
        currfn = f"{fn_base}{offset:04}{currext}"
        print(f"Fetching {currfn}: {line}")
        subprocess.run(["curl", line, "-o", currfn])
