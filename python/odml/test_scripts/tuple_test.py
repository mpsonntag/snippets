import os

import odml

out_dir = "/home/msonntag/Chaos/DL/tmp/tuples"
fname = "tuple_test"
fpath = os.path.join(out_dir, fname)

doc = odml.Document()
sec = doc.create_section(name="tuple_test")
prop = sec.create_property(name="tuple_test", dtype="2-tuple")
prop.values = ["(1; 2)", "(3; 4)", "(5; 6)"]
oprop = sec.create_property(name="list")
oprop.values = [1, 2, 3, 4, 5]

odml.save(doc, fpath)
