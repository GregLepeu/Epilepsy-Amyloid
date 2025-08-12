import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"

file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name)

df_epi = df[['CLM_id_subject','IPP']]

df.to_csv(path+file_name)
df_epi.to_csv(path+'Patients_list.csv')
a=1