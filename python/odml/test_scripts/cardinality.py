import odml

doc = odml.Document()
sec = odml.Section(name="sec", parent=doc)
prop = odml.Property(name="prop", val_cardinality=10, parent=sec)
