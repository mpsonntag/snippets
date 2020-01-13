import datetime as dt

import odml

from odml.tools import ODMLReader

doc = odml.Document()
sec = odml.Section(name="name", parent=doc)

time_string = '12:34:56'
time = dt.time(12, 34, 56)
val_in = time_string
vals_in = [None, "", time_string, time]
_ = odml.Property(name="time test single", dtype="time", value=val_in, parent=sec)
_ = odml.Property(name="time test", dtype="time", value=vals_in, parent=sec)

fname = '/home/msonntag/Chaos/DL/odmltestsave.YAML'
odml.save(doc, fname, 'YAML')

ydoc = odml.load(fname, 'YAML')


author = "HPL"
date = "1890-08-20"
sec_name = "section name"
sec_type = "section type"
prop_name = "prop name"
prop_type = "time"
prop_value = '15:15:15'
yaml_doc = """
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

test = ODMLReader('YAML').from_string(yaml_doc)
