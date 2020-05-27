import odml

from odml.validation import IssueID, LABEL_WARNING, Validation, ValidationError


def check_left_right(obj):
    validation_id = IssueID.custom_validation

    if obj.name in ["Hemisphere", "ActiveHand"] and (not len(obj.values) == 1 or
                                                     obj.values[0] not in ["right", "left"]):

        msg = "Invalid '%s' value: %s" % (obj.name, obj.values)
        yield ValidationError(obj, msg, LABEL_WARNING, validation_id)


def verify_hand_hemisphere_prop(obj):
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
