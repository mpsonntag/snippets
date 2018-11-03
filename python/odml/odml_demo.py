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
prop.values = "Caenorhabditis elegans"

prop = odml.Property(name="Strains", parent=sec)
prop.values = ["N2", "CX9191"]

prop = odml.Property(name="genetic_modifications", parent=sec)
prop.values = "Pflp-8, Pflp-17::GCaMP5.k"

# adding base information where the data can be found
sec = odml.Section(name="data_repository", parent=doc)

prop = odml.Property(name="repoURI", parent=sec)
prop.values = "https://gin.g-node.org/mpsonntag/demo"


# adding information about experimental protocols
sec = odml.Section(name="protocols", parent=doc)

subsec = odml.Section(name="ramp1", type="oxygen_ramps", parent=sec)
prop = odml.Property(name="oxygen_concentrations", parent=subsec)
prop.values = [21, 4, 21]
prop.unit = "% O2"

prop = odml.Property(name="shifting_times", parent=subsec)
prop.values = [10, 10, 180, 180, 180, 60]
prop.unit = "s"

prop = odml.Property(name="description", parent=subsec)
prop.values = "Recording start in the first 10s, 10s at 21% oxygen, ramp down over 180s" \
              " until 4% oxygen have been reached, at 4% oxygen for 180s, increase of " \
              "oxygen for 180s until 21% oxygen have been reached, at 21% oxygen for 60s."

subsec = odml.Section(name="shift1", type="oxygen_shifts", parent=sec)
prop = odml.Property(name="oxygen_concentrations", parent=subsec)
prop.values = [21, 4, 21]
prop.unit = "% O2"

prop = odml.Property(name="shifting_times", parent=subsec)
prop.values = [110, 360, 150]
prop.unit = "s"

prop = odml.Property(name="description", parent=subsec)
prop.values = "Recording start at 21% oxygen, stays there for 110s after this a shift" \
              "to 4% oxygen. Stays at 4% oxygen for 360s. Shift to 21% oxygen, stays" \
              "at 21% oxygen for 150s."


sec = odml.Section(name="animal_conditions", parent=doc)
prop = odml.Property(name="conditions", parent=sec)
prop.values = ["well-fed", "starving"]

subsec = odml.Section(name="well-fed", parent=sec)
prop = odml.Property(name="description", parent=subsec)
prop.values = "Animals are picked from a bacterial lawn to an agar plate containing no" \
              "bacteria. The animals are used from immediately until maximum two after " \
              "they have been removed from a food source."

subsec = odml.Section(name="starving", parent=sec)
prop = odml.Property(name="description", parent=subsec)
prop.values = "Animals are picked from a bacterial lawn to an agar plate containing no" \
              "bacteria. The animals are used after they have been left on the plate" \
              "for 5 hours until a maximum of 7 hours after they have been removed from" \
              "a food source."

# add information about experiments
sec = odml.Section(name="experiments", parent=doc)

subsec = odml.Section(name="trial", type="ramp/ca-imaging", parent=sec)

prop = odml.Property(name="date", dtype=odml.dtypes.DType.date, parent=subsec)
prop.values = "2012-10-23"

prop = odml.Property(name="strain", parent=subsec)
prop.values = "N2"

prop = odml.Property(name="protocol", parent=subsec)
prop.value = "ramp1/oxygen_ramps"

prop = odml.Property(name="condition", parent=subsec)
prop.values = 90
prop.unit = 'minute'

prop = odml.Property(name="resting_time", parent=subsec)
prop.values = 5
prop.unit = "minute"

prop = odml.Property(name="tracked", parent=subsec)
prop.values = "URX"

prop = odml.Property(name="frames", parent=subsec)
prop.values = "6100"

prop = odml.Property(name="paralytic", parent=subsec)
prop.values = "Tetramisol"

prop = odml.Property(name="comment", parent=subsec)
prop.value = "reflector changer not none, nose not in correct position"

subsub = odml.Section(name="setup", type="hardware", parent=subsec)
prop = odml.Property(name="microscope 1", parent=subsub)
prop = odml.Property(name="EM_gain", parent=subsub)
prop.values = 1500
prop = odml.Property(name="LED_I", parent=subsub)
prop.values = 20
prop = odml.Property(name="gray_`filter", parent=subsub)
prop.values = 20
prop.unit = "%"
prop = odml.Property(name="exposure", parent=subsub)
prop.values = 100
prop.unit = "ms"



odml.save(doc, filename)

