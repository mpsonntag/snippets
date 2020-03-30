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
