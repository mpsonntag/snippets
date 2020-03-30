import odml

doc = odml.Document()
sec = odml.Section(name="sec", parent=doc)

# -- Test set cardinality on Property init
# Test empty init
prop_card_none = odml.Property(name="prop_cardinality_empty", parent=sec)
assert prop_card_none.val_cardinality is None
prop_card_none.val_cardinality

# Test single int max init
prop_card_max = odml.Property(name="prop_cardinality_max", val_cardinality=10, parent=sec)
assert prop_card_max.val_cardinality == (None, 10)
prop_card_max.val_cardinality

# Test tuple init
prop_card_min = odml.Property(name="prop_cardinality_min", val_cardinality=(2, None), parent=sec)
assert prop_card_min.val_cardinality == (2, None)
prop_card_min.val_cardinality

# -- Test Property cardinality re-assignment
prop = odml.Property(name="prop", val_cardinality=(None, 10), parent=sec)
assert prop.val_cardinality == (None, 10)
prop.val_cardinality

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
