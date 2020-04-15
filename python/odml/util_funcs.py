"""
Script file to test minor scriptlets
"""

import odml


def filter_func():
    """
    odml validation warnings filter function tests
    """
    doc = odml.Document()
    sec = odml.Section(parent=doc)
    prop = odml.Property(parent=sec)

    val = odml.validation.Validation(prop)
    _ = [curr for curr in val.errors if prop.id == curr.obj.id]
