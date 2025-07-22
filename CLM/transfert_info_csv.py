import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/data/"

file_1 = 'CLMPACSMOLIS_filter_LALIVE_20240304_Epi.csv'

file_2 = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_1 = pd.read_csv(path+file_1)

df_2 = pd.read_csv(path+file_2)

# Columns to update (all columns in df_1 except 'IPP')
columns_to_update = [col for col in df_1.columns if col not in ['IPP', 'subj_id']]

# Iterate over rows of df_1
for _, row in df_1.iterrows():
    ipp_value = row['IPP']
    # Check if the IPP value is in df_2['LFP']
    if ipp_value in df_2['IPP'].values:
        # Get the index of the row in df_2 where LFP matches the IPP value
        index = df_2[df_2['IPP'] == ipp_value].index[0]
        # Update the values in df_2
        df_2.loc[index, columns_to_update] = row[columns_to_update].values
    else:
        print(f"Error: IPP value {ipp_value} not found in df_2['IPP']")

df_2.to_csv(path+file_2)