"""
Test validations of odml cardinality feat
"""


def section_properties_cardinality_validation():
    import odml

    validate = odml.validation.Validation
    msg_base = "Section properties cardinality violated"

    doc = odml.Document()
    # Test no caught warning on empty cardinality
    sec = odml.Section(name="prop_empty_cardinality", type="test", parent=doc)
    # Check that the current section did not throw any properties cardinality warnings
    for err in validate(doc).errors:
        print("msg: %s" % err.msg)
        if err.obj.id == sec.id:
            print("Message not found: %s" % (msg_base not in err.msg))
            assert msg_base not in err.msg

    # Test no warning on valid cardinality
    sec = odml.Section(name="prop_valid_cardinality", prop_cardinality=(1, 2), parent=doc)
    _ = odml.Property(parent=sec)
    for err in validate(doc).errors:
        print(err.msg)
        if err.obj.id == sec.id:
            print("Message not found: %s" % (msg_base not in err.msg))
            assert msg_base not in err.msg

    # Test maximum value cardinality validation
    test_range = 3
    test_card = 2
    sec = odml.Section(name="prop_invalid_max_val", prop_cardinality=test_card, parent=doc)
    for _ in range(test_range):
        _ = odml.Property(parent=sec)

    test_msg = "%s (maximum %s values, %s found)" % (msg_base, test_card, len(sec.properties))

    for err in validate(doc).errors:
        if err.obj.id == sec.id and msg_base in err.msg:
            print("Found it: %s" % err.msg)
            assert not err.is_error
            assert test_msg in err.msg

    # Test minimum value cardinality validation
    test_card = (4, None)

    sec = odml.Section(name="prop_invalid_min_val", prop_cardinality=test_card, parent=sec)
    _ = odml.Property(parent=sec)

    test_msg = "%s (minimum %s values, %s found)" % (msg_base, test_card[0],
                                                     len(sec.properties))

    for err in validate(doc).errors:
        if err.obj.id == sec.id and msg_base in err.msg:
            print("Found it: %s" % err.msg)
            assert not err.is_error
            assert test_msg in err.msg


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
