import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND"

file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_epi = pd.read_csv(path+'/data/'+file_name,encoding='ISO-8859-1')

# Create the a 'SNAP/AD' column based on the A, T and N status
df_epi['AD/Non-AD'] = df_epi.apply(lambda row: 'Non-AD' if row['ATN status'] == 'A-T+N-' or  row['ATN status'] == 'A-T-N+' or row['ATN status'] == 'A-T+N+' or row['ATN status'] == 'A-T-N-'else
                        'AD' if row['ATN status'] == 'A+T+N-' or row['ATN status'] == 'A+T+N+' else np.nan, axis=1)


a=1

df_epi.to_csv(path+'/data/'+file_name)