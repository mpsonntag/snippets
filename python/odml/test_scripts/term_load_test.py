import os
import tempfile

from odml import terminology


terminology.load(terminology.REPOSITORY)

cache_dir = os.path.join(tempfile.gettempdir(), "odml.cache")


def current_cache_files_map():
    curr_map = {}
    for fnm in os.listdir(cache_dir):
        spn = fnm.split('.')
        fn_mtime = os.path.getmtime(os.path.join(cache_dir, fnm))
        curr_map[spn[1]] = [spn[0], fn_mtime]

    return curr_map


orig_map = current_cache_files_map()

# test cache does not change
terminology.load(terminology.REPOSITORY)

load_map = current_cache_files_map()

assert(len(orig_map) == len(load_map))
for curr_file in orig_map:
    assert curr_file in load_map
    assert orig_map[curr_file] == load_map[curr_file]
