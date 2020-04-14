"""
Script testing odml cache refresh
"""

import os
import tempfile

from glob import glob

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

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


def refresh_terminology(refresh_url, file_filter="*"):
    terminology.load(refresh_url)

    # Fetch current cache content
    orig_map = current_cache_files_map(file_filter)

    # Test cache content does not change
    terminology.load(refresh_url)
    load_map = current_cache_files_map(file_filter)

    assert len(orig_map) == len(load_map)
    for curr_file in orig_map:
        assert curr_file in load_map
        assert orig_map[curr_file] == load_map[curr_file]

    # Test refresh loads same cached files but changes them.
    # Different mtimes and id strings are sufficient.
    terminology.refresh(refresh_url)
    refresh_map = current_cache_files_map(file_filter)
    assert len(orig_map) == len(refresh_map)
    for curr_file in orig_map:
        assert curr_file in refresh_map
        # Check different id
        assert orig_map[curr_file][0] == refresh_map[curr_file][0]
        # Check different mtime
        assert orig_map[curr_file][1] < refresh_map[curr_file][1]


def refresh_odml_terminology():
    refresh_terminology(terminology.REPOSITORY)


def refresh_local_terminology():
    tmp_dir = tempfile.mkdtemp("_odml")
    print("Using temp directory '%s'" % tmp_dir)
    tmp_name = os.path.basename(tmp_dir)

    main_name = "%s_main.xml" % tmp_name
    main_file = os.path.join(tmp_dir, main_name)
    main_url = "file://%s" % pathname2url(main_file)

    include_name = "%s_include.xml" % tmp_name
    include_file = os.path.join(tmp_dir, include_name)
    include_url = "file://%s" % pathname2url(include_file)

    include_doc = Document()
    _ = Section(name="include_sec", type="test", parent=include_doc)
    save(include_doc, include_file)

    main_doc = Document()
    _ = Section(name="main_sec", type="test", include=include_url, parent=main_doc)
    save(main_doc, main_file)

    file_filter = "*%s*" % tmp_name
    refresh_terminology(main_url, file_filter)


def main():
    refresh_local_terminology()


if __name__ == "__main__":
    main()
