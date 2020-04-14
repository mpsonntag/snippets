"""
Script testing odml cache refresh
"""

import os
import tempfile

from glob import glob


from odml import save, Document, Section
from odml import terminology


def current_cache_files_map(file_filter="*"):
    """
    Returns a dict mapping the basefilenames of cached odml files
    to their md5 hash and mtime.

    :param file_filter: a valid glob to search for files in the odml cache directory.
                        The cache directory is provided and must not be part of the glob.
                        Default value is '*'.

    :return: dict of the format {filename: [md5_hash, mtime]}
    """
    cache_dir = os.path.join(tempfile.gettempdir(), "odml.cache", file_filter)

    curr_map = {}
    for fnm in glob(cache_dir):
        spn = fnm.split('.')
        fn_mtime = os.path.getmtime(os.path.join(cache_dir, fnm))
        curr_map[spn[1]] = [spn[0], fn_mtime]

    return curr_map


def main():
    terminology.load(terminology.REPOSITORY)

    # Fetch current cache content
    orig_map = current_cache_files_map()

    # Test cache content does not change
    terminology.load(terminology.REPOSITORY)
    load_map = current_cache_files_map()

    assert len(orig_map) == len(load_map)
    for curr_file in orig_map:
        assert curr_file in load_map
        assert orig_map[curr_file] == load_map[curr_file]

    # Test refresh loads same cached files but changes them.
    # Different mtimes and id strings are sufficient.
    terminology.refresh(terminology.REPOSITORY)
    refresh_map = current_cache_files_map()
    assert len(orig_map) == len(refresh_map)
    for curr_file in orig_map:
        assert curr_file in refresh_map
        # Check different id
        assert orig_map[curr_file][0] == refresh_map[curr_file][0]
        # Check different mtime
        assert orig_map[curr_file][1] < refresh_map[curr_file][1]


if __name__ == "__main__":
    main()
