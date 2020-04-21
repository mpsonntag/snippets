import os
import tempfile

import odml


def fill_up_drive():
    temp_dir = tempfile.gettempdir()
    tmp_dir_path = os.path.join(temp_dir, "odml_test")
    if not os.path.exists(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    f_name = "test.yaml"
    file_path = os.path.join(tmp_dir_path, f_name)

    # invalid yaml odml file content
    content = """
    Document:
      id: 82408bdb-1d9d-4fa9-b4dd-ad78831c797c
      invalid_doc_attr: i_do_not_exist_on_doc_level
      sections:
      - id: d4f3120a-c02f-4102-a9fe-2e8b77d1d0d2
        name: sec
        invalid_sec_attr: i_do_not_exist_on_sec_level
        properties:
        - id: 18ad5176-2b46-4a08-9b85-eafd6b14fab7
          name: prop
          value: []
          invalid_prop_attr: i_do_not_exist_on_prop_level
        sections: []
        type: n.s.
    odml-version: '1.1'
    """

    with open(file_path, "w") as dump_file:
        dump_file.write(content)

    return file_path


def tidy_up(file_path):
    temp_dir_path = os.path.dirname(file_path)
    print("Removing file '%s'" % file_path)
    os.remove(file_path)
    print("Removing temporary directory '%s'" % temp_dir_path)
    os.rmdir(temp_dir_path)


cleanup_dir = True
f_path = fill_up_drive()

try:
    l_doc = odml.load(f_path, "YAML")
except Exception as exc:
    if cleanup_dir:
        tidy_up(f_path)

    raise exc

if cleanup_dir:
    tidy_up(f_path)
