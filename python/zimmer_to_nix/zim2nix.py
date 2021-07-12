import pandas as pd

head_col = ['curr_frame', 'time_elapsed', 'obj_substracted', 'substracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

data = pd.read_csv('20120705Pflp178GCaMP5kshift210421W8BAG.log',
                   header=None, names=head_col)

