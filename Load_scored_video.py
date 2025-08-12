import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Desktop/"

file_name_1 = 'Scored_video.csv'
file_name_2 = 'correspondence_table.csv'


# Load CSV files into a pandas DataFrame
df_Racine_score = pd.read_csv(path+file_name_1)

df_correspondance = pd.read_csv(path+'randomized_files/'+file_name_2)

# Merge the two files
merged_df = pd.merge(df_Racine_score, df_correspondance, on='Random name')

merged_df['Animal'] = merged_df['Filename'].str[9:21]
merged_df['Session'] = merged_df['Filename'].str[22:25]
merged_df['Seizure n°'] = merged_df['Filename'].str[26:-4]

merged_df['Seizure n°'] [merged_df['Seizure n°'] == 'Sz'] = 'Sz1'

Racine_df = merged_df[['Animal','Session','Seizure n°', 'Modified Racine Score']]


Racine_df.to_csv('/Users/gregorylepeu/Documents/Research/Projects/Post-Ictal/Data/'+'Racine_score.csv')
a=1
