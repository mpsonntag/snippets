import pandas as pd

fn = "/Users/michi/Chaos/work/_Lab_Zimmer/calcium_imaging/results/N2/urx/shift210421/20120705Pflp178GCaMP5kshift210421W7URXx2.log"

# row_wise read in of csv file
data = pd.read_csv(fn)

# transpose to get columns
tdata = data.transpose()

# get first column as array
col = tdata.values[0]
