import odml

doc = odml.Document()
sec = odml.Section(name="sec", type="sometype", parent=doc)

# -- Test set cardinality on Property init
# Test empty init
prop_card_none = odml.Property(name="prop_cardinality_empty", parent=sec)
assert prop_card_none.val_cardinality is None
print(prop_card_none.val_cardinality)

# Test single int max init
prop_card_max = odml.Property(name="prop_cardinality_max", val_cardinality=10, parent=sec)
assert prop_card_max.val_cardinality == (None, 10)
print(prop_card_max.val_cardinality)

# Test tuple init
prop_card_min = odml.Property(name="prop_cardinality_min", val_cardinality=(2, None), parent=sec)
assert prop_card_min.val_cardinality == (2, None)
print(prop_card_min.val_cardinality)

# -- Test Property cardinality re-assignment
prop = odml.Property(name="prop", val_cardinality=(None, 10), parent=sec)
assert prop.val_cardinality == (None, 10)
print(prop.val_cardinality)

# Test Property cardinality reset
for non_val in [None, "", [], ()]:
    prop.val_cardinality = non_val
    assert prop.val_cardinality is None
    print("Curr val '%s'" % prop.val_cardinality)
    prop.val_cardinality = 1

# Test Property cardinality single int max assignment
prop.val_cardinality = 10
assert prop.val_cardinality == (None, 10)
print(prop.val_cardinality)

# Test Property cardinality tuple max assignment
prop.val_cardinality = (None, 5)
assert prop.val_cardinality == (None, 5)
print(prop.val_cardinality)

# Test Property cardinality tupe min assignment
prop.val_cardinality = (5, None)
assert prop.val_cardinality == (5, None)
print(prop.val_cardinality)

# Test Property cardinality min/max assignment
prop.val_cardinality = (1, 5)
assert prop.val_cardinality == (1, 5)
print(prop.val_cardinality)

# -- Test Property cardinality assignment failures
try:
    prop.val_cardinality = "a"
except ValueError:
    print("String assignment failure")

try:
    prop.val_cardinality = -1
except ValueError:
    print("Negative integer assignment failure")

try:
    prop.val_cardinality = (1, "b")
except ValueError:
    print("Invalid tuple content assignment failure")

try:
    prop.val_cardinality = (1, 2, 3)
except ValueError:
    print("Invalid tuple type assignment failure")

try:
    prop.val_cardinality = (-1, 1)
except ValueError:
    print("Invalid tuple min integer assignment failure")

try:
    prop.val_cardinality = (1, -5)
except ValueError:
    print("Invalid tuple max integer assignment failure")

try:
    prop.val_cardinality = (5, 1)
except ValueError:
    print("Invalid tuple integer order assignment failure")


# -- Test saving and loading
# Test saving to and loading from an XML file
xname = "/home/sommer/Chaos/tmp/odml/prop_cardinality.xml"
odml.save(doc, xname)

xdoc = odml.load(xname)
xprop = xdoc.sections["sec"].properties["prop_cardinality_empty"]
assert xprop.val_cardinality is None
print(xprop.val_cardinality)

xprop = xdoc.sections["sec"].properties["prop_cardinality_max"]
assert xprop.val_cardinality == (None, 10)
print(xprop.val_cardinality)

xprop = xdoc.sections["sec"].properties["prop_cardinality_min"]
assert xprop.val_cardinality == (2, None)
print(xprop.val_cardinality)

xprop = xdoc.sections["sec"].properties["prop"]
assert xprop.val_cardinality == (1, 5)
print(xprop.val_cardinality)

# Test saving to and loading from a JSON file
jname = "/home/sommer/Chaos/tmp/odml/prop_cardinality.json"
odml.save(doc, jname, "JSON")
jdoc = odml.load(jname, "JSON")

jprop = jdoc.sections["sec"].properties["prop_cardinality_empty"]
assert jprop.val_cardinality is None
print(jprop.val_cardinality)

jprop = jdoc.sections["sec"].properties["prop_cardinality_max"]
assert jprop.val_cardinality == (None, 10)
print(jprop.val_cardinality)

jprop = jdoc.sections["sec"].properties["prop_cardinality_min"]
assert jprop.val_cardinality == (2, None)
print(jprop.val_cardinality)

jprop = jdoc.sections["sec"].properties["prop"]
assert jprop.val_cardinality == (1, 5)
print(jprop.val_cardinality)


# Test saving to and loading from a YAML file
yname = "/home/sommer/Chaos/tmp/odml/prop_cardinality.yaml"
odml.save(doc, yname, "YAML")
ydoc = odml.load(yname, "YAML")

yprop = ydoc.sections["sec"].properties["prop_cardinality_empty"]
assert yprop.val_cardinality is None
print(yprop.val_cardinality)

yprop = ydoc.sections["sec"].properties["prop_cardinality_max"]
assert yprop.val_cardinality == (None, 10)
print(yprop.val_cardinality)

yprop = ydoc.sections["sec"].properties["prop_cardinality_min"]
assert yprop.val_cardinality == (2, None)
print(yprop.val_cardinality)

yprop = ydoc.sections["sec"].properties["prop"]
assert yprop.val_cardinality == (1, 5)
print(yprop.val_cardinality)


# -- Test assignment validation warnings
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import odml

# Redirect stdout to test messages
capture = StringIO()
sys.stdout = capture


def _get_captured_output(buff):
    out = [txt.strip() for txt in buff.getvalue().split('\n') if txt]
    capture.seek(0)
    capture.truncate()

    return out


doc = odml.Document()
sec = odml.Section(name="sec", type="type", parent=doc)

# -- Test cardinality validation warnings on Property init
# Test warning when setting invalid minimum
prop_card_min = odml.Property(name="prop_card_min", values=[1],
                              val_cardinality=(2, None), parent=sec)
# add assert minimum validation warning
out_a = _get_captured_output(capture)

# Test warning when setting invalid maximum
prop_card_max = odml.Property(name="prop_card_max", values=[1, 2, 3],
                              val_cardinality=2, parent=sec)
# add assert maximum validation warning
out_b = _get_captured_output(capture)

# Reset stdout
sys.stdout = sys.__stdout__

print(out_a)
print(out_b)


# Test no warning on valid init
prop_card = odml.Property(name="prop_card", values=[1, 2],
                          val_cardinality=(1, 5), parent=sec)

# -- Test cardinality validation warnings on cardinality updates
# Test warning when setting minimally required values cardinality
prop_card.val_cardinality = (3, None)
# add assert minimum validation warning

# Test warning when setting maximally required values cardinality
prop_card.values = [1, 2, 3]
prop_card.val_cardinality = 2
# add assert maximum validation warning

# Test no warning on valid cardinality
prop_card.val_cardinality = (1, 10)
# add assert validation empty

# Test no warning when setting cardinality to None
prop_card.val_cardinality = None
# add assert validation empty

# -- Test cardinality validation warnings on values updates
# Test warning when violating minimally required values cardinality
prop_card.val_cardinality = (3, None)
prop_card.values = [1, 2]
# add assert minimum validation warning

# Test warning when violating maximally required values cardinality
prop_card.val_cardinality = (None, 2)
prop_card.values = [1, 2, 3]
# add assert maximum validation warning

# Test no warning when setting correct number of values
prop_card.values = [1, 2]
# add assert validation empty

# Test no warning when setting values to None
prop_card.values = None
# add assert validation empty