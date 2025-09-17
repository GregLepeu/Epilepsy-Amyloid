import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import dabest

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name)

# Replace 'A-B-' with 'negative' in column C
df['Syndrome'] = df['Syndrome'].replace('Amnestic (pure)', 'Amnestic')
order = ['Diffuse','Amnestic','Executive','Attention', 'lvPPA','svPPA','nfvPPA','Langage','Normal']

# Bar plot using seaborn
title = 'Syndrome across cohort'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df, x='Syndrome', order=order)


# Barplot for epi patients
df_epi = df[df['Epi Soarian']==1]
title = 'Syndrome for epilepsy patients'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df_epi, x='Syndrome',order=order)

# Barplot for ND-epi patients
df_ND_epi = df[df['Epi ND']==1]
title = 'Syndrome for neurodegenrative epilepsy patients'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df_ND_epi, x='Syndrome',order=order)

# Show the plot
plt.show()

