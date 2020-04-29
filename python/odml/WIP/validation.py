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
    if hasattr(curr, "name"):
        disp = "[id=%s]" % curr.id
        if curr.name and curr.name != curr.id:
            disp = "[name=%s]" % curr.name

    obj_fmt = str(curr).split()[0].split("[")[0]
    print("Validation%s: %s%s '%s'" % (rank.capitalize(), obj_fmt, disp, "some err message"))
