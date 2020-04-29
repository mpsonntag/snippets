import odml


def print_val(rank, curr):
    # Cleanup the odml object print strings
    print_str = str(curr).split()[0].split("[")[0].split(":")[0]
    # Document has no name attribute and should not print id or name info
    if hasattr(curr, "name"):
        if curr.name and curr.name != curr.id:
            print_str = "%s[%s]" % (print_str, curr.name)
        else:
            print_str = "%s[%s]" % (print_str, curr.id)
    print("Validation%s: %s '%s'" % (rank.capitalize(), print_str, "some err message"))


doc = odml.Document()
sec = odml.Section(parent=doc)
_ = odml.Section(parent=sec)
_ = odml.Section(parent=sec)
subsec = odml.Section(parent=sec)

prop = odml.Property(parent=sec)

subprop = odml.Property(parent=subsec)

val = odml.validation.Validation(doc)

errors = list()
warnings = list()
reduce = set()
obj_valid_map = {}
valid_obj_map = {}
secs = list()
props = list()

for i in val.errors:
    vid = i.validation_id
    if i.is_error:
        errors.append(i)
    else:
        warnings.append(i)

    reduce.add(i.obj)

    if i.obj in obj_valid_map:
        obj_valid_map[i.obj].append(vid)
    else:
        obj_valid_map[i.obj] = [vid]
    if vid in valid_obj_map:
        valid_obj_map[vid].append(i.obj)
    else:
        valid_obj_map[vid] = [i.obj]
