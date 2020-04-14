import os
import tempfile

from odml import terminology


terminology.load(terminology.REPOSITORY)

cache_dir = os.path.join(tempfile.gettempdir(), "odml.cache")

orig_map = {}
for fname in os.listdir(cache_dir):
    spn = fname.split('.')
    fn_mtime = os.path.getmtime(os.path.join(cache_dir, fname))
    orig_map[spn[1]] = [spn[0], fn_mtime]

print(orig_map)

refresh_map = {}
