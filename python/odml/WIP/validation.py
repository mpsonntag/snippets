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
sec_count = 0
prop_count = 0
obj_valid_map = {}
valid_obj_map = {}

for i in val.errors:
    vid = i.validation_id
    if i.is_error:
        errors.append(i)
    else:
        warnings.append(i)

    if i.obj not in reduce and 'section' in str(i.obj).lower():
        sec_count += 1
    elif i.obj not in reduce and 'property' in str(i.obj).lower():
        prop_count += 1
    reduce.add(i.obj)

    if i.obj in obj_valid_map:
        obj_valid_map[i.obj].append(vid)
    else:
        obj_valid_map[i.obj] = [vid]
    if vid in valid_obj_map:
        valid_obj_map[vid].append(i.obj)
    else:
        valid_obj_map[vid] = [i.obj]

msg = "Validation found %s errors and %s warnings" % (len(errors), len(warnings))
msg += " in %s Sections and %s Properties." % (sec_count, prop_count)
msg += "\nRun 'odml.Validation' for details and to resolve the issues."

print(msg)
