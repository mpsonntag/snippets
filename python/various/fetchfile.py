import subprocess
import time

from os.path import splitext

offset = 0
file_name_base = "11_"

infile = "linklist.md"
with open(infile, encoding="utf8") as openfile:
    while line := openfile.readline():
        line = line.strip()
        offset += 1
        if not (offset % 10) % 5:
            time.sleep(7)
        else:
            time.sleep(offset % 5)
        _, curr_ext = splitext(line)
        curr_file_name = f"{file_name_base}{offset:04}{curr_ext}"
        print(f"Fetching {curr_file_name}: {line}")
        subprocess.run(["curl", line, "-o", curr_file_name], check=False)
