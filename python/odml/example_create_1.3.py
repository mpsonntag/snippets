import odml
import os

wdir = "/home/msonntag/Chaos/work/x_odml/tmp"
fn_base = "1.3.3_example.%s"

doc = odml.Document(author="author", date="2018-02-02", version="v1.13",
                    repository="http://portal.g-node.org/odml/terminologies/v1.0/terminologies.xml")

sec1 = odml.Section(name="section one", type="mainsec", definition="def s1", reference="ref s1",
                    link="somewhere s1", include="url s1",
                    repository="http://portal.g-node.org/odml/terminologies/v1.0/analysis/power_spectrum.xml")
sec2 = odml.Section(name="section two", type="mainsec", definition="def s2", reference="ref s2", link="somewhere s2",
                    include="url s2", repository="repo s2")
sec3 = odml.Section(name="section three", type="mainsec", definition="def s3", reference="ref s3", link="somewhere s3",
                    include="url s3", repository="repo s3")

doc.append(sec1)
doc.append(sec2)
doc.append(sec3)

sec1 = odml.Section(name="subsection one", type="subsec", definition="def subs1", reference="ref subs1",
                    link="somewhere subs1", include="url subs1", repository="repo subs1")

doc.sections[0].append(sec1)

prop = odml.Property(name="prop one", value="", definition="def prop1",
                     dependency="dep p1", dependency_value="dep val p1")

prop = odml.Property(name="prop one", value="", definition="def prop1",
                     dependency="dep p1", dependency_value="dep val p1", parent=doc.sections[0])

prop = odml.Property(name="prop two", value="", definition="def prop2",
                     dependency="dep p2", dependency_value="dep val p2", parent=doc.sections[0])

prop = odml.Property(name="prop three", value="", definition="def prop3",
                     dependency="dep p3", dependency_value="dep val p3", parent=doc.sections[0])

prop = odml.Property(name="prop one", value="", definition="def prop1",
                     dependency="dep p1", dependency_value="dep val p1", parent=doc.sections[0].sections[0])

prop = odml.Property(name="prop three", value="", definition="def prop3",
                     dependency="dep p3", dependency_value="dep val p3", parent=doc.sections[0].sections[0])

prop = odml.Property(name="prop two", value="", definition="def prop2",
                     dependency="dep p2", dependency_value="dep val p2", parent=doc.sections[0].sections[0])

val = odml.Value(value=["1", "2", "3", "4", "5"], uncertainty=12, unit="arbitrary", dtype=odml.DType.string,
                 definition="def val 1", reference="ref val 1", filename="filename val 1",
                 encoder="enc val 1", comment="comment val 1")

doc.sections[0].properties[0].append(val)

val = odml.Value(value=1, uncertainty=12, unit="arbitrary", dtype=odml.DType.int, definition="def val 1",
                 reference="ref val 1", filename="filename val 1", encoder="enc val 1", comment="comment val 1")

doc.sections[0].properties[0].append(val)
doc.sections[0].properties[1].append(val)

val = odml.Value(value=2, uncertainty=12, unit="arbitrary", dtype=odml.DType.int, definition="def val 1",
                 reference="ref val 1", filename="filename val 1", encoder="enc val 1", comment="comment val 1")
doc.sections[0].properties[1].append(val)
val = odml.Value(value=3, uncertainty=12, unit="arbitrary", dtype=odml.DType.int, definition="def val 1",
                 reference="ref val 1", filename="filename val 1", encoder="enc val 1", comment="comment val 1")
doc.sections[0].properties[1].append(val)
val = odml.Value(value=4, uncertainty=12, unit="arbitrary", dtype=odml.DType.int, definition="def val 1",
                 reference="ref val 1", filename="filename val 1", encoder="enc val 1", comment="comment val 1")
doc.sections[0].properties[1].append(val)
doc.sections[0].properties[1].append(val)
doc.sections[0].properties[1].append(val)
doc.sections[0].properties[1].append(val)
doc.sections[0].properties[1].append(val)
doc.sections[0].sections[0].properties[1].append(val)
doc.sections[0].sections[0].properties[1].append(val)
doc.sections[0].sections[0].properties[1].append(val)
val = odml.Value(value=2, uncertainty=12, unit="arbitrary", dtype=odml.DType.int, definition="def val 1",
                 reference="ref val 1", filename="filename val 1", encoder="enc val 1", comment="comment val 1")
doc.sections[0].sections[0].properties[1].append(val)

odml.fileio.save(doc, os.path.join(wdir, (fn_base % "xml")))
odml.fileio.save(doc, os.path.join(wdir, (fn_base % "yaml")), "YAML")
odml.fileio.save(doc, os.path.join(wdir, (fn_base % "json")), "JSON")
