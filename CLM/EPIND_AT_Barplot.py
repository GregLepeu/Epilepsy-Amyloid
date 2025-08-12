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

# Bar plot using seaborn
title = 'AT status across cohort'
order = ['A-T-', 'A-T+', 'A+T-', 'A+T+']
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df, x='AT status', order=order)


# Barplot for epi patients
df_epi = df[df['Epi Soarian']==1]
title = 'AT status for epilepsy patients'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df_epi, x='AT status', order=order)

# Barplot for ND-epi patients
df_ND_epi = df[df['Epi ND']==1]
title = 'AT status for neurodegenrative epilepsy patients'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df_ND_epi, x='AT status', order=order)

# Show the plot
plt.show()

