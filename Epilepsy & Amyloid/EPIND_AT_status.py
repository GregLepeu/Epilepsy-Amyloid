import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"

file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_epi = pd.read_csv(path+'/data/'+file_name,encoding='ISO-8859-1')

df_epi['Epi_not_ND'] = df_epi['Epi Soarian'] - df_epi['Epi ND']

# Create the 'AT status' column based on the A and T status
df_epi['AT status'] = df_epi.apply(lambda row: 'A-T-' if row['csf_AD_A'] == 0 and row['csf_AD_T'] == 0 else
                              'A+T-' if row['csf_AD_A'] == 1 and row['csf_AD_T'] == 0 else
                              'A-T+' if row['csf_AD_A'] == 0 and row['csf_AD_T'] == 1 else
                              'A+T+', axis=1)

df_epi['ratio_abeta42_40'] = df_epi['csf_abeta42'] / df_epi['csf_abeta40']

# Create the 'AT status' column based on the A and T status
df_epi['csf_AD_N'] = df_epi.apply(lambda row: 1 if row['csf_tTau'] >= 404 else 0, axis=1)

# Create the 'ATN status' column based on the A, T and N status
df_epi['ATN status'] = df_epi.apply(lambda row:  row['AT status'] + 'N+' if row['csf_tTau'] >= 404 else  row['AT status'] + 'N-', axis=1)


# Create the a 'SNAP/AD' column based on the A, T and N status
df_epi['SNAP/AD'] = df_epi.apply(lambda row: 'SNAP' if row['ATN status'] == 'A-T+N-' or  row['ATN status'] == 'A-T-N+' or row['ATN status'] == 'A-T+N+'else
                        'AD' if row['ATN status'] == 'A+T+N-' or row['ATN status'] == 'A+T+N+' else np.nan, axis=1)


a=1

df_epi.to_csv(path+'/data/'+file_name)