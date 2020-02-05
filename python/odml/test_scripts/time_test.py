import datetime as dt
import os

import odml

from odml.tools import ODMLReader

# save load test
doc = odml.Document()
sec = odml.Section(name="sec_name", parent=doc)
time_string = "12:34:56"
time = dt.time(12, 34, 56)
val_in = time_string
vals_in = [None, "", time_string, time]
_ = odml.Property(name="time test single", dtype="time", value=val_in, parent=sec)
_ = odml.Property(name="time test", dtype="time", value=vals_in, parent=sec)

# string load test
author = "HPL"
date = "1890-08-20"
sec_name = "section name"
sec_type = "section type"
prop_name = "prop name"
prop_type = "time"
prop_value = "15:15:15"
string_doc = """
        odml-version: '1.1'
        Document:
            author: %s
            date: %s
            sections:
            - name: %s
              type: %s
              properties:
              - name: %s
              - type: %s
              - value:
                - %s
        """ % (author, date, sec_name, sec_type, prop_name, prop_type, prop_value)


out_dir = "/home/msonntag/Chaos/DL/tmp/odml"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

print("-- YAML tests ...")
y_name = "odmltestsave.YAML"
y_path = os.path.join(out_dir, y_name)

print("-- Saving YAML file ...")
odml.save(doc, y_path, "YAML")

print("-- Loading YAML file ...")
ydoc = odml.load(y_path, "YAML")
ydoc.pprint()

print("-- Loading YAML string ...")
yaml_test = ODMLReader("YAML").from_string(string_doc)
yaml_test.pprint()

print("-- JSON tests ...")
j_name = "odmltestsave.JSON"
j_path = os.path.join(out_dir, j_name)

print("-- Saving JSON file ...")
odml.save(doc, j_path, "JSON")

print("-- Loading JSON file ...")
jdoc = odml.load(j_path, "JSON")
jdoc.pprint()
