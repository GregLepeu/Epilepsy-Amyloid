import os
import random
import string
import pandas as pd
import numpy as np


path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"

file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_epi = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Load CSV files into a pandas DataFrame
df_Clemens = pd.read_csv(path+'/data/'+'ATN_Gregory.csv', encoding='ISO-8859-1')

columns_to_update = ['A', 'CSF_AB42', 'CSF_AB42_AB40_RATIO', 'PET_AMYLOID','T',
                     'CSF_P_TAU', 'PET_TAU', 'N', 'N_H_TAU',
                     'N_PET_FDG', 'N_MRI']


# Ensure 'IPP' column exists in both DataFrames
if 'IPP' in df_epi.columns and 'IPP' in df_Clemens.columns:
    # Set 'IPP' as index in both dataframes for easier lookup
    df_Clemens.set_index('IPP', inplace=True)

    # Loop through each row in df1 and update values if 'IPP' is found in df2
    for index, row in df_epi.iterrows():
        ipp_value = row['IPP']
        if ipp_value in df_Clemens.index:
            # Update only if columns exist in df2
            for col in columns_to_update:
                if col in df_Clemens.columns:
                    df_epi.at[index, col] = df_Clemens.at[ipp_value, col]

    # Reset index of df2 if needed
    df_Clemens.reset_index(inplace=True)


a=1

df_epi['AD_A'] = df_epi.apply(lambda row: 1 if row['csf_AD_A']== 1 or row['A']=='POS' else 0, axis=1)
df_epi['AD_T'] = df_epi.apply(lambda row: 1 if row['csf_AD_T']== 1 or row['T']=='POS' else 0, axis=1)
df_epi['AD_N'] = df_epi.apply(lambda row: 1 if row['csf_AD_N']== 1 or row['N']=='POS' else 0, axis=1)

# Filter the DataFrame based on the two conditions
filtered_rows = df_epi[(df_epi['NPSY'] == 0)]


df_epi['CLEMENS AT status'] = df_epi.apply(lambda row: 'A-T-' if row['AD_A'] == 0 and row['AD_T'] == 0 else
                              'A+T-' if row['AD_A'] == 1 and row['AD_T'] == 0 else
                              'A-T+' if row['AD_A'] == 0 and row['AD_T'] == 1 else
                              'A+T+', axis=1)

df_epi['CLEMENS ATN status'] = df_epi.apply(lambda row:  row['CLEMENS AT status'] + 'N+' if row['AD_N'] ==1 else  row['AT status'] + 'N-', axis=1)

df_ND =  df_epi[(df_epi['AD_N'] == 1)]
df_not_ND = df_epi[(df_epi['AD_N'] == 0)]

a
