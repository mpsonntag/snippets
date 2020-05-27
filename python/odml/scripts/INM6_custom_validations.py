import odml

from odml.validation import IssueID, LABEL_WARNING, Validation, ValidationError


def check_left_right(obj):
    validation_id = IssueID.custom_validation

    if obj.name in ["Hemisphere", "ActiveHand"] and (not len(obj.values) == 1 or
                                                     obj.values[0] not in ["right", "left"]):

        msg = "Invalid '%s' value: %s" % (obj.name, obj.values)
        yield ValidationError(obj, msg, LABEL_WARNING, validation_id)
