"""
Custom validations for the odML library, the validations
are specific for an INM6 use case. Check the tutorial on
python-odml.readthedocs.org for a general odml validation
introduction.

These validations require an odml library >= 1.5.0.
"""

import odml

from odml.validation import IssueID, LABEL_WARNING, Validation, ValidationError


def check_left_right(obj):
    """
    Checks if a Property with the name "Hemisphere" or "ActiveHand"
    has a value length of 1 and contains only the value content
    of "right" or "left".

    :param obj: odml Property
    :return: Yields a ValidationError if the check fails.
    """
    validation_id = IssueID.custom_validation

    if obj.name in ["Hemisphere", "ActiveHand"] and (not len(obj.values) == 1 or
                                                     obj.values[0] not in ["right", "left"]):

        msg = "Invalid '%s' value: %s" % (obj.name, obj.values)
        yield ValidationError(obj, msg, LABEL_WARNING, validation_id)


def verify_hand_hemisphere_prop(obj):
    """
    Checks if the Properties with the name "Hemisphere" and "ActiveHand"
    each contain the opposing value of the other: "left"-"right" or
    "right"-"left" respectively.

    :param obj: odml Property

    :return: Yields a ValidationError if any of the required Properties
             cannot be found at its place in the tree or if the corresponding
             Property does not contain the required corresponding value.
    """
    validation_id = IssueID.custom_validation

    # path hemisphere: root/S[Subject]/S[ArrayImplant]/P[Hemisphere]
    hemisphere = "Hemisphere"
    # path active hand: root/S[Subject]/P[ActiveHand]
    active_hand = "ActiveHand"
    if obj.name in [hemisphere, active_hand]:
        other = None
        try:
            if obj.name == hemisphere:
                other = obj.parent.parent.properties[active_hand]
            elif obj.name == active_hand:
                other = obj.parent.sections["ArrayImplant"].properties[hemisphere]
        except KeyError:
            msg = "Invalid location of active hand/hemisphere property"
            yield ValidationError(obj, msg, LABEL_WARNING, validation_id)
            return

        invalid = False
        if not other or not obj.values or not other.values:
            invalid = True
        elif not obj.values[0] in ["left", "right"] or not other.values[0] in ["left", "right"]:
            invalid = True
        elif obj.values[0] == "right" and not other.values[0] == "left":
            invalid = True
        elif obj.values[0] == "left" and not other.values[0] == "right":
            invalid = True

        if invalid:
            msg = "Invalid active hand/hemisphere pair"
            yield ValidationError(obj, msg, LABEL_WARNING, validation_id)


def verify_hand_hemisphere_root(obj):
    """
    Checks if the Properties with the name "Hemisphere" and "ActiveHand"
    each contain the opposing value of the other: "left"-"right" or
    "right"-"left" respectively.

    :param obj: odml Document root

    :return: Yields a ValidationError if any of the required Properties
             cannot be found at its place in the tree or if the corresponding
             Property does not contain the required corresponding value.
    """
    validation_id = IssueID.custom_validation

    try:
        # path hemisphere: root/S[Subject]/S[ArrayImplant]/P[Hemisphere]
        hemisphere = obj.sections["Subject"].sections["ArrayImplant"].properties["Hemisphere"]
        # path active hand: root/S[Subject]/P[ActiveHand]
        active_hand = obj.sections["Subject"].properties["ActiveHand"]
    except KeyError:
        msg = "Invalid location of active hand or hemisphere property"
        yield ValidationError(obj, msg, LABEL_WARNING, validation_id)
        return

    invalid = False
    if not hemisphere or not hemisphere.values:
        invalid = True
    elif not active_hand or not active_hand.values:
        invalid = True
    elif not hemisphere.values[0] in ["left", "right"] or \
            not active_hand.values[0] in ["left", "right"]:
        invalid = True
    elif hemisphere.values[0] == "right" and not active_hand.values[0] == "left":
        invalid = True
    elif hemisphere.values[0] == "left" and not active_hand.values[0] == "right":
        invalid = True

    if invalid:
        msg = "Invalid active hand/hemisphere pair"
        yield ValidationError(obj, msg, LABEL_WARNING, validation_id)


# Create empty custom validation and add custom handler functions
Validation.register_handler("property", check_left_right)

# Edited versions of the original file i140703-001.odml
filename = "invalid_hand_hemisphere_entry_example_i140703-001.odml"
# filename = "invalid_hand_hemisphere_value_example_i140703-001.odml"
invalid_doc = odml.load(filename)
custom_validation = Validation(invalid_doc, validate=False, reset=True)
custom_validation.register_custom_handler("property", check_left_right)
custom_validation.register_custom_handler("property", verify_hand_hemisphere_prop)
custom_validation.register_custom_handler("odML", verify_hand_hemisphere_root)

# Run validation and print report
custom_validation.report()

# Print individual warnings and errors
for err in custom_validation.errors:
    print(err)
