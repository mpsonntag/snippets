import os

import odml

out_dir = "/home/msonntag/Chaos/DL/tmp/tuples"
f_name = "tuple_test"
f_path = os.path.join(out_dir, f_name)

tuple_values = ["(1; 2)", "(3; 4)", "(5; 6)"]

# test saving odml style tuples
tst = "tuple_test"

doc = odml.Document()
sec = doc.create_section(name=tst)
tuple_prop = sec.create_property(name=tst, dtype="2-tuple")
tuple_prop.values = tuple_values
list_prop = sec.create_property(name="list")
list_prop.values = [1, 2, 3, 4, 5]

# check XML
odml.save(doc, f_path)
x_check = odml.load("%s.xml" % f_path)
assert len(x_check.sections[tst].properties[tst].values) == len(tuple_values)
assert len(x_check.sections[tst].properties[tst].values) == \
       len(doc.sections[tst].properties[tst].values)

# check JSON
odml.save(doc, f_path, 'JSON')
j_check = odml.load("%s.JSON" % f_path, 'JSON')
assert len(j_check.sections[tst].properties[tst].values) == len(tuple_values)
assert len(j_check.sections[tst].properties[tst].values) == \
       len(doc.sections[tst].properties[tst].values)

# check YAML
odml.save(doc, f_path, 'YAML')
y_check = odml.load("%s.YAML" % f_path, 'YAMl')
assert len(y_check.sections[tst].properties[tst].values) == len(tuple_values)
assert len(y_check.sections[tst].properties[tst].values) == \
       len(doc.sections[tst].properties[tst].values)


# test saving lists of odml style tuples
fname = "tuple_direct_test.xml"
fpath = os.path.join(out_dir, fname)

tdoc = odml.Document()
tsec = tdoc.create_section(name="tuple_test")
tprop = odml.Property(name="tuple_test", dtype="2-tuple",
                      values=tuple_values, parent=tsec)

odml.save(doc, fpath)
check_doc = odml.load(fpath)
assert len(check_doc.sections[0].properties[0].values) == len(tuple_values)

