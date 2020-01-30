import os

import odmltools.importers.import_datacite as dimp


home = os.path.join(os.getenv("HOME"), "Chaos")
resources = os.path.join(home, "work/odmltools/test/resources/")
extra_fn = "invalidNS.xml"
extra_file = os.path.join(resources, extra_fn)
out_dir = os.path.join(home, "DL/tmp")

# test fail
dimp.handle_document(extra_file, out_dir)

# test ns escape
extra_nspace = ["http://datacite.org/schema/kernel-2"]
dimp.handle_document(extra_file, out_dir, extra_ns=extra_nspace)
