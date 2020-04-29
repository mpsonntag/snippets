import odml

doc = odml.Document()
sec = odml.Section(parent=doc)
_ = odml.Section(parent=sec)
_ = odml.Section(parent=sec)
subsec = odml.Section(parent=sec)

prop = odml.Property(parent=sec)

subprop = odml.Property(parent=subsec)

val = odml.validation.Validation(doc)

rank = 'warning'
curr = sec


def print_val(rank, curr):
    disp = ""
    # Document has no name attribute and should not print id or name info
    if hasattr(curr, "name"):
        disp = "[%s]" % curr.id
        if curr.name and curr.name != curr.id:
            disp = "[%s]" % curr.name

    # Cleanup the odml object print strings
    obj_fmt = str(curr).split()[0].split("[")[0].split(":")[0]
    print("Validation%s: %s%s '%s'" % (rank.capitalize(), obj_fmt, disp, "some err message"))
