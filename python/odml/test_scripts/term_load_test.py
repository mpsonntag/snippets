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


# Fetch current cache content
orig_map = current_cache_files_map()

# Test cache content does not change
terminology.load(terminology.REPOSITORY)
load_map = current_cache_files_map()

assert(len(orig_map) == len(load_map))
for curr_file in orig_map:
    assert curr_file in load_map
    assert orig_map[curr_file] == load_map[curr_file]

# Test refresh loads same cached files but changes them.
# Different mtimes and id strings are sufficient.
terminology.refresh(terminology.REPOSITORY)
refresh_map = current_cache_files_map()
assert(len(orig_map) == len(refresh_map))
for curr_file in orig_map:
    assert curr_file in refresh_map
    # Check different id
    is_equ = orig_map[curr_file][1] == refresh_map[curr_file][1]
    print("%s, %s, %s, %s" % (curr_file, orig_map[curr_file][1], refresh_map[curr_file][1], is_equ))
    assert orig_map[curr_file][0] == refresh_map[curr_file][0]
    # Check different mtime
    assert orig_map[curr_file][1] < refresh_map[curr_file][1]
