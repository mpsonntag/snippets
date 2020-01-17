import odml

doc = odml.Document()
sec = doc.create_section(name="secname")
prop = sec.create_property(name="propname", value=["a", "b", "c"])

file_default = "/home/msonntag/Chaos/DL/odml_style_default.xml"
file_style_odml = "/home/msonntag/Chaos/DL/odml_style_odml.xml"


odml.tools.XMLWriter(doc).write_file(file_default)
odml.tools.XMLWriter(doc).write_file(file_style_odml, local_style=True)

