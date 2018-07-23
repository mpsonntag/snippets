import nixio

if __name__ == '__main__':
    filename = "/home/msonntag/Chaos/DL/nix/bla.h5"
    print("Writing file '%s'" % filename)

    nf = nixio.File(filename, nixio.FileMode.Overwrite)

    sec = nf.create_section(name="sec", type_="type")

    secref = "sec ref"
    sec.reference = secref

    pname = "prop"
    prop = sec.create_property(name=pname, values=[nixio.Value("")])

    prop_ucty = 5
    prop.uncertainty = prop_ucty
    try:
        prop.uncertainty = "bla"
    except TypeError:
        print("Uncertainty string check works")

    prop_ref = "I AM AN OBSCURE REFERENCE"
    prop.reference = prop_ref

    prop_vorg = "I come from over there"
    prop.value_origin = prop_vorg

    prop_dep = "dependency"
    prop.dependency = prop_dep

    prop_depval = "dependency_val"
    prop.dependency_value = prop_depval

    nf.close()

    bla = nixio.File.open(filename)

    assert bla.sections[0].reference == secref
    print("Read sec reference: %s" % bla.sections[0].reference)

    assert bla.sections[0].props[pname].uncertainty == prop_ucty
    print("Read prop uncertainty: %s" % bla.sections[0].props[pname].uncertainty)
    assert bla.sections[0].props[pname].reference == prop_ref
    print("Read prop reference: %s" % bla.sections[0].props[pname].reference)
    assert bla.sections[0].props[pname].value_origin == prop_vorg
    print("Read prop val origin %s" % bla.sections[0].props[pname].value_origin)
    assert bla.sections[0].props[pname].dependency == prop_dep
    print("Read prop val dep %s" % bla.sections[0].props[pname].dependency)
    assert bla.sections[0].props[pname].dependency_value == prop_depval
    print("Read prop dep val %s" % bla.sections[0].props[pname].dependency_value)

    bla.close()
