## Matches patients and controls according age and gender
# a

#%%
# import modules

import subject_match_class
import importlib
importlib.reload(subject_match_class)
import json
from pprint import pprint
import numpy as np
import pandas as pd
import os


#%%
## read in hypnograms again as a dictionary, actually we just require the demographics
output_dir ='/media/dagi/DATA/somnonetz/parasomnia/ms/RESULTS'
with open(os.path.join(output_dir,'ms-sleepstages-all.json'), 'r') as f:
    patients = json.load(f)

#%%
patients_df = pd.DataFrame(patients).transpose()
patients_df = patients_df[['subjectID','age','gender']]
patients_df.head()
#%%
## read in siesta data
siesta_dir ='/home/dagi/NC-HTW/PROJECTS/SOMNONETZ/sn-tds/RESULTS_CSV'
controls = pd.read_csv(os.path.join(siesta_dir,'siesta_all_consent.csv'), low_memory=False, skipinitialspace=True)
# remove trailing blanks
controls.columns = controls.columns.str.lstrip()
# rename column sex > gender
controls.rename({'sex': 'gender'}, axis=1, inplace=True)

#%%
controls_df = controls.query('status == "healthy" & night == 2')
controls_df = controls_df[['subjectID','age','gender']]
controls_df.shape

#%%
# convert dictionary to dataframe. Is a nested dict, therefore not so easy
# pprint
controls_df.head()


#%%
controls_df.head()
#print(controls_df['sex'][1])


#%%
results = subject_match_class.SubjectMatch(patients_df,controls_df)

#%%
subject_matching = results.matching
#%%
subject_matching.head()
#%%
# write in file
subject_matching.to_csv(os.path.join(output_dir,'subject_matches.csv'))

#%%
# def default(o):
#     if isinstance(o, np.int64): return int(o)
#     raise TypeError
#
# with open(os.path.join(output_dir,'ms-sleepparams-all.json'), 'w') as f:
#     json.dump(sleep_parameters, f, default=default)


