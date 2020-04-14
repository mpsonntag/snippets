import os
import tempfile

from odml import terminology


terminology.load(terminology.REPOSITORY)

cache_dir = os.path.join(tempfile.gettempdir(), "odml.cache")

for fname in os.listdir(cache_dir):
    print(fname)