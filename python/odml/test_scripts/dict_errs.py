import os
import tempfile

import odml


def fill_up_drive(file_content):
    temp_dir = tempfile.gettempdir()
    tmp_dir_path = os.path.join(temp_dir, "odml_test")
    if not os.path.exists(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    f_name = "test.yaml"
    file_path = os.path.join(tmp_dir_path, f_name)

    with open(file_path, "w") as dump_file:
        dump_file.write(file_content)

    return file_path


def tidy_up(file_path):
    temp_dir_path = os.path.dirname(file_path)
    print("Removing file '%s'" % file_path)
    os.remove(file_path)
    print("Removing temporary directory '%s'" % temp_dir_path)
    os.rmdir(temp_dir_path)


def get_invalid_attribute_content():
    return """Document:
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


cleanup_dir = False

content = """
Document:
  id: cb64006a-1440-442a-9b53-edfa66f97191
  sections:
  - id: 83e9b569-40f2-4174-876a-7f49cea79c0a
    name: 83e9b569-40f2-4174-876a-7f49cea79c0a
    properties:
    - id: 4a5ae765-70d4-4f61-987d-ac766ef1797c
      name: 4a5ae765-70d4-4f61-987d-ac766ef1797c
      type: int
      value:
      - eins
      - zwei
      - drei
      - vier
    sections: []
    type: n.s.
odml-version: '1.1'
"""

f_path = fill_up_drive(get_invalid_attribute_content())

try:
    l_doc = odml.load(f_path, "YAML")
except Exception as exc:
    if cleanup_dir:
        tidy_up(f_path)

    raise exc

if cleanup_dir:
    tidy_up(f_path)
