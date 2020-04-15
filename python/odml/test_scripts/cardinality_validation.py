"""
Test validations of odml cardinality feat
"""


def property_values_cardinality_validation():
    import odml

    from odml.validation import Validation

    doc = odml.Document()
    sec = odml.Section(name="sec", type="test", parent=doc)

    # Test no caught warning on empty cardinality
    prop = odml.Property(name="prop_empty_cardinality", values=[1, 2, 3, 4], parent=sec)
    valid = Validation(doc)
    print(valid.errors)

    for err in valid.errors:
        assert not err.obj.id == prop.id

    # Test no warning on valid cardinality
    prop = odml.Property(name="prop_valid_cardinality", values=[1, 2, 3, 4],
                         val_cardinality=(2, 10), parent=sec)
    valid = Validation(doc)
    print(valid.errors)

    for err in valid.errors:
        assert not err.obj.id == prop.id

    # Test minimum value cardinality validation
    test_val = [1, 2, 3]
    test_card = 2

    prop = odml.Property(name="prop_invalid_max_val", values=test_val,
                         val_cardinality=test_card, parent=sec)
    valid = Validation(doc)
    print(valid.errors)

    test_msg_base = "Property values cardinality violated"
    test_msg = "%s (maximum %s values, %s found)" % (test_msg_base, test_card, len(prop.values))
    for err in valid.errors:
        if err.obj.id == prop.id:
            assert not err.is_error and err.msg == test_msg

    # Test maximum value cardinality validation
    test_val = "I am a nice text to test"
    test_card = (4, None)

    prop = odml.Property(name="prop_invalid_min_val", values=test_val,
                         val_cardinality=test_card, parent=sec)
    valid = Validation(doc)
    print(valid.errors)

    test_msg = "%s (minimum %s values, %s found)" % (test_msg_base, test_card[0], len(prop.values))
    for err in valid.errors:
        if err.obj.id == prop.id:
            assert not err.is_error and err.msg == test_msg
