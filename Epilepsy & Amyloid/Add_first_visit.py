import os
import random
import string
import pandas as pd
import numpy as np

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/data/"

file_1 = 'Gregory_DateFirstVisit.csv'

file_2 = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_1 = pd.read_csv(path+file_1, encoding='ISO-8859-1')

df_2 = pd.read_csv(path+file_2, encoding='ISO-8859-1')


# Merge on 'IPP'
df = df_2.merge(df_1, on='IPP', how='left')

# Convert DATE_1 to datetime (specifying the format)
df['Date Dx Epi'] = pd.to_datetime(df['Date Dx Epi'], format='%d.%m.%y')

# Convert DATE_2 to datetime (automatic parsing)
df['First_Visit'] = pd.to_datetime(df['First_Visit'])

# Compute the difference in days, then convert to years
df['Year to Dx of ND'] = (df['Date Dx Epi'] - df['First_Visit']).dt.days / 365.25

df.to_csv(path+file_2)