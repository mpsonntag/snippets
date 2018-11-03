from pathlib import Path

import odml

# create an empty document and save it
doc = odml.Document()

filename = str(Path.joinpath(Path.home(), 'Chaos', 'work', 'ginrepos', 'demo',
                             'elegans_oxygen.odml'))

odml.save(doc, filename)

# add some document information
doc.author = 'Michael Sonntag'
doc.date = '2018-11-04'
doc.version = '1.0'

# adding base information about the animals used in our experiment
sec = odml.Section(name="model_organism", parent=doc)
sec.definition = "Model organism used in the documented experiments"

prop = odml.Property(name="Species", parent=sec)
prop.values = "Caenorabdhitis elegans"

prop = odml.Property(name="Strain", parent=sec)
prop.values = "N2"

sec = odml.Section(name="data_repository", parent=doc)
prop = odml.Property(name="repoURI", parent=sec)
prop.values = "https://gin.g-node.org/mpsonntag/demo"

odml.save(doc, filename)

