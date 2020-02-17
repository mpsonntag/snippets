import os

import odml

out_dir = "/home/msonntag/Chaos/DL/tmp/tuples"
fname = "tuple_test.xml"
fpath = os.path.join(out_dir, fname)

tuple_values = ["(1; 2)", "(3; 4)", "(5; 6)"]

# test saving odml style tuples
doc = odml.Document()
sec = doc.create_section(name="tuple_test")
tuple_prop = sec.create_property(name="tuple_test", dtype="2-tuple")
tuple_prop.values = tuple_values
list_prop = sec.create_property(name="list")
list_prop.values = [1, 2, 3, 4, 5]

odml.save(doc, fpath)

check = odml.load(fpath)

# test saving lists of odml style tuples
fname = "tuple_direct_test.xml"
fpath = os.path.join(out_dir, fname)

tdoc = odml.Document()
tsec = tdoc.create_section(name="tuple_test")
tprop = odml.Property(name="tuple_test", dtype="2-tuple",
                      values=tuple_values, parent=tsec)

odml.save(doc, fpath)
check_doc = odml.load(fpath)
